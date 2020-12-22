December 2019
=============

Dec 27 - v19.12
---------------

.. csv-table:: Module Versions
    :header: "Modules", "Versions"

        ``dyntopo.laas``, v19.12

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    bash$ pip install --upgrade dyntopo.laas

Features:
^^^^^^^^^

- max_launch_time_minutes is now respected in cases where reservation can
  take a long time (for example, when bringing up virtual devices on Esxi
  backend server).
