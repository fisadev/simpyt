from threading import Thread
import logging

from flask import Flask, render_template, redirect, send_from_directory, cli, jsonify, request

from pages import Page
from core import Simpyt


web_app = Flask("simpyt")


def initialize_web_app():
    """
    Configure the web app to run in the Simpyt context.
    """
    web_app.pages_cache = {}

    if not Simpyt.current.web_debug:
        web_app.logger.disabled = True
        logging.getLogger('werkzeug').disabled = True
        cli.show_server_banner = lambda *args: None

    return web_app


@web_app.route("/")
def home():
    """
    Home page were we list the available configured pages.
    """
    pages_names = Page.configured_pages()
    return render_template(
        "home.html",
        pages_names=pages_names,
        simpyt=Simpyt.current,
    )


@web_app.route("/page/<string:page_name>")
def page_show(page_name):
    return show_or_edit_page(page_name, edit=False)


@web_app.route("/page/<string:page_name>/edit")
def page_edit(page_name):
    return show_or_edit_page(page_name, edit=True)


@web_app.route("/page/<string:page_name>/controls")
def page_controls(page_name):
    return show_or_edit_page(page_name, edit=False, only_page_controls=True)


def show_or_edit_page(page_name, edit, only_page_controls=False):
    """
    Show a particular page with controls, optionally allowing to edit its config.
    If only_page_controls is True, the response includes only the html part of the page itself,
    to be used when "refreshing" the page in the edit mode.
    """
    try:
        if only_page_controls:
            template_name = "page_controls.html"
        else:
            template_name = "page.html"

        page = Page.read(page_name)
        web_app.pages_cache[page_name] = page

        return render_template(template_name, page=page, edit=edit)
    except Exception as err:
        return render_template("page_error.html", error=str(err),
                               simpyt=Simpyt.current)


@web_app.route("/page/<string:page_name>/code", methods=["GET", "POST"])
def page_code(page_name):
    """
    Load and return the page code, to use in the web editor.
    """
    try:
        if request.method == "GET":
            code = Page.read_code(page_name)

            return jsonify({"code": code})
        elif request.method == "POST":
            payload = request.get_json()
            Page.save_code(page_name, payload["code"])

            return jsonify({"result": "ok"})
    except Exception as err:
        return jsonify({"error": str(err)})


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
