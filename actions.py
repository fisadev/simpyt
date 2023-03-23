import time
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

    def __init__(self, keys_to_press):
        self.keys_to_press = keys_to_press

    def run(self):
        # TODO: send this keys as OS keyboard input
        ...


class Wait(Action):
    """
    Wait some seconds.

    This action is useful to combine with other actions when you need to wait some time
    between them.

    Params:
        - seconds_to_wait (int|float): time in seconds to wait. Defaults to 0.5.
    """

    def __init__(self, seconds_to_wait=0.5):
        self.seconds_to_wait= seconds_to_wait


    def run(self):
        time.sleep(self.seconds_to_wait)


class OpenApp(Action):
    """
    Open a specific app, given its name.

    Params:
        - app_name (str): Name of the app to open.
    """

    def __init__(self, app_name):
        self.app_name= app_name

    def run(self):
        # TODO open self.app_name
        ...
