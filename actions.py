import pyautogui
import subprocess
import time
from abc import ABC, abstractmethod


class Action(ABC):
    """
    Action that can be triggered in interactions with a Control.

    To create a new type of action:
        - inherit from this class
        - overwrite all the abstractmethods
        - set the class attribute CONFIG_KEY with the key expected in the yaml to trigger the
        action.
    """

    CONFIG_KEY: str

    @abstractmethod
    def run(self):
        """
        Overwrite this method with the logic to run a specific action.
        """

    @abstractmethod
    def serialize(self):
        """
        Serialize the config for an Action instance.

        Returns:
            - a string or yaml-freindly format (such as a list of strings) with the config needed
            to instanciate this Action instance.
        """

    @classmethod
    @abstractmethod
    def deserialize(cls, config):
        """
        Create an Action instance based on the given config.
        """


class PressKeys(Action):
    """
    Press a specific sequence of keys.

    Params:
        - keys_to_press (list of strings): a list of keys to press.
    """
    CONFIG_KEY = "press"
    SEQ_KEY_SEP = ","
    KEY_SEP = "+"
    VALID_KEYS = [name.upper() for name in  pyautogui.KEYBOARD_KEYS]

    def __init__(self, keys_seq):
        self.keys_seq = keys_seq

    def are_valid_keys(self, keys):
        return all([key.upper() in self.VALID_KEYS for key in keys.split(self.KEY_SEP)])

    def run(self):
        for keys in self.keys_seq:
            if self.are_valid_keys(keys):
                pyautogui.hotkey(*keys.split(self.KEY_SEP))
                Wait().run()
            else:
                print("Key error on ", keys)

    def serialize(self):
        return " ".join(self.keys_seq)

    @classmethod
    def deserialize(cls, config):
        keys_to_press = config.split()

        return cls(keys_to_press)


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
    CONFIG_KEY = "wait"

    def __init__(self, seconds_to_wait=0.5):
        self.seconds_to_wait= seconds_to_wait


    def run(self):
        time.sleep(self.seconds_to_wait)


    def serialize(self):
        return self.seconds_to_wait

    @classmethod
    def deserialize(cls, config):
        return cls(seconds_to_wait=config)


class OpenApp(Action):
    """
    Open a specific app, given its name.

    Params:
        - app_path (str): Path to the executable of the app to open.
    """
    CONFIG_KEY = "open"

    def __init__(self, app_path):
        self.app_path = app_path.split("\n")

    def run(self):
        subprocess.run(self.app_path)

    def serialize(self):
        return self.app_path

    @classmethod
    def deserialize(cls, config):
        return cls(app_path=config)


if __name__ == "__main__":
    PressKeys(["Alt+1","Alt+2","Alt+3"]).run()
    OpenApp("/bin/ls").run()
