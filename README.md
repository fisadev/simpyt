# Simpyt

![](docs/idea.png)

# For users: 

Installation instructions and quickstart in the official website: http://simpyt.fisadev.com

# For devs:

You must use Python 3.10 at most, newer versions don't work :(

If you are using a modern Ubuntu, you can install it like this:

    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt-get update
    sudo apt-get install python3.10 python3.10-venv python3.10-dev python3.10-tk


You might also need to install a few extra dependencies in Ubuntu (sorry, don't know how to get these in other OSs):

    sudo apt install pkg-config libasound2-dev libjack-dev


After that, you can install the dependencies. I highly suggest running inside a virtualenv:

    python3.10 -m venv venv
    source venv/bin/activate
    pip install -r requirements_dev.txt


And finally run Simpyt in dev mode:

    python simpyt.py
