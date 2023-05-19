from uuid import uuid4

import yaml

from actions import Action

DEFAULT_GRID_WIDTH = 16
DEFAULT_GRID_HEIGHT = 4


class PageButton:
    """
    A control that can be displayed in a page, and run some actions when interacted with.
    """
    def __init__(self, x=0, y=0, width=1, height=1, target_page=None, color=None,
                 border_width=None, border_color="black", image=None, text=None, text_size="16px",
                 text_font="Verdana", text_color="black", text_horizontal_align="center",
                 text_vertical_align="center", linked_action=None, script=None):
        self.id = uuid4().hex

        self.x = x
        self.y = y
        self.width = width
        self.height = height

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

    @property
    def column_start(self):
        return self.x + 1

    @property
    def column_end(self):
        return self.column_start + self.width

    @property
    def row_start(self):
        return self.y + 1

    @property
    def row_end(self):
        return self.row_start + self.height

    def press_button(self):
        """
        The button is being held down.
        """
        if self.linked_action:
            self.linked_action.run(Action.Mode.LINKED_CONTROL_PRESS)

    def release_button(self):
        """
        The button was released.
        """
        if self.linked_action:
            self.linked_action.run(Action.Mode.LINKED_CONTROL_RELEASE)

        if self.script:
            self.script.run()

    @classmethod
    def deserialize(cls, raw_config):
        """
        Deserialize and load control configs from a simpyt page file.
        """
        linked_action, script = Action.deserialize(raw_config)
        raw_at = raw_config.pop("at")
        parts = raw_at.split()

        if len(parts) != 5 or parts[2] != "to":
            raise ValueError(f"Incorrect control format: 'at: {raw_at}'")

        x = int(parts[0])
        y = int(parts[1])
        width = int(parts[3]) - x
        height = int(parts[4]) - y

        return cls(x=x, y=y, width=width, height=height,
                   linked_action=linked_action, script=script,
                   **raw_config)


class Page:
    """
    A collection of controls to show together.
    """
    def __init__(self, name, background, controls,
                 width=DEFAULT_GRID_WIDTH, height=DEFAULT_GRID_HEIGHT):
        self.name = name
        self.background = background
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
    def available_pages(cls, pages_path):
        """
        List all the available (config files) pages.
        """
        return [
            page_path.name[:-5]
            for page_path in pages_path.glob("*.page")
        ]
