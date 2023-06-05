# Simpyt

Convert your old phone, tablet, or even any MIDI controller, to a fully customizable button box for your flight sim :) (or any other apps).

Simpyt allows you to do two main things:

- Create "virtual" button boxes: pages with programmable buttons that you can display and use from any phone or tablet.
- Use MIDI controllers as programmable button boxes.

The buttons are customizable and fully programable: they can reproduce sequences of keys, simulate joystick buttons or axis, open apps, etc.

## Installation and running

1. [Download and install Python 3 from the official website](https://www.python.org/downloads/) (on Linux any modern Python 3 will do)
2. [Download the latest Simpyt.pyz release](https://github.com/fisadev/simpyt/releases) and place it anywhere you want
3. Just run (double click) simpyt.pyz. 

That's it!

The first time you run it, it will take a few seconds to boot and create a `simpyt_configs` folder, where all your configs can be edited. The next time it should start up almost instantaneously.

No extra apps are needed in the devices you want to use as virtual button boxes (old phones or tablets are ideal). You only need a working web browser in them.

# Quick start

## Web button boxes (pages)

[PENDING: add a sample picture of a web button box]

After you first ran Simpyt and the `simpyt_configs` folder was created, a few demo pages were created inside the configs too. You can try them out by navigating with your browser to `http://127.0.0.1:9999` (from the same PC where Simpyt is running).

The pages are defined as files inside `simpyt_configs/pages`. Each page is a single file with `.page` extension that defines some basic settings, the list of buttons to show, and what they do. You can create as many as you need, just place them in that folder.

This is a basic example of a `.page` file:

```yaml
background_image: tomcat_countermeasures_pannel.png
width: 200
height: 130
controls:
- at: 10 50 size 5 5
  simulate: keys ctrlright shiftright a
- at: 20 50 size 5 5
  simulate: keys ctrlright shiftright b
```

(in case this format looks familiar: yes, it's yaml! :D)

Thats a simple page that uses a background image of some switches pannel from the F-14 Tomcat, defines a 200x130 grid on top of that background image, and then creates two buttons:
- One button at position 10,50 and size 5x5, which when pressed fires a key combination in your computer: `ctrl+shift+a`.
- Another button at position 15,50 and size 5x5, which when pressed fires another key combination: `ctrl+shift+b`.

With Simpyt running and this page inside yor configs folder, you can navigate with any old phone web browser to http://YOUR_COMPUTER_IP/, click on the page name, and you will see the button box. And if you touch with your fingers in the regions defined by those buttons, then your computer will simulate the specified key combinations (for instance, you could map those key combinations in your flight sim to operate the switches of the Tomcat).

For this to work, you also need to store the `tomcat_countermeasures_pannel.png` image in the `simpyt_configs/images` folder.

A background image is optional, you can just define a background color too. And you can use colors, borders, texts or even individual images for each button.

Buttons can simulate key presses, joystick button presses, open apps, or even run full scripts of actions.

Full docs on the attributes buttons can define and the actions they can run in the **Full docs** section, further below.

## Midi devices as button boxes

[PENDING: add a sample picture of a midi controller]

Midi devices don't require you to navigate to the Simpyt web app, but you still need `simpyt.pyz` to be running, and you can only stop it from the web interface.

Midi devices work almost like the web button boxes: you define a button box with a `.midi_device` file inside the `simpyt_configs/midis` folder, and the device file specifies some basic settings and a list of controls to use. You can have as many as you want, too (very useful if you have several midi controllers lying around!).

This is a basic example of a `.midi_device` file:

```yaml
name: MY_PIANO
controls:
- when: note 43 surpasses 64
  simulate: keys escape
- when: control 40 between 0-127
  simulate: joystick 1 axis 1
```

Thats a simple config that tries to connecto to a midi device called "MY_PIANO" (this should be the name that the midi device has in your system when connected to your computer). If the midi device is found, it will:
- Simulate the `escape` key on your computer whenever the note 43 is pressed in your midi controller.
- Simulate a virtual joystick axis movement when the knob with id 40 in your midi controller is moved.

Different type of midi controls are supported (notes, plain controls, program changers) and they can simulate key presses, joystick button presses or axis movements, open apps, or even run full scripts of actions.

Full docs on the supported midi controls and the actions they can run in the **Full docs** section, further below.

## I have a midi controller, but no idea about the ids of its controls

That's ok! We provide an app to be able to inspect both he types and ids of the midi controls you have. Download the latest `midi_inspector.pyz` [release](https://github.com/fisadev/simpyt/releases), open a terminal, go to the folder where you have downloaded it, and run:

```python midi_inspector.pyz MY_DEVICE_NAME``` 

(use the name of your device instead of "MY_DEVICE_NAME").

Then just use your midi controller, and this app will show you both the type and ids of the buttons and knobs you are testing.

In the future, the midi_inspector app will be integrated into Simpyt to make things easier. For now, this is the way :)

# Full docs

### Global page attributes

| Attribute               | Usage                                                                                                        |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| width                   | Mandatory. How many columns the button box area should be split into. Example: `200`                                                                |
| height                  | Mandatory. How many rows the button box area should be split into. Example: `130`                                                                   |
| controls                | Mandatory. A list of controls to show in the page. See examples in the tutorial and full docs about Page control attributes.                        |
| background_image        | Optional. A name of an image file from `simpyt_configs/images` to use as background of the page. Example: `joystick_background.png`                 |
| background_color        | Optional. A name or code of a color to use as background of the page. Examples: `lightgray`, `"#00FF00"`. Quotes are needed when using color codes. |

Important clarifications:

- We always ensure the grid is made of square bits. That way configs are portable accross different devices and screen form factors.

### Page control attributes

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

### Global midi device attributes

| Attribute               | Usage                                                                                                        |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| name                    | Mandatory. The name of the midi device, as seen by the operative system. Example: `PYANO-BRAND-XYZ`                                                 |
| controls                | Mandatory. A list of controls to map from the device. See examples in the tutorial and full docs about Midi control attributes.                     |

### Midi control attributes

| Attribute               | Usage                                                                                                        |
| ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| when                    | Mandatory. The real life midi control to monitor, and how to do read it. Supports many different formats, see below this table for detailed info.  |
| simulate                | Optional. Simulate keyboard keys or joystick buttons or axis when the midi control is used. See the Actions full docs for examples and format.     |
| script                  | Optional. A sequence of multiple actions to run when the midi control is used. See the Actions full docs for examples and format.                  |

Reading midi controls:

The midi controls supported come in three different types: `note`, `control` and `program`.
Any button or knob in your midi controller might "fire" events of these types. You need to know both the type and the "id" of the control, to tell Simpyt to listen for changes in it.
Most pianos, drums, and the like tend to fire `note` events. Most knobs and extra buttons tend to fire `control` events. And `program` events tend to be fired by devices with speciall buttons meant to switch different pre defined programs.

Also, you have two options in how to deal with the inputs from the control: do something when its value surpasses a threshold, or do something when the value is between a range.

Some examples:

- `when: note 43 surpasses 20`: this tells Simpyt to do something when the note 43 is pressed, and its value is equal or above 20. In something like a piano, notes can have different values depending on how hard you hit them. These values are usually between 0 and 127.
- `when: control 6 surpasses 64`: this tells Simpyt do something when the control button with id 6 is pressed. Buttons tend to fire an event with value 127 when pressed, and 0 when released.
- `when: control 7 between 20-40`: this tells Simpyt to do something when the control knob with id 7 is placed in between 20 and 40. This would be useful for isntance to map only a part of that knob movement, to an axis of a virtual joystick.
- `when: program beteeen 0-127`: this tells Simpyt to do something when the "program" knob (if your controller has one) is placed between the 0 and 127 positions. Again, could be useful to map this to a virtual joystick axis that then you can use in your flight sim.

In general, it makes sense to use `surpasses` with buttons, piano keys, drum pads, etc. And to map those to key presses, virtual joystick buttons, or even scripts.

And it makes sense to use `between` with knobs, and to map that to virtual joystick axis.

You can do something else instead, but stuff tend to be less predictable if not used like that :)

### Actions for page or midi controls (simulate/script)

[PENDING]

# Developers

[PENDING]
