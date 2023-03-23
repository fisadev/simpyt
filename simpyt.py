from pathlib import Path

from flask import Flask, render_template

from pit import Page, Control
import settings

app = Flask(__name__)
app.page = None


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

    if len(list(settings.PAGES_PATH.glob("*.page"))) == 0:
        print("No pages present, creating an example page")
        Page.example_page().save()

    print("SimPyt initial setup complete! Running server...")
    print()

    app.run(host="0.0.0.0", port=9999, debug=True)


@app.route("/")
def home():
    return render_template("home.html", )


launch_server()
