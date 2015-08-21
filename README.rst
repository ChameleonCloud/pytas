===============================
PyTAS
===============================

Python package for TAS integration

Features
--------

* TODO


Demo
----

Included is a Dockerized IPython Notebook which you can use to play with
PyTAS.

Copy ``docker.env.sample`` to ``docker.env`` and update it with your TAS
API Credentials. Then, run IPython with::

    docker build -t pytas/demo .
    docker run -it --rm -p 8888:8888 --env-file docker.env pytas/demo

Then navigate to http://docker.local:8888/notebooks/demo_0.ipynb in your browser.
The password is ``pytas`` unless you changed it to a different value in ``docker.env``.