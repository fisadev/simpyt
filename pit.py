from uuid import uuid4

import yaml

import settings


class Control:
    """
    A control that can be displayed in a simpyt, and run some action when interacted with.
    """
    def __init__(self, position, id_=None, action=None, color=None, image=None):
        if id_ is None:
            id_ = str(uuid4())

        self.id = id_

        self.position = position
        self.action = action

        if color is None and image is None:
            print("PROBLEM: the control at position", position, "has no color or image. Setting "
                  "a green color as default.")
            color = "green"

        self.color = color
        self.image = image

    def act(self):
        """
        Run the action that this control was configured to do.
        """
        pass

    def serialize(self):
        """
        Serialize the control data to be able to store it in a simpyt config file.
        """
        return {
            "id": self.id,
            "position": self.position,

            "color": self.color,
            "image": self.image,

            # TODO class? action?
        }

    @classmethod
    def deserialize(cls, raw_config):
        """
        Deserialize and load control configs from a simpyt config file.
        """
        return cls(
            id_=raw_config["id"],
            position=raw_config["position"],

            color=raw_config["color"],
            image=raw_config["image"],

            # TODO class with other params? action?
        )


class Pit:
    """
    A collection of controls to show in pages.
    """
    def __init__(self, name, author, background, controls):
        self.name = name
        self.author = author
        self.background = background
        self.controls = controls

    @classmethod
    def read(cls, name):
        """
        Read the simpyt definition from a yaml file.
        """
        pit_path = settings.CONFIGS_PATH / (name + ".pit")
        with open(pit_path, "r") as pit_file:
            raw_config = yaml.safe_load(pit_file)

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
        Save the simpyt definition into a yaml file.
        """
        raw_config = {
            "author": self.author,
            "background": self.background,
            "controls": [
                ctrl.serialize()
                for ctrl in self.controls
            ],
        }

        pit_path = settings.CONFIGS_PATH / (self.name + ".pit")

        with open(pit_path, "w") as pit_file:
            yaml.safe_dump(raw_config, pit_file)

    @classmethod
    def example_pit(cls):
        """
        Create a very basic example Pit.
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
