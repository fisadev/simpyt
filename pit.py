from uuid import uuid4

import yaml

from actions_management import get_actions_list
import settings

DEFAULT_GRID_WIDTH = 16
DEFAULT_GRID_HEIGHT = 4


class Control:
    """
    A control that can be displayed in a page, and run some actions when interacted with.
    """
    def __init__(self, x=0, y=0, width=1, height=1, actions=None, color=None, image=None):
        if actions is None:
            actions = []

        self.id = uuid4().hex

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.color = color
        self.image = image

        self.action = actions

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
        pass

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
            "actions": [{action.CONFIG_KEY: action.serialize() for action in self.actions}]

            # TODO class?
        }

    @classmethod
    def deserialize(cls, raw_config):
        """
        Deserialize and load control configs from a simpyt page file.
        """
        return cls(
            x=raw_config["x"],
            y=raw_config["y"],

            width=raw_config["width"],
            height=raw_config["height"],

            color=raw_config["color"],
            image=raw_config["image"],
            actions=get_actions_list(raw_config)

            # TODO class with other params?
        )


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

    def save(self):
        """
        Save the page definition into a yaml file.
        """
        raw_config = {
            "author": self.author,
            "background": self.background,
            "width": self.width,
            "height": self.height,
            "controls": [
                ctrl.serialize()
                for ctrl in self.controls
            ],
        }

        page_path = settings.PAGES_PATH / (self.name + ".page")

        with open(page_path, "w") as page_file:
            yaml.safe_dump(raw_config, page_file)

    @classmethod
    def available_pages(cls):
        """
        List all the available (config files) pages.
        """
        return [
            page_path.name[:-5]
            for page_path in settings.PAGES_PATH.glob("*.page")
        ]

    @classmethod
    def example_page(cls):
        """
        Create a very basic example Page.
        """
        return cls(
            name="example",
            author="SimPyt",
            background="black",
            width=15,
            height=4,
            controls=[
                Control(
                    x=0,
                    y=0,
                    width=1,
                    height=3,
                    color="rgba(255, 63, 63, .5)",
                    image="push-button-1.png",
                ),
                Control(
                    x=3,
                    y=1,
                    width=2,
                    height=1,
                    color="rgba(63, 255, 63, .5)",
                    image="push-button-2.png",
                )
            ],
        )
