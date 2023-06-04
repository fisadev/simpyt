# Simpyt

Convert your old phone, tablet, or even any MIDI controller, to a fully customizable button box for your flight sim :) (or any other apps).

Simpyt allows you to do two main things:

- Build "virtual" button boxes: pages with buttons that you can access from any phone or tablet and use as button boxes for your flight simulator, or any other app too. The buttons are customizable and fully programable: they can reproduce sequences of keys, simulate joystick actions, open apps, etc. And no special software is needed in the device, just a web browser.
- Use MIDI controllers as button boxes: if you have a MIDI controller, Simpyt allows you to map its buttons and knobs to virtual joysticks, key sequences, open apps, etc, just like the buttons of the pages.


## Installation and running

You just need to [download and install Python 3 from the official website](https://www.python.org/downloads/) (on Linux any modern Python 3 will do), then [download the latest Simpyt.pyz release](https://github.com/fisadev/simpyt/releases) and place it anywhere you want, and finally just double click it. That's it!

No extra apps are needed in the device you want to use as a button box (old phones or tablets are ideal). You only need a working web browser in them.

The first time you run the Simpyt app, a new `simpyt_configs` folder will be created next to the app. All the configs live inside that folder, no other hidden files are used for configs.

# Tutorial

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

That's ok! We provide an app to be able to inspect both he types and ids of the midi controls you have. Download the latest `midi_inspector.pyz` [release](https://github.com/fisadev/simpyt/releases), open a terminal, go to the folder where you have downloaded it, and run `python midi_inspector.pyz MY_DEVICE_NAME` (use the name of your device).

Then just use your midi controller, and this app will show you both the type and ids of the buttons and knobs you are testing.

In the future, the midi_inspector app will be integrated into Simpyt to make things easier. For now, this is the way :)

# Full docs

[PENDING]

# Developers

[PENDING]
