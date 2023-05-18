from uuid import uuid4

import yaml

from actions_management import get_actions_list
import settings

from actions import PressKeys, Wait

DEFAULT_GRID_WIDTH = 16
DEFAULT_GRID_HEIGHT = 4


class Control:
    """
    A control that can be displayed in a page, and run some actions when interacted with.
    """
    def __init__(self, x=0, y=0, width=1, height=1, actions=None, target_page=None, color=None,
                 border_width=None, border_color="black", image=None, text=None, text_size="16px",
                 text_font="Verdana", text_color="black", text_horizontal_align="center",
                 text_vertical_align="center"):
        if actions is None:
            actions = []

        self.id = uuid4().hex

        self.x = x
        self.y = y
        self.width = width
        self.height = height

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

        self.actions = actions
        self.target_page = target_page

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

    def activate(self):
        """
        Run the actions that this control was configured to do.
        """
        for action in self.actions:
            action.run()

    def serialize(self):
        """
        Serialize the control data to be able to store it in a simpyt config file.
        """
        return {
            "x": self.x,
            "y": self.y,

            "width": self.width,
            "height": self.height,

            "color": self.color,
            "image": self.image,
            "border_width": self.border_width,
            "border_color": self.border_color,

            "text": self.text,
            "text_size": self.text_size,
            "text_font": self.text_font,
            "text_color": self.text_color,
            "text_horizontal_align": self.text_horizontal_align,
            "text_vertical_align": self.text_vertical_align,

            "target_page": self.target_page,
            "actions": [{action.CONFIG_KEY: action.serialize()} for action in self.actions]
        }

    @classmethod
    def deserialize(cls, raw_config):
        """
        Deserialize and load control configs from a simpyt page file.
        """
        raw_config["actions"] = get_actions_list(raw_config)
        return cls(**raw_config)


class Page:
    """
    A collection of controls to show together.
    """
    def __init__(self, name, author, background, controls,
                 width=DEFAULT_GRID_WIDTH, height=DEFAULT_GRID_HEIGHT):
        self.name = name
        self.author = author
        self.background = background
        self.width = width
        self.height = height
        self.controls = controls

    @property
    def extra_cells(self):
        """
        Based on the dimension of the grid and the number of cells taken by the controls,
        return the number of cells that would need to be rendered to complete the grid.
        """
        total_cells = self.width * self.height
        taken_cells = sum(ctrl.width * ctrl.height for ctrl in self.controls)
        return max(0, total_cells - taken_cells)

    @classmethod
    def read(cls, name):
        """
        Read the page definition from a yaml file.
        """
        page_path = settings.PAGES_PATH / (name + ".page")
        with open(page_path, "r") as page_file:
            raw_config = yaml.safe_load(page_file)

        return cls(
            name=name,
            author=raw_config["author"],
            background=raw_config["background"],
            width=raw_config["width"],
            height=raw_config["height"],
            controls=[
                Control.deserialize(ctrl_raw_config)
                for ctrl_raw_config in raw_config["controls"]
            ],
        )

    @classmethod
    def available_pages(cls):
        """
        List all the available (config files) pages.
        """
        return [
            page_path.name[:-5]
            for page_path in settings.PAGES_PATH.glob("*.page")
        ]
