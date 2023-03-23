from pathlib import Path

from flask import Flask, render_template

from pit import Pit, Control
import settings

app = Flask(__name__)
app.pit = None


def launch_server():
    """
    Do some global health checks and ensure we have everything we need, and then run the server.
    """
    if not settings.CONFIGS_PATH.exists():
        print("No configs directory, creating an empty one")
        settings.CONFIGS_PATH.mkdir()

    if not settings.IMAGES_PATH.exists():
        print("No images directory, creating an empty one")
        settings.IMAGES_PATH.mkdir()

    if len(list(settings.CONFIGS_PATH.glob("*.pit"))) == 0:
        print("No configs present, creating a example config")
        Pit.example_pit().save()

    print("SimPyt initial setup complete! Running server...")
    print()

    app.run(host="0.0.0.0", port=9999, debug=True)


@app.route("/")
def home():
    return render_template("home.html", )


launch_server()
