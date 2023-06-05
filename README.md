# Simpyt

Convert your old phone, tablet, or even any MIDI controller, to a fully customizable button box for your flight sim :) (or any other apps).

Simpyt allows you to do two main things:

- Create "virtual" button boxes: pages with programmable buttons that you can display and use from any phone or tablet.
- Use MIDI controllers as programmable button boxes.

The buttons are customizable and fully programable: they can reproduce sequences of keys, simulate joystick buttons or axis, open apps, etc.

# Quick start

## Installation and running

1. [Download and install Python 3 from the official website](https://www.python.org/downloads/) (on Linux any modern Python 3 will do)
2. [Download the latest Simpyt.pyz release](https://github.com/fisadev/simpyt/releases) and place it anywhere you want
3. Just run (double click) simpyt.pyz. 

That's it!

The first time you run it will take a few seconds to boot and create a `simpyt_configs` folder, where all your configs live. The next time it should start up almost instantaneously.

No extra apps are needed in the devices you want to use as virtual button boxes (old phones or tablets are ideal). You only need a working web browser in them.

## Web button boxes (pages)

[PENDING: add a sample picture of a web button box]

Simpyt comes with a couple of demo button boxes. Just run simpyt.pyz and open [http://127.0.0.1:9999](http://127.0.0.1:9999) in your browser to try them.

The pages are defined as files inside `simpyt_configs/pages`. 
Each page is a single file with `.page` extension that defines some basic settings, the list of buttons to show, and what they do. 
You can create as many as you need and use them at the same time from different devices.

Example of a simple `.page` file:

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

(in case this looks familiar: yes, it's yaml :D)

That page would show an image of a Tomcat cockpit pannel (which should be added in the `simpyt_configs/images` folder), with a couple of clickeable buttons that fire some key presses in your computer when clicked. 
You would map those keys to stuff in your flight sim, and that's it! A working button box :)

To show the button box in a phone or tablet, just connect the device to the same network than your pc and browse to `http://YOUR_COMPUTER_IP/`.

The page and buttons are fully customizable (text, color, borders, images, etc).
Buttons can simulate key presses, joystick button presses, open apps, or even run full scripts of actions.

More examples and full docs on the attributes of buttons and pages [here](https://github.com/fisadev/simpyt/blob/main/docs/pages.md).

More examples and full docs full docs on the actions they can run here: [here](https://github.com/fisadev/simpyt/blob/main/docs/actions.md).

## Midi devices as button boxes

[PENDING: add a sample picture of a midi controller]

Midi devices work almost like the web button boxes, except instead of using a web browser you just interact with your physical midi device.
You define a midi button box with a `.midi_device` file inside the `simpyt_configs/midis` folder, and the device file specifies some basic settings and a list of controls to use. 
You can have as many as you want at the same time, too.

Example of a basic `.midi_device` file:

```yaml
name: MY-PIANO-BRAND-XYZ
controls:
- when: note 43 surpasses 64
  simulate: keys escape
- when: control 40 between 0-127
  simulate: joystick 1 axis 1
```

Thats a simple config that tries to connecto to a midi device called "MY-PIANO-BRAND-XYZ" (this should be the name that the midi device has in your system when plugged in). 
It fires the `escape` key when a note is played in the midi device, and simulates a virtual joystick axis when some knob is turned.

Different type of midi controls are supported and they can simulate key presses, joystick buttons or axis, open apps, or even run full scripts of actions.

More examples and full docs on the configuration of midi devices [here](https://github.com/fisadev/simpyt/blob/main/docs/midis.md).

More examples and full docs full docs on the actions they can run here: [here](https://github.com/fisadev/simpyt/blob/main/docs/actions.md).
