# TODO import some linux virtual joystick lib


class Joystick:
    """
    Wrapper around ??? joystick classes and quirks.
    """
    # using the vgamepad lib, define the buttons and axes it supports

    # conversion from button number (0 to ??) to the internal ??? button id
    BUTTONS = (
        "sample_fake_button_0",
        "sample_fake_button_1",
        "sample_fake_button_2",
    )

    # conversion from axis number (0 to ??) to the internal ??? axis name
    AXES = (
        "sample_fake_axis_0",
        "sample_fake_axis_1",
    )

    def __init__(self, id_):
        self.id = id_
        self.pad = None

    def press_button(self, button_number):
        """
        Hold down a button.
        """
        print("TODO: hold button", button_number)

    def release_button(self, button_number):
        """
        Release a button.
        """
        print("TODO: release button", button_number)

    def move_axis(self, axis_number, value):
        """
        Set the value of an axis, as a ratio from 0 to 1.
        """
        if not 0 <= value <= 1:
            raise ValueError("The value for axis {axis_number} in joystick {self.id} can't be "
                             f"{value}, must be between 0 and 1")

        print("TODO: move axis", axis_number, "to value", value)
