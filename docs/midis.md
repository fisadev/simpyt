# Midi devices as button boxes

To use midi devices you first need to know this: each time you interact with a button, key, knob, etc 
in your midi device, it sends "messages" to your computer. 
Simpyt allows you to capture those messages and do things when they're received, like simulating key presses,
moving joystick axis, running programs, etc.

Midi devices have three main types of "thingies" that are supported by Simpyt:

- Things that produce musical notes. Typical midi pianos and drums tend to emit these messages.
- Things that produce "control change" events. Typical midi knobs tend to emit these messages.
- Things that produce "program change" events. Some midi controllers have program buttons or knobs that emit these.

Notes and controls events have a note or control id, plus a value (intensity?) for that note or control.
Program events just have a program value.

Simpyt can capture those values and map them to a simulated joystick axis, or use thresholds to run actions 
when the received value crosses that threshold.

For instance, you could configure Simpyt to open an application when a piano note is pressed strongly enough,
or to simulate a joystick axis when some midi knob is turned.

# Examples

Mapping a couple of knobs and buttons from a midi controller, to a simulated virtual joystick that your games can detect and use:

```yaml
name: MY-MIDI-CONTROLLER-BRAND-XYZ
controls:
- when: control 1 between 0-127
  action: joystick 1 axis 1
- when: control 2 between 0-127
  action: joystick 1 axis 2
- when: note 40 surpasses 64
  action: joystick 1 button 1
- when: note 41 surpasses 64
  action: joystick 1 button 2
```

Using a piano to simulate keyboard keys, run apps and do more complex sequences of actions:

```yaml
name: MY-PIANO-BRAND-XYZ
controls:
- when: note 40 surpasses 64
  action: keys ctrl shift a
- when: note 41 surpasses 64
  action: run regedit.exe
- when: note 42 surpasses 64
  script:
  - run notepad.exe
  - wait 0.2
  - write nice tunes
```

As you can see, midi controls can either just simulate a single keyboard/joystick event, or run complex scripts.
More examples and full docs full docs on the actions that they can run here: [here](https://github.com/fisadev/simpyt/blob/main/docs/actions.md).


# I have a midi controller, but no idea about the types and ids of its thingies

That's ok! Simpyt can help you identify your midi device and the types and ids of the controls in it.
Open a terminal, go to the folder where you have downloaded `simpyt.pyz`, and run:

```
py simpyt.pyz -d
``` 

(replace `py` with `python` if you're on Linux)

The first useful thing you will notice are some messages like these:

```
System midi device detected: SOME NAME
System midi device detected: ANOTHER NAME
System midi device detected: SOME OTHER NAME
```

Those are the midi devices you have plugged to your computer and could be used by Simpyt. Copy one of those names into a 
new Simpyt midi device to start using it.

Once you have a Simpyt midi device created, be sure to stop and re-start Simpyt, again using the terminal and the `-d` parameter.

Then just use your midi controller, and the app will show you both the type and ids of the buttons and knobs you are using.
Take note of those values, and use them in your device configs.


# Global midi device attributes

| Attribute               | Usage                                                                                                        |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| name                    | Mandatory. The name of the midi device, as seen by the operative system. Example: `PYANO-BRAND-XYZ`                                                 |
| controls                | Mandatory. A list of controls to map from the device. See examples in the tutorial and full docs about Midi control attributes.                     |

# Midi control attributes

| Attribute               | Usage                                                                                                        |
| ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| when                    | Mandatory. The real life midi control to monitor, and how to do read it. Supports many different formats, see below this table for detailed info.  |
| action                  | Optional. A single action to run when the midi control is used. See the Actions full docs for examples and format.                                 |
| script                  | Optional. A sequence of multiple actions to run when the midi control is used. See the Actions full docs for examples and format.                  |

### The `when` attribute:

The `when` attribute specifies when to run the action, and has two main parts: what type of midi control fires
it, and under which conditions.

The first part must specify what kind of midi event and control/note id to listen for. 
Examples: `note 43`, `control 6`, or just `program` (to react to midi program changes).

The second part must specify under which values Simpyt must run the action.
It's either a threshold, to run the actions only when the value for that note/control/program surpasses that
threshold, or a range, to run the actions only when the value for that note/control/program is inside the 
specified range.
Examples: `surpasses 50`, `between 10-30`, etc.

Combining both things together, some full examples:

- `when: note 43 surpasses 20`: this tells Simpyt to do something when the note 43 is pressed, and its value is equal or above 20. In something like a piano, notes can have different values depending on how hard you hit them. These values are usually between 0 and 127.
- `when: control 6 surpasses 64`: this tells Simpyt do something when the control button with id 6 is pressed. Buttons tend to fire an event with value 127 when pressed, and 0 when released.
- `when: control 7 between 20-40`: this tells Simpyt to do something when the control knob with id 7 is placed in between 20 and 40. This would be useful for isntance to map only a part of that knob movement, to an axis of a virtual joystick.
- `when: program beteeen 0-127`: this tells Simpyt to do something when the "program" knob (if your controller has one) is placed between the 0 and 127 positions. Again, could be useful to map this to a virtual joystick axis that then you can use in your flight sim.

In general, it makes sense to use `surpasses` with buttons, piano keys, drum pads, etc. And to map those to key presses, virtual joystick buttons, or even scripts.

And it makes sense to use `between` with knobs, and to map that to virtual joystick axis.

You can do something else instead, but stuff tend to be less predictable if not used like that :)
