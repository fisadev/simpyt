# Midi devices as button boxes

[PENDING INTRO]

# I have a midi controller, but no idea about the ids of its controls

That's ok! We provide an app to be able to inspect both he types and ids of the midi controls you have. Download the latest `midi_inspector.pyz` [release](https://github.com/fisadev/simpyt/releases), open a terminal, go to the folder where you have downloaded it, and run:

```bash
python midi_inspector.pyz MY_DEVICE_NAME
``` 

(use the name of your device instead of "MY_DEVICE_NAME").

Then just use your midi controller, and this app will show you both the type and ids of the buttons and knobs you are testing.

In the future, the midi_inspector app will be integrated into Simpyt to make things easier. For now, this is the way :)

# Global midi device attributes

| Attribute               | Usage                                                                                                        |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| name                    | Mandatory. The name of the midi device, as seen by the operative system. Example: `PYANO-BRAND-XYZ`                                                 |
| controls                | Mandatory. A list of controls to map from the device. See examples in the tutorial and full docs about Midi control attributes.                     |

# Midi control attributes

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
