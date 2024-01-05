from threading import Thread
from time import sleep
from uuid import uuid4
import platform

import mido
import yaml

from actions import Action, JoystickAction
from core import Simpyt, ImproperlyConfiguredException


USE_PYGAME = platform.system() == "Windows"


if USE_PYGAME:
    import pygame
    import pygame.midi as pgm


class MidiDevice:
    """
    A collection of midi controls mapped to actions.
    """
    def __init__(self, name, controls, port=None):
        self.name = name
        self.controls = controls
        self.port = port

    @classmethod
    def read(cls, name):
        """
        Read the device definition from a yaml file.
        """
        device_path = Simpyt.current.midis_path / (name + ".midi_device")
        with open(device_path, "r") as page_file:
            raw_config = yaml.safe_load(page_file)

        try:
            raw_config["controls"] = [
                MidiControl.deserialize(ctrl_raw_config)
                for ctrl_raw_config in raw_config["controls"]
            ]
        except ImproperlyConfiguredException as icex:
            icex.file_path = device_path
            raise

        return cls(**raw_config)

    @classmethod
    def configured_devices(cls):
        """
        List all the configured (config files) midi devices.
        """
        return [
            midi_path.name[:-12]
            for midi_path in Simpyt.current.midis_path.glob("*.midi_device")
        ]


class MidiControl:
    """
    A control from a midi device, that can run some actions when interacted with.
    """
    def __init__(self, when_channel=None, when_is_program=False, when_control=None, when_note=None,
                 when_value_between=None, when_value_surpasses=None, linked_action=None,
                 script=None):
        self.id = uuid4().hex

        self.when_channel = when_channel
        self.when_is_program = when_is_program
        self.when_control = when_control
        self.when_note = when_note
        self.when_value_between = when_value_between
        self.when_value_surpasses = when_value_surpasses

        self.linked_action = linked_action
        self.script = script

        if self.when_value_between is not None and self.when_value_surpasses is not None:
            raise ValueError("Only one of when_value_between and when_value_surpasses can "
                             "be defined.")

        if self.linked_to_axis() and self.when_value_surpasses is not None:
            raise ValueError("When mapping a midi control to an axis, a range of values must be "
                             "specified instead of just a threshold")

    @classmethod
    def extract_midi_value(cls, midi_message):
        """
        Extract the most value-like attribute from the midi message, and convert it to something
        we can understand.
        For control_change and program_change messages, we have the 'value' and 'program'
        attributes.
        For note_on and note_off messages, we return either 1 or 0.
        """
        if hasattr(midi_message, "value"):
            value = midi_message.value
        elif hasattr(midi_message, "program"):
            value = midi_message.program
        elif midi_message.type == "note_on":
            value = 1
        elif midi_message.type == "note_off":
            value = 0
        else:
            raise ValueError("Can't find a value-like attribute in the midi message")

        return value

    def matches(self, midi_message):
        """
        Does a midi message matches our conditions?
        """
        if self.when_channel is not None and getattr(midi_message, "channel", None) != self.when_channel:
            return False

        if self.when_is_program and midi_message.type != "program_change":
            return False

        if self.when_control is not None:
            if midi_message.type != "control_change":
                return False
            elif midi_message.control != self.when_control:
                return False

        if self.when_note is not None:
            if midi_message.type not in ("note_on", "note_off"):
                return False
            elif midi_message.note != self.when_note:
                return False

        return True

    def linked_to_axis(self):
        """
        Is this control linked to an axis in a joystick?
        """
        return (
            isinstance(self.linked_action, JoystickAction)
            and self.linked_action.ControlType == JoystickAction.ControlType.AXIS
        )

    def run(self, midi_message):
        """
        Simulate buttons or axes in a virtual joystick.
        """
        input_value = self.extract_midi_value(midi_message)

        if self.when_value_between is not None:
            is_on = self.when_value_between[0] <= input_value <= self.when_value_between[1]
        elif self.when_value_surpasses is not None:
            is_on = input_value > self.when_value_surpasses

        # scripts are just on/off
        if self.script and is_on:
            self.script.run()

        # linked actions are more complex, depending on their type
        if self.linked_action:
            if self.linked_to_axis():
                # convert input midi control value to output joystick value
                input_min, input_max = self.when_value_between
                axis_value = (input_value - input_min) / (input_max - input_min)
                self.linked_action.run(Action.Mode.LINKED_CONTROL_MOVE, axis_value)
            else:
                if is_on:
                    # linked actions simulate the pressing down, and then releasing
                    # unlinked actions just run in the press down phase
                    if self.linked_action.CAN_BE_LINKED:
                        self.linked_action.run(Action.Mode.LINKED_CONTROL_PRESS)
                    else:
                        self.linked_action.run(Action.Mode.UNLINKED)
                else:
                    if self.linked_action.CAN_BE_LINKED:
                        self.linked_action.run(Action.Mode.LINKED_CONTROL_RELEASE)

    @classmethod
    def parse_when(cls, raw_when):
        """
        Parse the syntax of the 'when' attribute in midi controls. Return a dict of arguments to
        use when creating a MidiControl instance.
        """
        when_control = None
        when_note = None
        when_is_program = False
        value_condition_start_at = None

        when_value_between = None
        when_value_surpasses = None

        try:
            parts = raw_when.split()

            midi_type = parts.pop(0)

            if midi_type == "control":
                assert len(parts) == 3
                when_control = int(parts[0])
                condition_parts = parts[1:]
            elif midi_type == "note":
                assert len(parts) == 3
                when_note = int(parts[0])
                condition_parts = parts[1:]
            elif midi_type == "program":
                assert len(parts) == 2
                when_is_program = True
                condition_parts = parts
            else:
                raise ValueError(f"Unknown midi event type: {midi_type}")

            assert len(condition_parts) == 2
            condition_type, condition_value = condition_parts

            if condition_type == "between":
                value1, value2 = condition_value.split("-")
                when_value_between = int(value1), int(value2)
            elif condition_type == "surpasses":
                when_value_surpasses = int(condition_value)
            else:
                raise ValueError(f"Unknown condition: {parts[value_condition_start_at]}")

        except Exception as ex:
            raise ImproperlyConfiguredException(
                "The 'when' attribute in a midi control has an incorrect format:\n"
                f"when: {raw_when}"
            ) from ex

        # TODO support when_channel

        return dict(
            when_is_program=when_is_program,
            when_control=when_control,
            when_note=when_note,
            when_value_between=when_value_between,
            when_value_surpasses=when_value_surpasses,
        )

    @classmethod
    def deserialize(cls, raw_config):
        """
        Deserialize and load control configs from a simpyt midi file.
        """
        if "when" not in raw_config:
            raise ImproperlyConfiguredException(
                f"Missing 'when' attribute in midi control. Found attributes: {raw_config}"
            )

        when_args = cls.parse_when(raw_config.pop("when"))
        linked_action, script = Action.deserialize(raw_config)

        return cls(**when_args, linked_action=linked_action, script=script)


