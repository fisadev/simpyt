from time import sleep
import sys
import platform

import mido


USE_PYGAME = platform.system() == "Windows"


if USE_PYGAME:
    import pygame
    import pygame.midi as pgm


def run_inspector(device_names):
    """
    Run the main loop of the app.
    """
    if USE_PYGAME:
        pygame.init()
        pgm.init()
        midi_backend = mido.Backend('mido.backends.pygame')
    else:
        midi_backend = mido.Backend('mido.backends.rtmidi')

    ports = [midi_backend.open_input(name) for name in device_names]

    try:
        while True:
            for port, message in mido.ports.multi_receive(ports, yield_ports=True):
                if message.type == "program_change":
                    kind = "is_program"
                    id_ = "(not applicable)"
                    value = message.program
                elif message.type == "control_change":
                    kind = "control"
                    id_ = message.control
                    value = message.value
                elif message.type == "note_on":
                    kind = "note"
                    id_ = message.note
                    value = 1
                elif message.type == "note_off":
                    kind = "note"
                    id_ = message.note
                    value = 0

                print(
                    f'device="{port.name}"',
                    f"kind={kind}", f"control/note={id_}", f"value={value}",
                    flush=True,
                )

            sleep(0.01)
    except KeyboardInterrupt:
        print("Quitting", flush=True)
        if USE_PYGAME:
            pgm.quit()


run_inspector(sys.argv[1:])
