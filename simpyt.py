from pathlib import Path
from threading import Thread

from flask import Flask, render_template

from pit import Page, Control
import settings

app = Flask(__name__)


def launch_server():
    """
    Do some global health checks and ensure we have everything we need, and then run the server.
    """
    if not settings.PAGES_PATH.exists():
        print("No pages directory, creating an empty one")
        settings.PAGES_PATH.mkdir()

    if not settings.IMAGES_PATH.exists():
        print("No images directory, creating an empty one")
        settings.IMAGES_PATH.mkdir()

    if len(Page.available_pages()) == 0:
        print("No pages present, creating an example page")
        Page.example_page().save()

    print("SimPyt initial setup complete! Running server...")
    print()

    app.run(host="0.0.0.0", port=9999, debug=True)


@app.route("/")
def home():
    """
    Home page were we list the available configured pages.
    """
    return render_template("home.html", available_pages=Page.available_pages())


@app.route("/page/<string:page_name>")
def page(page_name):
    """
    Show a particular page with controls.
    """
    page_ = Page.read(page_name)
    return render_template("page.html", page=page_)


@app.route("/activate_control/<string:page_name>/<string:control_id>")
def activate_control(page_name, control_id):
    """
    Run the actions associated to a particular control of a particular page.
    """
    page_ = Page.read(page_name)
    # control, = [ctrl for ctrl in page_.controls if ctrl.id == control_id]
    control = page_.controls[0]  # TODO for testing, replace with line above
    activation_thread = Thread(target=control.activate)
    activation_thread.run()
    return {"result": "ok"}


launch_server()