def midi_integration_loop():
    """
    Run the main loop of the midi integration.
    """
    if USE_PYGAME:
        pygame.init()
        pgm.init()
        midi_backend = mido.Backend('mido.backends.pygame')
    else:
        midi_backend = mido.Backend('mido.backends.rtmidi')

    devices = []

    for device_name in MidiDevice.configured_devices():
        try:
            device = MidiDevice.read(device_name)
            device.port = midi_backend.open_input(device.name)
            devices.append(device)

            print("Midi device found and configured:", device_name)
        except ImproperlyConfiguredException as ex:
            print(f"Midi device found but with problems in its config!: {device_name}\n"
                  f"{ex.as_user_friendly_text()}")
        except OSError:
            print("Midi device found, but couldn't connect to it! Is it plugged?:", device_name)
        except Exception as ex:
            print(f"Midi device found but failed to read its config!: {device_name}\n{ex}")

    if not devices:
        print("No midi devices configured, won't run the midi module of Simpyt")
        return

    devices_by_port_name = {device.port.name: device for device in devices}
    ports = [device.port for device in devices_by_port_name.values()]

    try:
        while True:
            for port, message in mido.ports.multi_receive(ports, yield_ports=True):
                device = devices_by_port_name[port.name]

                if Simpyt.current.debug:
                    message_details = f"type={message.type} "

                    channel = getattr(message, "channel", None)
                    if channel:
                        message_details += f"channel={channel} "

                    if message.type == "control_change":
                        message_details += f"control={message.control} "

                    if message.type in ("note_on", "note_off"):
                        message_details += f"note={message.note} "

                    value = MidiControl.extract_midi_value(message)
                    message_details += f"value={value}"

                    print("Interacted with midi device", device.name, message_details)

                for control in device.controls:
                    if control.matches(message):
                        control_run_thread = Thread(target=control.run, args=[message])
                        control_run_thread.start()

            sleep(0.01)
    except KeyboardInterrupt:
        pass

    if USE_PYGAME:
        pgm.quit()


def launch_midis_server():
    """
    Launch the midis server and return the thread.
    """
    midi_thread = Thread(target=midi_integration_loop, daemon=True)
    midi_thread.start()

    print("Midi app running!")

    if Simpyt.current.debug:
        print("Midi devices detected connected to your computer:")
        print("(you can use these names as the device name in midi devices configs)")
        for output_name in mido.get_output_names():
            print("    ", output_name)

    return midi_thread
