Nuage VSD Sim
=============
A sample Nuage VSD API simulator with limited to no backend logic

Installation
------------
It is best to install this VSD API Simulator in a virtual Python environment to make sure it does not interfere with your default environment.

Once you created your virtual environment, run the following command

.. code-block::

    $ pip install git+https://github.com/pdellaert/vspk-sim

Configuration
-------------
By default, it will look for a ``config.ini`` file in the ``.nuage-vsd-sim`` folder in your home directory.

If that does not exist, it will look for a ``config.ini`` file in ``/etc/nuage-vsd-sim``.

You can specify your own configuration file using the ``-c /path/to/config.ini`` command line option.

Running the VSD API Simulator
-----------------------------
You can start the Nuage VSD API Simulator by executing

.. code-block::

    $ nuage-vsd-sim


Supported Features
------------------

Supported Headers
~~~~~~~~~~~~~~~~~
* ``X-Nuage-Filter`` - See limitations
* ``X-Nuage-Page``
* ``X-Nuage-PageSize``
* ``X-Nuage-Count`` - Only in response
  
Basic CRUD operations on root level of objects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* ``.get()``
* ``.get_first()``
* ``.fetch()``
* ``.delete()``
* ``.save()``
* ``.create_child()`` - See limitations

Supported entities
~~~~~~~~~~~~~~~~~~
* Enterprise
* Group
* Users

Limitations
~~~~~~~~~~~
* You can use any user information, you will always log in as csproot.
* Filter can only contain a single field and an exact filter, for instance ``'name == "Something"'``.
* No advanced backend functionality is mimicked: If you create an entity, it will not automatically do the same things it would in a real VSD.

  Example: Creating an Enterprise will not automatically create the Administrator (or other) groups

