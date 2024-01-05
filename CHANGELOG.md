# Pending release

- Hotfix: debug mode was breaking the app, fixed it.
- Separated "debug" (-d parameter) and "web debug" (-wd) modes. Debug mode is intended for users, while web debug mode is internal for devs working on Simpyt.
- New behaviours when in debug mode:
    - Any borderless buttons in web button pages are shown with a green border, to make things easier to debug.
    - Show details about buttons being pressed.
    - List system detected midi devices.
    - Show details about midi controls being used (as long as the device is configured for Simpyt).

# v1.0.1

- Hotfix: make keys in actions case insensitive (it was supposed to be like that, but there was a bug in the valid keys check)

# v1.0.0

- First release!! :) This initial Simpyt version supports:
    - Using phone/tablets as button boxes (with configirable button pages), with visually customizable buttons (color, size, position, text, image, etc).
    - Using midi devices as button boxes (reading notes and encoders)
    - Simulating key presses, fake joystick axes, run commands and even scripts.
