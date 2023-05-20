from functools import partial
from pathlib import Path
from shutil import copytree
from threading import Thread
import os
import platform
import sys

from flask import Flask, render_template, redirect, send_from_directory

from pages import Page
from midi import MidiDevice, midi_integration_loop


if platform.system() == "Windows":
    # print buffering in windows hides output for too long
    print = partial(print, flush=True)


class SimPytApp(Flask):
    """
    The main flask app.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        current_path = Path(".").absolute()

        self.pages_cache = {}
        self.root_simpyt_path = Path(__file__).parent.absolute()
        self.root_configs_path = None

    @property
    def assets_path(self):
        return self.root_simpyt_path / "assets"

    @property
    def root_example_configs_path(self):
        return self.root_simpyt_path / "example_configs"

    @property
    def pages_path(self):
        return self.root_configs_path / "pages"

    @property
    def midis_path(self):
        return self.root_configs_path / "midis"

    @property
    def images_path(self):
        return self.root_configs_path / "images"

    def launch_server(self, root_configs_path, debug=False):
        """
        Do some global health checks and ensure we have everything we need, and then run the
        server.
        """
        self.root_configs_path = root_configs_path.absolute()

        print()
        print("-" * 20)
        print("WELCOME TO SYMPIT")
        print("-" * 20)
        print()
        print("Debug:", debug)
        print("Configs folder:", self.root_configs_path)

        if not self.root_configs_path.exists():
            print("No config folder found, creating a new one with example pages")
            copytree(self.root_example_configs_path, self.root_configs_path)

        print("SimPyt initial setup complete! Running server...")
        print()

        midi_devices = [MidiDevice.read(device_name, self.midis_path)
                        for device_name in MidiDevice.configured_devices(self.midis_path)]
        midi_thread = Thread(target=midi_integration_loop, args=[midi_devices])
        midi_thread.start()

        web_thread = Thread(target=self.run, kwargs=dict(host="0.0.0.0", port=9999, debug=debug))
        web_thread.start()

    def load_page(self, name, force_refresh=False):
        """
        Load a page from the cache, or read it from the file system.
        """
        if force_refresh:
            self.pages_cache.pop(name, None)

        if name in self.pages_cache:
            page = self.pages_cache[name]
        else:
            print("READING")
            page = Page.read(name, self.pages_path)
            self.pages_cache[name] = page

        return page


app = SimPytApp("simpyt")


@app.route("/")
def home():
    """
    Home page were we list the available configured pages.
    """
    return render_template("home.html", configured_pages=Page.configured_pages(app.pages_path))


@app.route("/page/<string:page_name>")
def page_show(page_name):
    """
    Show a particular page with controls.
    """
    page = app.load_page(page_name, force_refresh=True)
    return render_template("page.html", page=page)


@app.route("/page/<string:page_name>/reload")
def page_reload(page_name):
    """
    Force the reload (re-read from disk) of a particular page.
    """
    del app.pages_cache[page_name]
    return redirect(f"/page/{page_name}")


@app.route("/activate_control/<string:page_name>/<string:control_id>/<string:event_type>")
def activate_control(page_name, control_id, event_type):
    """
    Run the actions associated to a particular control of a particular page.
    """
    page = app.load_page(page_name)
    control, = [ctrl for ctrl in page.controls if ctrl.id == control_id]

    if event_type == "press_button":
        method_to_call = control.press_button
    elif event_type == "release_button":
        method_to_call = control.release_button

    control_run_thread = Thread(target=method_to_call)
    control_run_thread.start()
    return {"result": "ok"}


@app.route("/image/<path:image_path>")
def image_show(image_path):
    """
    Serve a particular image.
    """
    return send_from_directory(app.images_path, image_path)


@app.route("/assets/<path:asset_path>")
def assets_send(asset_path):
    """
    Serve the assets.
    """
    return send_from_directory(app.assets_path, asset_path)


if __name__ == "__main__":
    # configs placed either in the parent dir of the pyempaq pyz file or the simpyt.py file
    executable_at = Path(os.environ.get("PYEMPAQ_PYZ_PATH", __file__)).parent
    debug = "-d" in sys.argv
    app.launch_server(root_configs_path=executable_at / "configs", debug=debug)
