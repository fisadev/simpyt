from pathlib import Path
from shutil import copytree
import os
import platform


PLATFORM = platform.system()


class ImproperlyConfiguredException(Exception):
    """
    An error in some config, with enough info to tell the user where's the problem.
    """
    def __init__(self, reason, file_path=None):
        self.file_path = file_path
        self.reason = reason

    def as_user_friendly_text(self):
        """
        Generate a user-friendly text about this error.
        """
        return f"{self.reason}\nProblematic config: {self.file_path}"


class Simpyt:
    """
    The main app.
    """
    VERSION = "1.0.1"

    # class attribute, reference to the running app
    current = None

    def __init__(self, root_configs_path, debug=False, web_debug=False):
        self.root_configs_path = root_configs_path
        self.root_code_path = Path(__file__).parent.absolute()
        self.debug = debug
        self.web_debug = web_debug

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
        """
        Run the simpyt app.
        """
        assert Simpyt.current is None
        Simpyt.current = self

        if PLATFORM == "Windows":
            os.environ["PYTHONUNBUFFERED"] = "TRUE"

        print()
        print()
        print("#" * 21)
        print("  WELCOME TO SYMPIT")
        print("#" * 21)
        print()
        print("Version:", self.VERSION)
        print("Debug:", self.debug)
        print("Configs folder:", self.root_configs_path)

        if not self.root_configs_path.exists():
            print("No configs found, creating example configs")
            copytree(self.example_configs_path, self.root_configs_path)

        print("Simpyt initial setup complete! Running server...")
        print()
        print("You can browse your pages in this computer by clicking this link:")
        print("http://localhost:9999/")
        print("From other devices, you will need to use your computer IP address instead.")
        print()
        print("To stop Simpyt, press Ctrl+C several times in this terminal or click on this link:")
        print("http://localhost:9999/stop")
        print()

        # imported here to prevent circular imports
        from pages import launch_pages_server
        from midi import launch_midis_server

        self.web_thread = launch_pages_server()
        self.midi_thread = launch_midis_server()

        try:
            self.web_thread.join()
            self.midi_thread.join()
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        """
        Stop the full app.
        """
        print()
        print("Stopping Simpyt")
        print()
        os._exit(0)
