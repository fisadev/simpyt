import platform
import subprocess
import time
from abc import ABC, abstractmethod
from enum import Enum
from time import sleep

from core import Simpyt, ImproperlyConfiguredException

PLATFORM = platform.system()

if PLATFORM == "Windows":
    from joystick_windows import Joystick
    import pydirectinput as keyboard_lib
elif PLATFORM == "Linux":
    from joystick_linux import Joystick
    import pyautogui as keyboard_lib
else:
    raise ValueError(f"Unsuported platform: {PLATFORM}")


class Action(ABC):
    """
    Action that can be triggered in interactions with a Control.

    To create a new type of action:
        - inherit from this class
        - overwrite all the abstractmethods
        - set the class attribute PREFIX with the prefix expected in the config files to trigger
          the action.
    """
    PREFIX: str
    CAN_BE_LINKED = False
    HAS_PARAMETERS = True

    ACTIONS_BY_PREFIX = {}

    class Mode(Enum):
        """
        The modes in which actions can be used.
        """
        # action being "linked" to the status of a particular control. For instance: a keys action
        # linked to a button, will press and hold down the keys while the button is down, and
        # release them when the button is up. Or a midi controller linked to a joystick axis will
        # move the axis of the joystick when the midi controller is moved
        LINKED_CONTROL_PRESS = "linked_press"
        LINKED_CONTROL_RELEASE = "linked_release"
        LINKED_CONTROL_MOVE = "linked_move"
        # action being ran unlinked to the status of any real life control, for instance as a step
        # in a script
        UNLINKED = "unlinked"

    @abstractmethod
    def run(self, mode):
        """
        Overwrite this method with the logic to run a specific action.
        """

    @classmethod
    def register(cls, action_class):
        """
        Register an action class, to the dict of actions by prefix.
        """
        cls.ACTIONS_BY_PREFIX[action_class.PREFIX] = action_class
        return action_class

    @classmethod
    def deserialize(cls, raw_config):
        """
        Deserialize a linked action, or a script of actions, or even both, defined for a control.
        """
        linked_action = None
        script = None

        raw_linked_action = raw_config.pop("action", None)
        raw_script = raw_config.pop("script", None)

        if raw_linked_action:
            linked_action = cls.find_and_deserialize(raw_linked_action)

        if raw_script:
            script = Script(
                [cls.find_and_deserialize(script_action_raw_config)
                 for script_action_raw_config in raw_script]
            )

        return linked_action, script

    @classmethod
    def find_and_deserialize(cls, raw_config):
        """
        Find the specific Action class from the prefix, and then deserialize it passing the rest
        of the config.
        """
        try:
            parts = raw_config.split()
            prefix = parts[0]

            try:
                action_class = cls.ACTIONS_BY_PREFIX[prefix]
            except KeyError as ex:
                raise ImproperlyConfiguredException(f"Unknown action: {raw_config}") from ex

            if action_class.HAS_PARAMETERS:
                if len(parts) < 2:
                    raise ValueError(f"Incorrect action format: {raw_config}")

                action_raw_config = " ".join(parts[1:])
            else:
                action_raw_config = None

            return action_class.deserialize(action_raw_config)

        except ImproperlyConfiguredException:
            # if we got a nice error, just pass it around
            raise
        except Exception as ex:
            # otherwise, generate a nice error
            raise ImproperlyConfiguredException(
                f"This action has an incorrect format: {raw_config}"
            ) from ex


class Script:
    """
    A sequence of actions to be called in unlinked mode.
    """
    def __init__(self, actions):
        self.actions = actions

    def run(self):
        """
        Execute all the actions.
        """
        for action in self.actions:
            action.run(Action.Mode.UNLINKED)


