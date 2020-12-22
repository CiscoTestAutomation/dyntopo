August 2018
===========

August 7 - v4.0.2
-----------------

.. csv-table:: Module Versions
    :header: "Modules", "Versions"

        ``dyntopo.laas``, v4.0.2

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    bash$ pip install --upgrade dyntopo.laas

Features:
^^^^^^^^^

- The topology is now terminated if a terminal state (such as Released)
  is reported by the VmCloud server while waiting for the topology
  to be reserved.
