September 2019
==============

Sep 24 - v19.9
--------------

.. csv-table:: Module Versions
    :header: "Modules", "Versions"

        ``dyntopo.laas``, v19.9

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    bash$ pip install --upgrade dyntopo.laas

Features:
^^^^^^^^^

- Websocket events from a LaaS server that do not contain a booking ID
  are now silently ignored.
