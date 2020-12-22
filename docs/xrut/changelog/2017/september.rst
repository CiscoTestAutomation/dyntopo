September 2017
==============

September 26
------------

.. csv-table:: Module Versions
    :header: "Modules", "Versions"

        ``dyntopo.xrut``, v3.0.4

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    bash$ pip install --upgrade dyntopo.xrut


Features:
^^^^^^^^^

- Raw arguments may now be passed through directly to XR-UT.


September 25
------------

.. csv-table:: Module Versions
    :header: "Modules", "Versions"

        ``dyntopo.xrut``, v3.0.3

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    bash$ pip install --upgrade dyntopo.xrut


Features:
^^^^^^^^^

- Refactoring to support pyATS Kleenex core, which now allows orchestrators
  to auto-generate portions of the clean configuration.  The XR-UT
  orchestrator does not currently use this feature.

- Migration of bringup configuration from the legacy pyATS pre-v3.0.0 format
  has now been deprecated.


September 4
-----------

.. csv-table:: Module Versions
    :header: "Modules", "Versions"

        ``dyntopo.xrut``, v3.0.2


Features:
^^^^^^^^^

- Enhanced to support the ``actual_name`` attribute on a logical interface.

  - This allows users to force the orchestrator to bind a logical interface
    to an explicit interface rather than letting the orchestrator choose the
    actual interface name.
