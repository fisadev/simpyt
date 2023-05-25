class BaseJoystick:
    """
    Base class for joystick implementations on different platforms.
    """

    # these two should be defined to specify the list of supported buttons and axis. These names
    # aren't meant to be known by the user, who will just specify the number for the button or
    # axis. Instead, here we translate those to whatever id the libs we use require
    BUTTONS = ()
    AXES = ()

    # already defined joysticks
    _cache = []

    @classmethod
    def get(cls, id_):
        """
        Get or create a joystick with the specified id, ensuring we have all other joysticks up to
        that id also defined (they MUST be created in order, to preserve mappings and hardware
        ids!!!)
        Joystick ids start at 1, it's a user input.
        """
        # create any missing joysticks, including the requested one
        while len(cls._cache) < id_:
            cls._cache.append(cls(id_))

        # return the requested joystick
        return cls._cache[id_ - 1]

    def __init__(self, id_):
        self.id = id_

    def press_button(self, button_number):
        """
        Hold down a button.
        """
        ...

    def release_button(self, button_number):
        """
        Release a button.
        """
        ...

    def move_axis(self, axis_number, value):
        """
        Set the value of an axis, as a ratio from 0 to 1.
        """
        ...
