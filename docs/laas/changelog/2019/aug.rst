August 2019
===========

Aug 27 - v19.8
--------------

.. csv-table:: Module Versions
    :header: "Modules", "Versions"

        ``dyntopo.laas``, v19.8

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    bash$ pip install --upgrade dyntopo.laas

Features:
^^^^^^^^^

- Improved retry/recovery behavior when connection to LaaS server is lost
  while waiting for a reservation.

- Now a release is being done when tearing down pure virtual topologies,
  as this is now the expectation of reservation-capable LaaS servers.

- Now supports generation of new-style credentials.
