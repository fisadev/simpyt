# Quick start

## Web button boxes (pages)

[PENDING: add a sample picture of a web button box]

The pages are defined as files inside `simpyt_configs/pages`. 
Each page is a single file with `.page` extension with some basic settings, the list of buttons to show, and what they do. 
You can create as many as you need and use them at the same time from different devices.

Example of a simple `.page` file:

```yaml
background_image: tomcat_countermeasures_pannel.png
width: 200
height: 130
controls:
- at: 10 50 size 5 5
  action: keys ctrl shift a
- at: 20 50 size 5 5
  action: keys ctrl shift b
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
You define a midi button box with a `.midi_device` file inside the `simpyt_configs/midis` folder, specifying its name and a list of controls to use. 
You can have as many as you want at the same time, too.

Example of a basic `.midi_device` file:

```yaml
name: MY-PIANO-BRAND-XYZ
controls:
- when: note 43 surpasses 64
  action: keys escape
- when: control 40 between 0-127
  action: joystick 1 axis 1
```

Thats a simple config that tries to connecto to a midi device called "MY-PIANO-BRAND-XYZ" (this should be the name that the midi device has in your system when plugged in). 
It fires the `escape` key when a note is played in the midi device, and simulates a virtual joystick axis when some knob is turned.

Different types of midi controls are supported and they can simulate key presses, joystick buttons or axis, open apps, or even run full scripts of actions.

More examples and full docs on the configuration of midi devices [here](https://github.com/fisadev/simpyt/blob/main/docs/midis.md).

More examples and full docs full docs on the actions they can run here: [here](https://github.com/fisadev/simpyt/blob/main/docs/actions.md).

