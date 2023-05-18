from pathlib import Path
from shutil import copytree
from threading import Thread

from flask import Flask, render_template, redirect, send_from_directory


from pit import Page


class SimPytApp(Flask):
    """
    The main flask app.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.pages_cache = {}
        self.assets_path = Path(".") / "assets"
        self.root_example_configs_path = Path('.') / "example_user_dir"
        self.root_configs_path = Path(".") / "config"

    @property
    def pages_path(self):
        return self.root_configs_path / "pages"

    @property
    def images_path(self):
        return self.root_configs_path / "images"

    def launch_server(self):
        """
        Do some global health checks and ensure we have everything we need, and then run the
        server.
        """
        if not self.root_configs_path.exists():
            print("No config folder found, creating a new one with example pages")
            copytree(self.root_example_configs_path, self.root_configs_path)

        print("SimPyt initial setup complete! Running server...")
        print()

        self.run(host="0.0.0.0", port=9999, debug=True)

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
    return render_template("home.html", available_pages=Page.available_pages(app.pages_path))


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


@app.route("/activate_control/<string:page_name>/<string:control_id>")
def activate_control(page_name, control_id):
    """
    Run the actions associated to a particular control of a particular page.
    """
    page = app.load_page(page_name)
    control, = [ctrl for ctrl in page.controls if ctrl.id == control_id]
    activation_thread = Thread(target=control.activate)
    activation_thread.run()
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
    app.launch_server()
