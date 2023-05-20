from threading import Thread
from time import sleep
from uuid import uuid4
import platform

import mido
import yaml

from actions import Action, JoystickAction


USE_PYGAME = platform.system() == "Windows"


if USE_PYGAME:
    import pygame
    import pygame.midi as pgm


class MidiDevice:
    """
    A collection of midi controls mapped to actions.
    """
    def __init__(self, name, controls):
        self.name = name
        self.controls = controls

    @classmethod
    def read(cls, name, midis_path):
        """
        Read the device definition from a yaml file.
        """
        device_path = midis_path / (name + ".midi_device")
        with open(device_path, "r") as page_file:
            raw_config = yaml.safe_load(page_file)

        raw_config["controls"] = [
            MidiControl.deserialize(ctrl_raw_config)
            for ctrl_raw_config in raw_config["controls"]
        ]
        return cls(**raw_config)

    @classmethod
    def configured_devices(cls, midis_path):
        """
        List all the configured (config files) midi devices.
        """
        return [
            midi_path.name[:-12]
            for midi_path in midis_path.glob("*.midi_device")
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

    def extract_midi_value(self, midi_message):
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
                    self.linked_action.run(Action.Mode.LINKED_CONTROL_PRESS)
                else:
                    self.linked_action.run(Action.Mode.LINKED_CONTROL_RELEASE)

    @classmethod
    def deserialize(cls, raw_config):
        """
        Deserialize and load control configs from a simpyt midi file.
        """
        linked_action, script = Action.deserialize(raw_config)

        if "when" not in raw_config:
            raise ValueError("Missing 'when' attribute in midi control.")

        try:
            raw_when = raw_config.pop("when")
            parts = raw_when.split()

            when_control = None
            when_note = None
            when_is_program = False

            if parts[0] == "control":
                if len(parts) != 4:
                    raise ValueError("Incorrect number of parts")
                when_control = int(parts[1])
            elif parts[0] == "note":
                if len(parts) != 4:
                    raise ValueError("Incorrect number of parts")
                when_note = int(parts[1])
            elif parts[0] == "program":
                if len(parts) != 3:
                    raise ValueError("Incorrect number of parts")
                when_is_program = True
            else:
                raise ValueError("First part should be either 'control', 'note' or 'program'")

            when_value_between = None
            when_value_surpasses = None

            if parts[2] == "between":
                value1, value2 = parts[3].split("-")
                when_value_between = int(value1), int(value2)
            elif parts[2] == "surpasses":
                when_value_surpasses = int(parts[3])
            else:
                raise ValueError("Middle part should be either 'between' or 'surpasses'")

        except:
            raise ValueError(f"Incorrect control format: 'when: {raw_when}'")

        # TODO support when_channel

        return cls(when_channel=None, when_is_program=when_is_program, when_control=when_control,
                   when_note=when_note, when_value_between=when_value_between,
                   when_value_surpasses=when_value_surpasses,
                   linked_action=linked_action, script=script)


def midi_integration_loop(midi_devices):
    """
    Run the main loop of the midi integration.
    """
    if USE_PYGAME:
        pygame.init()
        pgm.init()
        midi_backend = mido.Backend('mido.backends.pygame')
    else:
        midi_backend = mido.Backend('mido.backends.rtmidi')

    ports = [midi_backend.open_input(device.name) for device in midi_devices]
    devices_by_port_name = {
        port.name: device
        for port, device in zip(ports, midi_devices)
    }

    try:
        while True:
            for port, message in mido.ports.multi_receive(ports, yield_ports=True):
                device = devices_by_port_name[port.name]

                for control in device.controls:
                    if control.matches(message):
                        control_run_thread = Thread(target=control.run, args=[message])
                        control_run_thread.run()

            sleep(0.01)
    except KeyboardInterrupt:
        if USE_PYGAME:
            pgm.quit()
