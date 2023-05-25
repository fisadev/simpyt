import keyboard
import pyautogui


class Keyboard:
    """
    Wrapper around keyboard (the lib) to have a unified Keyboard between linux and windows.
    """
    VALID_KEYS = set(name.lower() for name in pyautogui.KEYBOARD_KEYS)

    def translate(self, keys):
        """
        Translate a set of pyautogui keys, to a string of keyboard (the lib) hotkeys.
        """
        # TODO do the actual translation
        return ", ".join(keys)

    def press(self, keys):
        """
        Press and keep holding a set of keys.
        """
        keyboard.press(self.translate(keys))

    def release(self, keys):
        """
        Release a set of keys.
        """
        keyboard.release(self.translate(keys))

    def press_and_release(self, keys):
        """
        Quickly press and release a set of keys.
        """
        keyboard.press_and_release(self.translate(keys))
