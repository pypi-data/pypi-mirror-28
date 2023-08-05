Simple bootstraping of python scripts
=====================================

This is an early prototype of a simple bootstrapping system for python. By
importing `scriptstrap` into a python script, a virtual environment ("venv")
will be automatically created, dependencies installed (using `pip`) and the
script will finally be re-launched inside the venv. This simplifies
distribution of small utility scripts, as package dependencies are
automatically manged by just running the script.

The intended use case for `scriptstrap` is single-file utility scripts only!

Features
--------

- Automatic creation of virtual environment for each script
- Dependencies are installed and imported automatically
- Simplified script distribution
- No additional dependencies other than python and virtualenv

Requirements
------------

* Python 2.7 or later
* virtualenv

Getting started
---------------

You must do a global install of `scriptstrap` or run it from another
venv. Recommended installation is::

    $ pip install scriptstrap

Example
-------

Simple script that downloads the Google main page and prints it:

.. code:: python

    import scriptstrap

    scriptstrap.python3('requests')

    print(requests.get('http://google.com').content)

Running the script, assuming the script is called `requests.py`, will create
a new venv in a directory called `requests.venv3` next to the script. If the
script is launched again, the same venv will be re-used.