@Action.register
class KeysAction(Action):
    """
    Press specific keys from the keyboard.
    When used in scripts, it just preses and releases the specified keys in a single step with the
    specified interval in between them.
    When used in linked mode, the up and down of the keys is linked to the up and down of the
    control using it.

    Params:
        - keys (list of strings): a list of strings with keys to press
    """
    PREFIX = "keys"
    CAN_BE_LINKED = True

    VALID_KEYS = [
        # top row
        'escape', 'esc',
        'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
        'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19',
        'f20', 'f21', 'f22', 'f23', 'f24',
        'printscreen', 'prntscrn', 'prtsc', 'prtscr', 'pause',

        # normal keys
        *'0123456789abcdefghijklmnopqrstuvwxyz',
        # symbols, only some of them (not all work on windows)
        *r";,.\/'[]-=`"

        # navigation block and spaces
        'enter', 'return', 'space', 'tab',
        'backspace', 'del', 'delete', 'insert',
        'home', 'end', 'pagedown', 'pgdn', 'pageup', 'pgup', 'insert',
        'up', 'down', 'left', 'right',

        # numpad
        'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6', 'num7', 'num8', 'num9',

        # modifiers
        'shift', 'shiftleft', 'shiftright',
        'ctrl', 'ctrlleft', 'ctrlright',
        'alt', 'altleft', 'altright',
        'win', 'winleft', 'winright',
    ]

    def __init__(self, keys):
        self.keys = [key.lower() for key in keys]
        self.ensure_valid_keys(keys)

    def ensure_valid_keys(self, keys):
        """
        Ensure that all the specified keys are valid, otherwise raise an error.
        """
        for key in keys:
            if not key in self.VALID_KEYS:
                raise ValueError(f"Unknown or unsupported key: {key}")

    def hold_down(self):
        """
        Hold down the defined keys.
        """
        for key in self.keys:
            keyboard_lib.keyDown(key)

    def release(self):
        """
        Release the defined keys.
        """
        for key in reversed(self.keys):
            keyboard_lib.keyUp(key)

    def run(self, mode):
        """
        Execute the acton.
        """
        if mode == self.Mode.UNLINKED:
            self.hold_down()
            sleep(0.1)
            self.release()
        elif mode == self.Mode.LINKED_CONTROL_PRESS:
            self.hold_down()
        elif mode == self.Mode.LINKED_CONTROL_RELEASE:
            self.release()

    @classmethod
    def deserialize(cls, raw_config):
        """
        Read the config and return a configured Action.
        """
        try:
            keys = raw_config.split()
        except:
            raise ValueError(f"The format of a 'press' action is incorrect: {raw_config}")

        return cls(keys)


@Action.register
class Write(Action):
    """
    Write a text.

    Params:
        - text (string): a string to be typed with the keyboard
    """
    PREFIX = "write"

    def __init__(self, text):
        self.text = text

    def run(self, mode):
        """
        Execute the action.
        """
        # if used in linked mode, execute the action in the control release
        if mode in (self.Mode.UNLINKED, self.Mode.LINKED_CONTROL_RELEASE):
            keyboard_lib.write(self.text)

    @classmethod
    def deserialize(cls, raw_config):
        """
        Read the config and return a configured Action.
        """
        return cls(raw_config)


@Action.register
class Wait(Action):
    """
    Wait some seconds.

    This action is useful to combine with other actions when you need to wait some time
    between them.

    Params:
        - seconds_to_wait (int|float): time in seconds to wait. Defaults to 0.5.


    Minimun time in second is different between OSs
    Check https://stackoverflow.com/questions/1133857/how-accurate-is-pythons-time-sleep/

    """
    PREFIX = "wait"

    def __init__(self, seconds_to_wait=0.5):
        self.seconds_to_wait= seconds_to_wait

    def run(self, mode):
        """
        Execute the action.
        """
        # if used in linked mode, execute the action in the control release
        if mode in (self.Mode.UNLINKED, self.Mode.LINKED_CONTROL_RELEASE):
            time.sleep(self.seconds_to_wait)

    @classmethod
    def deserialize(cls, raw_config):
        """
        Read the config and return a configured Action.
        """
        return cls(seconds_to_wait=float(raw_config))


@Action.register
class RunCommand(Action):
    """
    Run a specific command.

    Params:
        - command (str): Command of the app to run.
    """
    PREFIX = "run"

    def __init__(self, command):
        self.command = command

    def run(self, mode):
        """
        Execute the action.
        """
        # if used in linked mode, execute the action in the control release
        if mode in (self.Mode.UNLINKED, self.Mode.LINKED_CONTROL_RELEASE):
            subprocess.Popen(self.command, shell=True)

    @classmethod
    def deserialize(cls, raw_config):
        """
        Read the config and return a configured Action.
        """
        return cls(raw_config)


