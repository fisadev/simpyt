from uuid import uuid4
from threading import Thread

import yaml

from actions import Action

DEFAULT_GRID_WIDTH = 20
DEFAULT_GRID_HEIGHT = 10


class Page:
    """
    A collection of controls to show together, mapped to actions.
    """
    def __init__(self, name, controls, background_color=None, background_image=None,
                 width=DEFAULT_GRID_WIDTH, height=DEFAULT_GRID_HEIGHT):
        self.name = name
        self.background_color = background_color
        self.background_image = background_image
        self.width = width
        self.height = height
        self.controls = controls

    @classmethod
    def read(cls, name, pages_path):
        """
        Read the page definition from a yaml file.
        """
        page_path = pages_path / (name + ".page")
        with open(page_path, "r") as page_file:
            raw_config = yaml.safe_load(page_file)

        raw_config["name"] = name
        raw_config["controls"] = [
            PageButton.deserialize(ctrl_raw_config)
            for ctrl_raw_config in raw_config["controls"]
        ]
        return cls(**raw_config)

    @classmethod
    def configured_pages(cls, pages_path):
        """
        List all the configured (config files) pages.
        """
        return [
            page_path.name[:-5]
            for page_path in pages_path.glob("*.page")
        ]


class PageButton:
    """
    A control that can be displayed in a page, and run some actions when interacted with.
    """
    def __init__(self, row=1, col=1, row_end=2, col_end=2, target_page=None, color=None,
                 border_width=None, border_color="black", image=None, text=None, text_size="16px",
                 text_font="Verdana", text_color="black", text_horizontal_align="center",
                 text_vertical_align="center", linked_action=None, script=None):
        self.id = uuid4().hex

        self.row = row
        self.col = col
        self.row_end = row_end
        self.col_end = col_end

        self.target_page = target_page

        self.color = color
        self.image = image
        self.border_width = border_width
        self.border_color = border_color

        self.text = text
        self.text_size = text_size
        self.text_font = text_font
        self.text_color = text_color
        self.text_horizontal_align = text_horizontal_align
        self.text_vertical_align = text_vertical_align

        self.linked_action = linked_action
        self.script = script

    def press_button(self):
        """
        The button was pressed.
        """
        # TODO right now I don't have a way to hold buttons pressed on the web, so I can't
        # implement something like in the midi controls where you can hold down a button. So
        # everything is just ran on press and in UNLINKED mode, no hold vs release logic
        if self.linked_action:
            self.linked_action.run(Action.Mode.UNLINKED)

        if self.script:
            self.script.run()

    @classmethod
    def deserialize(cls, raw_config):
        """
        Deserialize and load control configs from a simpyt page file.
        """
        linked_action, script = Action.deserialize(raw_config)

        if "at" not in raw_config:
            raise ValueError("Missing 'at' attribute in page control.")

        try:
            raw_at = raw_config.pop("at")
            parts = raw_at.split()

            if len(parts) != 5:
                raise ValueError("Incorrect number of parts")

            col = int(parts[0])
            row = int(parts[1])

            if parts[2] == "to":
                col_end = int(parts[3])
                row_end = int(parts[4])
            elif parts[2] == "size":
                col_end = col + int(parts[3])
                row_end = row + int(parts[4])
        except:
            raise ValueError(f"Incorrect control format: 'at: {raw_at}'")

        return cls(row=row, col=col, row_end=row_end, col_end=col_end,
                   linked_action=linked_action, script=script,
                   **raw_config)


def launch_pages_server(simpyt_app):
    """
    Launch the pages server and return the thread.
    """
    from pages_web_app import initialize_web_app

    web_app = initialize_web_app(simpyt_app)

    web_thread = Thread(target=web_app.run,
                        kwargs=dict(host="0.0.0.0", port=9999, debug=simpyt_app.debug),
                        daemon=True)
    web_thread.start()

    return web_thread
