import time, pyautogui
from abc import ABC, abstractclassmethod


class Action(ABC):
    """
    Action that can be triggered in interactions with a Control.
    """

    @abstractclassmethod
    def run(self):
        """
        Overwrite this method to implement the logic to run a specific action.
        """


class PressKeys(Action):
    """
    Press a specific sequence of keys.

    Params:
        - keys_to_press (list of strings): a list of keys to press.
    """
    SEQ_KEY_SEP = ","
    KEY_SEP = "+"
    VALID_KEYS = [name.upper() for name in  pyautogui.KEYBOARD_KEYS]

    def __init__(self, keys_seq):
        self.keys_seq = keys_seq.split(self.SEQ_KEY_SEP)

    def are_valid_keys(self, keys):
        return all([key.upper() in self.VALID_KEYS for key in keys.split(self.KEY_SEP)])

    def run(self):
        for keys in self.keys_seq:
            if self.are_valid_keys(keys):
                pyautogui.hotkey(*keys.split(self.KEY_SEP))
                Wait().run()
            else:
                print("Key error on ", keys)

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

    def __init__(self, seconds_to_wait=0.5):
        self.seconds_to_wait= seconds_to_wait


    def run(self):
        time.sleep(self.seconds_to_wait)


class OpenApp(Action):
    """
    Open a specific app, given its name.

    Params:
        - app_path (str): Path to the executable of the app to open.
    """

    def __init__(self, app_path):
        self.app_path= app_path

    def run(self):
        # TODO open self.app_path
        ...


if __name__ == "__main__":
    PressKeys("Alt+1,Alt+2,Alt+3").run()
