May 2017
========

May 8
-----

.. csv-table:: Module Versions
    :header: "Modules", "Versions"

        ``dyntopo.laas``, v3.0.0


Features:
^^^^^^^^^

- Initial release (functionality split out from previously released
  base dyntopo package after namespace split).

- Introduced post-reservation busy-wait to work around a known LaaS-NG issue
  CSCvc99732.

- Tuned a vmcloud REST socket timeout parameter after seeing failures to
  launch on native Esxi.

- Now capturing management interface details under the device clean key.

- Now forcing interfaces connected to non-management external links to
  have a type of ``ext``.  This will help some libraries tell the difference
  between interfaces connecting topology devices and interfaces leading to
  the outside world.

- Now excluding management links and all interfaces connected to them from
  appearing in the actual testbed topology.

- Now allowing locally and externally connected links to be designated as
  management links.

- Added ``just_spawned`` key to allow uniclean to differentiate between
  micro (inner) clean and outer (post-bringup) clean.

- Refactored common topology objects in dyntopo and pyATS core to reduce
  duplicated code.
