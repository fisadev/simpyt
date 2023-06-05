# Basics

All pages can be accessed from the Simpyt home.
In the future, we plan to add some better navigation tools to move between pages.

Pages define a **grid**, and then buttons are placed inside that grid.
The grid is always composed of squared cells, to preserve aspect ratio accross different devices
(which is useful specially if you are using background images of aircraft pannels in them).

For instance, a page with the attributes:

```yaml
width: 200
height: 100
```

will always be twice as wide as high, no matter the form factor of the screen where you are showing it.
If for instance you access this page on a vertical tablet, then there will be some empty space below the page.

There are two main approaches to building your own button boxes:

- Using a background image and then just mapping regions of that image as buttons, which is useful to "reproduce" parts of an aircraft cockpit.
- Just using a simple background color and defining buttons with custom colors, texts, images, etc. Basically "drawing" your own UI.

Both are valid and useful, pick the one that works best for your use cases :)

# Examples

A button box using an image of an aircraft pannel, and mapping some regions of it to keyboard shortcuts (which should then be used in your flight sim), simulated joysticks, and scripts:

```yaml
background_image: tomcat_countermeasures_pannel.png
width: 200
height: 130
controls:
- at: 10 50 size 5 5
  simulate: keys ctrlright shiftright a
- at: 20 50 size 5 5
  simulate: joystick 1 button 3
- at: 30 50 size 10 10
  script:
  - keys crtl alt a
  - wait 0.2
  - keys F1
  - wait 0.2
  - keys F8
```

A button box drawing custom buttons from scratch instead, over a solid color background:

```yaml
background_color: lightgray
width: 200
height: 130
controls:
- at: 10 50 size 5 5
  text: "New tab"
  border_width: 3px
  border_color: black
  simulate: keys ctrl t
- at: 20 50 size 5 5
  text: "Simulate a joystick button"
  border_width: 3px
  border_color: black
  simulate: joystick 1 button 1
- at: 30 50 size 10 10
  image: hand_wave.png
  script:
  - run notepad.exe
  - wait 0.2
  - write hello world
```

As you can see, buttons can either just simulate a single keyboard/joystick event, or run complex scripts.

More examples and full docs full docs on the actions that buttons can run here: [here](https://github.com/fisadev/simpyt/blob/main/docs/actions.md).


# Global page attributes

| Attribute               | Usage                                                                                                        |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| width                   | Mandatory. How many columns the button box area should be split into. Example: `200`                                                                |
| height                  | Mandatory. How many rows the button box area should be split into. Example: `130`                                                                   |
| controls                | Mandatory. A list of controls to show in the page. See examples in the tutorial and full docs about Page control attributes.                        |
| background_image        | Optional. A name of an image file from `simpyt_configs/images` to use as background of the page. Example: `joystick_background.png`                 |
| background_color        | Optional. A name or code of a color to use as background of the page. Examples: `lightgray`, `"#00FF00"`. Quotes are needed when using color codes. |

We always ensure the grid is made of square bits. That way configs are portable accross different devices and screen form factors.

# Page control attributes

| Attribute               | Usage                                                                                                        |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| at                      | Mandatory. Specifies both the location, and the size of the button. Supports two different formats: initial position and size, or initial position and final position. Positions are specified as column-space-row, and sizes are specified as width-space-height. Examples: `10 20 size 8 5` (start at column 10 row 20, width 8 and height 5), `10 20 to 18 25` (start at column 10 row 20, end at column 18 row 25). |
| simulate                | Optional. Simulate keyboard keys or joystick buttons when the button is pressed. See the Actions full docs for examples and format.                                                                                                                                                                                                                                                                                     |
| script                  | Optional. A sequence of multiple actions to run when the button is pressed. See the Actions full docs for examples and format.                                                                                                                                                                                                                                                                                          |
| image                   | Optional. A name of an image file from `simpyt_configs/images` to use as background of the button. Example: `joystick_background.png`                                                                                                                                                                                                                                                                                   |
| color                   | Optional. A name or code of a color to use as background of the button. Examples: `lightgray`, `"#00FF00"`. Quotes are needed when using color codes.                                                                                                                                                                                                                                                                   |
| text                    | Optional. A text to display inside the button. Example: `"Open canopy"`. Quotes are recommended to prevent syntax issues, but can be skipped most of the times.                                                                                                                                                                                                                                                         |
| border_color            | Optional. A name or code of a color to use as border of the button. Examples: `lightgray`, `"#00FF00"`. Quotes are needed when using color codes.                                                                                                                                                                                                                                                                       |
| border_width            | Optional. The width and unit of measure for the border of the button. If not specified, the button is shown borderless. Example: `3px` (a 3 pixel border).                                                                                                                                                                                                                                                              |
| text_size               | Optional. The size and unit of measure for the text of the button, if using the `text` attribute. Example: `12px` (a 12 pixel font).                                                                                                                                                                                                                                                                                    |
| text_font               | Optional. The font name for the text of the button, if using the `text` attribute. Example: `Verdana`.                                                                                                                                                                                                                                                                                                                  |
| text_color              | Optional. A name or code of a color to use for the text of the button, if using the `text` attribute. Examples: `lightgray`, `"#00FF00"`. Quotes are needed when using color codes.                                                                                                                                                                                                                                     |
| text_horizontal_align   | EXPERIMENTAL. Optional. The horizontal alignment for the text of the button, if using the `text` attribute. Examples: `center`, `left`, `right`.                                                                                                                                                                                                                                                                        |
| text_vertical_align     | EXPERIMENTAL. Optional. The vertical alignment for the text of the button, if using the `text` attribute. Examples: `center`, `top`, `bottom`.                                                                                                                                                                                                                                                                          |
