from uuid import uuid4

import yaml

from actions import Action

DEFAULT_GRID_WIDTH = 16
DEFAULT_GRID_HEIGHT = 4


class Control:
    """
    A control that can be displayed in a page, and run some actions when interacted with.
    """
    def __init__(self, x=0, y=0, width=1, height=1, target_page=None, color=None,
                 border_width=None, border_color="black", image=None, text=None, text_size="16px",
                 text_font="Verdana", text_color="black", text_horizontal_align="center",
                 text_vertical_align="center", linked_action=None, script=None):
        if actions is None:
            actions = []

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

        self.linked_action = actions
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

    def activate(self):
        """
        Run the actions that this control was configured to do.
        """
        for action in self.actions:
            action.run()

    @classmethod
    def deserialize(cls, raw_config):
        """
        Deserialize and load control configs from a simpyt page file.
        """
        linked_action, script = Action.deserialize(raw_config)
        return cls(**raw_config, linked_action=linked_action, script=script)


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
    def read(cls, name, pages_path):
        """
        Read the page definition from a yaml file.
        """
        page_path = pages_path / (name + ".page")
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
    def available_pages(cls, pages_path):
        """
        List all the available (config files) pages.
        """
        return [
            page_path.name[:-5]
            for page_path in pages_path.glob("*.page")
        ]
