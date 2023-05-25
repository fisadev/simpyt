from threading import Thread

from flask import Flask, render_template, redirect, send_from_directory

from pages import Page

web_app = Flask("simpyt")
web_app.simpyt_app = None
web_app.pages_cache = {}


@web_app.route("/")
def home():
    """
    Home page were we list the available configured pages.
    """
    pages_names = Page.configured_pages(web_app.simpyt_app.pages_path)
    return render_template("home.html", pages_names=pages_names)


@web_app.route("/page/<string:page_name>")
def page_show(page_name):
    """
    Show a particular page with controls.
    """
    page = Page.read(page_name, web_app.simpyt_app.pages_path)
    web_app.pages_cache[page_name] = page
    return render_template("page.html", page=page)


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
    return send_from_directory(web_app.simpyt_app.images_path, image_path)


@web_app.route("/assets/<path:asset_path>")
def assets_send(asset_path):
    """
    Serve the assets.
    """
    return send_from_directory(web_app.simpyt_app.assets_path, asset_path)


@web_app.route("/stop")
def stop():
    """
    Stop Simpyt.
    """
    web_app.simpyt_app.stop()