@Action.register
class JoystickAction(Action):
    """
    Press specific buttons or move axes from a joystick.

    Butons behave just like keys in both modes (linked and unlinked).
    Axes in linked mode require a value to be passed in the call.
    Axes in unlinked mode require a value to be specified in the config, initially, and will
    allways be used.

    Params:
        - joystick_id (int): the number of virtual joystick to use
        - control_type (JoystickAction.ControlType): the type of control to use, button or axis
        - control_id (int): the number of button or axis to use
        - unlinked_axis_value (optional float): the value to use when movin an axis in unlinked
          mode (from -1 to 1)
    """
    PREFIX = "joystick"
    CAN_BE_LINKED = True

    class ControlType(Enum):
        """
        Types of joystick controls.
        """
        AXIS = "axis"
        BUTTON = "button"

    def __init__(self, joystick_id, control_type, control_id, unlinked_axis_value=None):
        self.joystick_id = joystick_id
        self.control_type = control_type
        self.control_id = control_id
        self.unlinked_axis_value = unlinked_axis_value
        self.joystick = Joystick.get(self.joystick_id)

        self.ensure_valid_controls()

    def ensure_valid_controls(self):
        """
        Ensure that the specified keys are valid, otherwise raise an error.
        """
        if self.control_type == self.ControlType.BUTTON:
            limit = len(self.joystick.BUTTONS)
        elif self.control_type == self.ControlType.AXIS:
            limit = len(self.joystick.AXES)

        if not 1 <= self.control_id <= limit:
            raise ValueError(f"Joystick {self.control_type.value} goes form 1 to {limit}, "
                             f"can't be {self.control_id}")

    def run(self, mode, value=None):
        """
        Execute the acton.
        """
        if self.control_type == self.ControlType.BUTTON:
            if mode == self.Mode.UNLINKED:
                self.joystick.press_button(self.control_id)
                time.sleep(0.1)
                self.joystick.release_button(self.control_id)
            elif mode == self.Mode.LINKED_CONTROL_PRESS:
                self.joystick.press_button(self.control_id)
            elif mode == self.Mode.LINKED_CONTROL_RELEASE:
                self.joystick.release_button(self.control_id)

        elif self.control_type == self.ControlType.AXIS:
            if value and self.unlinked_axis_value is None:
                raise ValueError("To use an axis not tied to an actual midi device axis, you must "
                                 f"specify a fixed value for it (joystick {self.joystick_id}, "
                                 f"axis {self.control_id})")
            if value is None:
                value = self.unlinked_axis_value

            if mode in (self.Mode.UNLINKED, self.Mode.LINKED_CONTROL_MOVE):
                self.joystick.move_axis(self.control_id, value)

    @classmethod
    def deserialize(cls, raw_config):
        """
        Read the config and return a configured Action.
        """
        try:
            parts = raw_config.split()
            assert len(parts) in (3, 5)

            joystick_id = int(parts[0])
            control_type = cls.ControlType(parts[1])
            control_id = int(parts[2])

            if len(parts) == 5:
                assert parts[3] == "value"
                unlinked_axis_value = float(parts[4])
            else:
                unlinked_axis_value = None
        except:
            raise ValueError(f"The format of a 'joystick' action is incorrect: {raw_config}")

        return cls(joystick_id, control_type, control_id, unlinked_axis_value)


@Action.register
class Quit(Action):
    """
    Just quit Sympit.
    """
    PREFIX = "quit"
    HAS_PARAMETERS = False

    def run(self, mode):
        """
        Execute the action.
        """
        # if used in linked mode, execute the action in the control release
        if mode in (self.Mode.UNLINKED, self.Mode.LINKED_CONTROL_RELEASE):
            Simpyt.current.stop()

    @classmethod
    def deserialize(cls, raw_config):
        """
        Read the config and return a configured Action.
        """
        return cls()
