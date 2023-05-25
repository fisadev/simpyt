from threading import Thread
import logging

from flask import Flask, render_template, redirect, send_from_directory, cli

from pages import Page
from core import Simpyt


web_app = Flask("simpyt")


def initialize_web_app():
    """
    Configure the web app to run in the Simpyt context.
    """
    web_app.pages_cache = {}

    if not Simpyt.current.debug:
        web_app.logger.disabled = True
        logging.getLogger('werkzeug').disabled = True
        cli.show_server_banner = lambda *args: None

    return web_app


@web_app.route("/")
def home():
    """
    Home page were we list the available configured pages.
    """
    pages_names = Page.configured_pages(Simpyt.current.pages_path)
    return render_template(
        "home.html",
        pages_names=pages_names,
        configs_path=Simpyt.current.root_configs_path,
    )


@web_app.route("/page/<string:page_name>")
def page_show(page_name):
    """
    Show a particular page with controls.
    """
    try:
        page = Page.read(page_name, Simpyt.current.pages_path)
        web_app.pages_cache[page_name] = page

        return render_template("page.html", page=page)
    except Exception as err:
        return render_template("page_error.html", error=str(err))


@web_app.route("/activate_control/<string:page_name>/<string:control_id>")
def activate_control(page_name, control_id):
    """
    Run the actions associated to a particular control of a particular page.
    """
    page = web_app.pages_cache[page_name]
    control, = [ctrl for ctrl in page.controls if ctrl.id == control_id]

    control_run_thread = Thread(target=control.press_button)
    control_run_thread.start()

    return {"result": "ok"}


@web_app.route("/image/<path:image_path>")
def image_show(image_path):
    """
    Serve a particular image.
    """
    return send_from_directory(Simpyt.current.images_path, image_path)


@web_app.route("/assets/<path:asset_path>")
def assets_send(asset_path):
    """
    Serve the assets.
    """
    return send_from_directory(Simpyt.current.assets_path, asset_path)


@web_app.route("/stop")
def stop():
    """
    Stop Simpyt.
    """
    Simpyt.current.stop()
