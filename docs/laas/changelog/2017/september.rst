September 2017
==============

September 25
------------

.. csv-table:: Module Versions
    :header: "Modules", "Versions"

        ``dyntopo.laas``, v3.0.4

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    bash$ pip install --upgrade dyntopo.xrut


- Refactoring to support pyATS Kleenex core, which now allows orchestrators
  to auto-generate portions of the clean configuration.  The LaaS
  orchestrator does not currently support this feature.

- Migration of bringup configuration from the legacy v1.0.0 format
  has now been deprecated.


September 4
-----------

.. csv-table:: Module Versions
    :header: "Modules", "Versions"

        ``dyntopo.laas``, v3.0.3


Features:
^^^^^^^^^

- Added port_channel link option.

- Users may now request multiple line cards on multinode platforms such as
  iosxrv using the ``actual_name`` attribute of a logical interface.
