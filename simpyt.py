from pathlib import Path
from shutil import copytree
import os
import sys
import platform

from pages import launch_pages_server
from midi import launch_midis_server


PLATFORM = platform.system()


class Simpyt:
    """
    The main app.
    """
    def __init__(self, root_configs_path, debug=False):
        self.root_configs_path = root_configs_path
        self.root_code_path = Path(__file__).parent.absolute()
        self.debug = debug

        self.web_thread = None
        self.midi_thread = None

    @property
    def assets_path(self):
        return self.root_code_path / "assets"

    @property
    def example_configs_path(self):
        return self.root_code_path / "example_configs"

    @property
    def pages_path(self):
        return self.root_configs_path / "pages"

    @property
    def images_path(self):
        return self.root_configs_path / "images"

    @property
    def midis_path(self):
        return self.root_configs_path / "midis"

    def run(self):
        if PLATFORM == "Windows":
            os.environ["PYTHONUNBUFFERED"] = "TRUE"

        print()
        print()
        print("-" * 20)
        print("WELCOME TO SYMPIT")
        print("-" * 20)
        print()
        print("Debug:", self.debug)
        print("Configs folder:", self.root_configs_path)

        if not self.root_configs_path.exists():
            print("No configs found, creating example configs")
            copytree(self.example_configs_path, self.root_configs_path)

        print("Simpyt initial setup complete! Running server...")
        print()

        self.web_thread = launch_pages_server(self)
        self.midi_thread = launch_midis_server(self)

        print("Simpyt is runnning!")
        print()

        self.web_thread.join()
        self.midi_thread.join()


if __name__ == "__main__":
    # configs placed either in the parent dir of the pyempaq pyz file or the simpyt.py file
    used_executable_dir_path = Path(os.environ.get("PYEMPAQ_PYZ_PATH", __file__)).parent

    simpyt_app = Simpyt(
        root_configs_path=(used_executable_dir_path / "configs").absolute(),
        debug="-d" in sys.argv,
    )
    simpyt_app.run()
