from pathlib import Path
import os
import sys

from core import Simpyt


if __name__ == "__main__":
    # configs placed either in the parent dir of the pyempaq pyz file or the simpyt.py file
    used_executable_dir_path = Path(os.environ.get("PYEMPAQ_PYZ_PATH", __file__)).parent

    simpyt_app = Simpyt(
        root_configs_path=(used_executable_dir_path / "configs").absolute(),
        debug="-d" in sys.argv,
    )
    simpyt_app.run()
