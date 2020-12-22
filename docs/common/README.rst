This package provides a common framework to support
dyntopo orchestrator packages.

Support Mailers
---------------
The `pyATS Support Team`_ would be happy to help you with any
issues relating to this package.

Please consider creating a question under `PieStack`_.

.. _pyATS Support Team: pyats-support@cisco.com
.. _PieStack: http://piestack.cisco.com

Installation
------------

pyATS Installation
^^^^^^^^^^^^^^^^^^

User needs to create an empty directory and inside that new directory
the installation script can be called.

.. code-block:: text

    /auto/pyats/bin/pyats-install

.. note::

    ``--help`` can be used to check installation options

For more information about pyATS
`installation <http://wwwin-pyats.cisco.com/documentation/html/install/install.html>`_
please check the documentation.


Package Installation
^^^^^^^^^^^^^^^^^^^^

Although this package is usually installed automatically when a dyntopo
orchestrator package is installed, it can also be manually installed
from pypi server (using `pip`).

First-time installation steps:

.. code-block:: text

    source env.csh
    pip install dyntopo.common


Steps to upgrade to latest:

.. code-block:: text

    source env.csh
    pip uninstall dyntopo
    pip install --upgrade dyntopo.common


Introduction
============

The ``dyntopo.common`` package defines common infrastructure that users may
find useful when creating their own dynamic topology orchestrator packages
under the pyATS `Bringup Model`_.

.. _Bringup Model: https://wiki.cisco.com/display/PYATS/Kleenex+Bringup+Documentation#KleenexBringupDocumentation-BringupModel

It contains the following components:

- An orchestrator-aware clean yaml loader.
- A logical object model that facilitates actual/logical binding.
- The clean schema for all orchestrators, defining and validating all
  generic and orchestrator-specific keys allowed in the clean YAML file.


.. sectionauthor:: Myles Dear <mdear@cisco.com>
