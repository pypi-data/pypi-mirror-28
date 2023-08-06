Lemming
#######

Generates the structure needed for a Python 3 project. Includes helpers for licenses and testing frameworks.

Installation
============

To install this software:

.. code-block:: bash

    $ pip install lemming

Usage
=====

The first time that you run lemming, you should execute the following:

.. code-block:: bash

    $ lemming config

it'll write ``.lemming.yml`` to your ``$HOME`` directory, which you can edit to automatically populate templates
with your details for all future runs.

That file looks as follows:

.. code-block:: yaml

    ---
    lemming:
      author: Paul Stevens
      author_email: no-reply@xnode.co.za
      license:
        type: MIT

To use `lemming` to generate a project:

.. code-block:: bash

    $ lemming <project_name>

This obviously means that you can never name a project ``config``...

The default license is the MIT license (rude, but this is the one that I use the most.) The other two choices are:

* Apache 2.0
* BSD 2-clause license

To select the APACHE license for your project:

.. code-block:: bash

    $ lemming testprog --license apache

To select the BSD 2-clause license for your project:

.. code-block:: bash

    $ lemming testprog --license bsd

Note
----

Currently supported licenses are:

* MIT (default)
* Apache 2.0
* BSD 2-clause license

Copyright
=========

Copyright 2017 Paul Stevens.

License
=======

Licensed under the MIT License. See LICENSE for details.
