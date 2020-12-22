September 2019
==============

September 24 - v19.9
--------------------

.. csv-table:: Module Versions
       :header: "Modules", "Versions"

        ``dyntopo.local``, v19.9

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    bash$ pip install --upgrade dyntopo.local

Features:
^^^^^^^^^

- Now ignoring all but the first line of IOL lock files containing
  multiple lines.

- Fixed failure that occurred when multiple bringup sessions are launched by
  a user at the same time.
