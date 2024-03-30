# Why?

A few of Simpyt's dependencies don't work in Python 3.11, so Python 3.10 is needed. But new Ubuntus
don't have Python 3.10 anymore.

I tried running Simpyt inside Docker (to be able to use the Python 3.10 Docker image), but that
requires a working X display because of PyAutoGUI. And all the tutorials on how to run things that 
require X inside Docker fail, as the newer Ubuntus either use Wayland or use X in different 
incompatible ways (stuff like X no longer creating the .Xauthority file, etc).

I wasn't able to make that work.

So, to have a working development environment on Ubuntu 23.10, I had to compile Python 3.10 and 
install a couple of extra dependencies:

# Compile and install Python 3.10 from source

sudo apt install wget build-essential libreadline-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev
wget https://www.python.org/ftp/python/3.10.14/Python-3.10.14.tgz
tar xzvf Python-3.10.14.tgz
cd Python-3.10.14
./configure --enable-optimizations
make -j4
sudo make altinstall

# More dependencies

sudo apt install libasound2-dev libjack-dev

# That's it

You can now create a virtualenv with python3.10, and install the requirements_dev.txt to run Simpyt 
locally.
