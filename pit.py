from uuid import uuid4

import yaml

import settings


class Control:
    """
    A control that can be displayed in a simpyt, and run some action when interacted with.
    """
    def __init__(self, position, actions=None, color=None, image=None):
        if actions is None:
            actions = []

        self.id = str(uuid4())

        self.position = position
        self.action = actions

        if color is None and image is None:
            print("PROBLEM: the control at position", position, "has no color or image. Setting "
                  "a green color as default.")
            color = "green"

        self.color = color
        self.image = image

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
            "position": self.position,

            "color": self.color,
            "image": self.image,

            # TODO class? action?
        }

    @classmethod
    def deserialize(cls, raw_config):
        """
        Deserialize and load control configs from a simpyt page file.
        """
        return cls(
            position=raw_config["position"],

            color=raw_config["color"],
            image=raw_config["image"],

            # TODO class with other params? action?
        )


class Page:
    """
    A collection of controls to show together.
    """
    def __init__(self, name, author, background, controls):
        self.name = name
        self.author = author
        self.background = background
        self.controls = controls

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
            page_path.name.replace(".page", "")
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
            controls=[
                Control(
                    position=(0, 0),
                    color="green",
                )
            ],
        )
