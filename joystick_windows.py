from joystick_base import BaseJoystick
from vgamepad import VX360Gamepad, XUSB_BUTTON


class Joystick(BaseJoystick):
    """
    Wrapper around vgamepad to have a unified Joystick interface in both linux and windows.
    """
    # using the vgamepad lib, define the buttons and axes it supports

    # conversion from button number (1 to 15) to the internal vgamepad button id
    BUTTONS = (
        XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP,
        XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN,
        XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT,
        XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT,
        XUSB_BUTTON.XUSB_GAMEPAD_START,
        XUSB_BUTTON.XUSB_GAMEPAD_BACK,
        XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB,
        XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB,
        XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER,
        XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER,
        XUSB_BUTTON.XUSB_GAMEPAD_GUIDE,
        XUSB_BUTTON.XUSB_GAMEPAD_A,
        XUSB_BUTTON.XUSB_GAMEPAD_B,
        XUSB_BUTTON.XUSB_GAMEPAD_X,
        XUSB_BUTTON.XUSB_GAMEPAD_Y,
    )

    # conversion from axis number (1 to 5) to the internal vgamepad axis name
    AXES = (
        "triggers",  # both triggers add up together...
        "left_joystick_float:x_value_float",
        "left_joystick_float:y_value_float",
        "right_joystick_float:x_value_float",
        "right_joystick_float:y_value_float",
    )

    def __init__(self, id_):
        super().__init__(id_)
        self.pad = VX360Gamepad()
        # using the same names from vgamepad, to make things easier
        self.current_params_left_joystick_float = dict(x_value_float=-1, y_value_float=1)
        self.current_params_right_joystick_float = dict(x_value_float=-1, y_value_float=1)

    def press_button(self, button_number):
        """
        Hold down a button.
        """
        self.pad.press_button(button=self.BUTTONS[button_number - 1])
        self.pad.update()

    def release_button(self, button_number):
        """
        Release a button.
        """
        self.pad.release_button(button=self.BUTTONS[button_number - 1])
        self.pad.update()

    def move_axis(self, axis_number, value):
        """
        Set the value of an axis, as a ratio from 0 to 1.
        """
        if not 0 <= value <= 1:
            raise ValueError("The value for axis {axis_number} in joystick {self.id} can't be "
                             f"{value}, must be between 0 and 1")

        axis_name = self.AXES[axis_number - 1]
        if ":" in axis_name:
            value = value * 2 - 1
            axis_name, param = axis_name.split(":")
            if "y" in param:
                value = -value
            current_params = getattr(self, f"current_params_{axis_name}")
            current_params[param] = value
            getattr(self.pad, axis_name)(**current_params)
            self.pad.update()
        else:
            if value >= 0.5:
                # first half
                self.pad.left_trigger_float(value_float=value * 2)
                self.pad.right_trigger_float(value_float=0)
            else:
                # second half
                self.pad.left_trigger_float(value_float=0)
                self.pad.right_trigger_float(value_float=1 - value * 2)
            self.pad.update()
