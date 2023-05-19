import pyautogui
import subprocess
import time
from abc import ABC, abstractmethod
from enum import Enum


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

    ACTIONS_BY_PREFIX = {}

    class Mode(Enum):
        """
        The modes in which actions can be used.
        """
        # action being "linked" to the status of a particular control. For instance: a keys action
        # linked to a button, will press and hold down the keys while the button is down, and
        # release them when the button is up.
        LINKED_CONTROL_PRESS = "linked_press"
        LINKED_CONTROL_RELEASE = "linked_release"
        # action being ran unlinked to the status of any control, for instance as a step in a
        # script
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

    @classmethod
    def deserialize(cls, raw_config):
        """
        Deserialize a linked action, or a script of actions, or even both, defined for a control.
        """
        linked_action = raw_config.pop("simulate", None)
        script = raw_config.pop("script", None)

        if linked_action:
            linked_action = cls.find_and_deserialize(linked_action)

        if script:
            script = Script(
                [cls.find_and_deserialize(script_action_raw_config)
                 for script_action_raw_config in script]
            )

        return linked_action, script

    @classmethod
    def find_and_deserialize(cls, raw_config):
        """
        Find the specific Action class from the prefix, and then deserialize it passing the rest
        of the config.
        """
        parts = raw_config.split()

        if len(parts) < 2:
            raise ValueError(f"Incorrect action format: {raw_config}")

        prefix = parts[0]
        action_raw_config = " ".join(parts[1:])

        if prefix not in cls.ACTIONS_BY_PREFIX:
            raise ValueError(f"Unknown action: {prefix}")

        return cls.ACTIONS_BY_PREFIX[prefix].deserialize(action_raw_config)


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
    KEY_SEP = "+"
    VALID_KEYS = set(name.upper() for name in  pyautogui.KEYBOARD_KEYS)

    def __init__(self, keys, interval_s):
        self.keys = keys
        self.interval_s = interval_s
        self.ensure_valid_keys(keys)

    def ensure_valid_keys(self, keys):
        """
        Ensure that all the specified keys are valid, otherwise raise an error.
        """
        for key in keys:
            if not key.upper() in self.VALID_KEYS:
                raise ValueError(f"Unknown key: {key}")

    def run(self, mode):
        """
        Execute the acton.
        """
        if mode == self.Mode.UNLINKED:
            pyautogui.hotkey(*self.keys, interval=self.interval_s)
        elif mode == self.Mode.LINKED_CONTROL_PRESS:
            for key in self.keys:
                pyautogui.keyDown(key)
        elif mode == self.Mode.LINKED_CONTROL_RELEASE:
            for key in self.keys:
                pyautogui.keyUp(key)

    @classmethod
    def deserialize(cls, raw_config):
        """
        Read the config and return a configured Action.
        """
        try:
            parts = raw_config.split()
            assert len(parts) in (1, 2)

            keys = parts[0].split(cls.KEY_SEP)

            if len(parts) == 2:
                interval_s = float(parts[1].replace("s", ""))
            else:
                interval_s = 0.1
        except:
            raise ValueError(f"The format of a 'press' action is incorrect: {raw_config}")

        return cls(keys, interval_s)


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
            pyautogui.write(self.text, interval=0.1)

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
        return cls(seconds_to_wait=int(raw_config))


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
