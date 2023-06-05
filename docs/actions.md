# Basics

Web buttons and midi controls can specify two attributes where they detail what to do when pressed/moved/etc:

- `simulate`, to basically "convert" that web/midi control into a simulated keyboard or joystick control.
- `script`, to fire a complex sequence of actions when that control is used.

The two of them end up running what we call "actions" in Simpyt. 
Simulate specifies a single action, while scripts specify a list of actions. But the syntax for actions is the same in both cases.

Scripts can use all available actions, while `simulate` attributes can only use keyboard keys and virtual joystick related actions.

# Available actions

## Keyboard keys

Example of a control simulating the ctrl+shift+a hotkey combination:

```yaml
(...)
simulate: keys ctrl shift a
```

Keyboard keys actions start with `keys`, and then just have a list of keys to press, separated by spaces. 
The keys will be pressed all at once, as a shortcut.
If you need a sequence of keys, you can use the `script` attribute instead of the `simulate` one.

Example of a script pressing several keys one after the other:

```yaml
(...)
script:
- keys a
- keys F12
- keys F11
- keys escape
```

It's usually a good idea to add `wait` actions in between key presses:

```yaml
(...)
script:
- keys a
- wait 0.1
- keys F12
- wait 0.1
- keys F11
- wait 0.1
- keys escape
```

These are the supported keys:

- Function keys: `f1` `f2` `f3` `f4` `f5` `f6` `f7` `f8` `f9` `f10` `f11` `f12` `f13` `f14` `f15` `f16` `f17` `f18` `f19` `f20` `f21` `f22` `f23` `f24` 
- Other top row keys: `escape` `esc` `printscreen` `prntscrn` `prtsc` `prtscr` `pause` 
- Basic alphanumeric keys: `0123456789abcdefghijklmnopqrstuvwxyz` 
- Symbols: ```;,.\/'[]-=` ```
- Navigation keys: `up` `down` `left` `right` `home` `end` `pagedown` `pgdn` `pageup` `pgup` `insert` 
- Line and deletion keys: `enter` `return` `space` `tab` `backspace` `del` `delete` `insert`
- Numpad: `num0` `num1` `num2` `num3` `num4` `num5` `num6` `num7` `num8` `num9` 
- Modifiers: `shift` `shiftleft` `shiftright` `ctrl` `ctrlleft` `ctrlright` `alt` `altleft` `altright` `win` `winleft` `winright` 

## Keyboard typing of text

[CAN'T BE USED IN `simulate` ATTRIBUTES!]

If you want to simulate the typing of a long text, you can use the `write` action too:

```yaml
(...)
script:
- write hello world
```

Right now the support for the `write` action is experimental, and many things aren't supported, like many
special symbols, uppercase letters (yeah... sorry :/).

## Joystick buttons and axis

Example of a control simulating a joystick button when activated:

```yaml
(...)
simulate: joystick 1 button 2
```

Example of a control (maybe a midi knob) simulating a joystick axis when changed:

```yaml
(...)
simulate: joystick 3 axis 4
```

Joystick actions basically create a simulated joystick that Windows will recognize as if you had connected a 
real joystick (no Linux support yet).
And you can even have multiple virtual joysticks, each one identified by its number (starting from 1).

Each joystick has 5 axis (1 to 5), and 15 buttons (1 to 15), but you don't need to use all of them.
And different controls in your button boxes can be mapped to the same virtual joystick controls, with 
unpredictable results :)

Joystick actions start with `joystick`, then specify the virtual joystick number, then the type of simulated
joystick control to use (`button` or `axis`), and then the control number (1 to 5 for axis, 1 to 15 for buttons).

In the very special case that you want to simulate an axis with something that isn't a midi knob 
with a range of values (for instance, using it in a script, or simulating a joystick axis with a simple button) then you will also need to specify what value to simulate in that axis. It's a value from 0 to 1.


Example of a script that would reset several simulated axis to their middle position:

```yaml
(...)
script: 
- joystick 1 axis 1 value 0.5
- joystick 1 axis 2 value 0.5
- joystick 1 axis 3 value 0.5
```

## Waits

[CAN'T BE USED IN `simulate` ATTRIBUTES!]

This action is only useful as an intermediate step in scripts, to wait some seconds in between them.
The wait time is expressed in seconds, with decimals supported.

Example of waiting half a second in between two other actions:

```yaml
(...)
script:
- run notepad.exe
- wait 0.5
- write hello world
```

## Running apps or commands

[CAN'T BE USED IN `simulate` ATTRIBUTES!]

This action is used to open an application or run any arbitrary command. 
It starts with `run`, and is followed by the command/app to execute.

Example of opening the Notepad app:

```yaml
(...)
script:
- run notepad.exe
```

## Quitting

[CAN'T BE USED IN `simulate` ATTRIBUTES!]

This action is used to stop Simpyt altogether, and receives no parameters.

Example:

```yaml
(...)
script:
- quit
```
