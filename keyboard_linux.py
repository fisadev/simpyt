import pyautogui


class Keyboard:
    """
    Wrapper around pyautogui to have a unified Keyboard between linux and windows.
    """
    VALID_KEYS = set(name.lower() for name in pyautogui.KEYBOARD_KEYS)

    def press(self, keys):
        """
        Press and keep holding a set of keys.
        """
        for key in keys:
            pyautogui.keyDown(key)

    def release(self, keys):
        """
        Release a set of keys.
        """
        for key in keys:
            pyautogui.keyUp(key)

    def press_and_release(self, keys):
        """
        Quickly press and release a set of keys.
        """
        pyautogui.hotkey(*keys)
