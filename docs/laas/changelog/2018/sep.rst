September 2018
==============

September 24 - v4.0.3
---------------------

.. csv-table:: Module Versions
    :header: "Modules", "Versions"

        ``dyntopo.laas``, v4.0.3

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    bash$ pip install --upgrade dyntopo.laas

Features:
^^^^^^^^^

- Now supports LaaS server configured as 'ssh://x.x.x.x' by
  translating to ip=x.x.x.x and protocol=ssh in the device connection
  block.

- Added new n9000v plugin.
