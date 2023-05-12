.. _laasv2bringup:

This `orchestrator`_ was designed to bring up and tear down dynamic topologies on `LaasV2 <http://laasv2.cisco.com>`_.

.. _orchestrator: https://wiki.cisco.com/display/PYATS/Kleenex+Bringup+Documentation#KleenexBringupDocumentation-Orchestration

For support and feedback, please contact the pyATS team by opening a ticket on `Piestack <http://piestack.cisco.com>`_

Installation Instructions
-------------------------

pyATS Installation
^^^^^^^^^^^^^^^^^^

Instructions on how to install pyATS can be found `here <http://wwwin-pyats.cisco.com/documentation/html/install/install.html>`_.

Package Installation
^^^^^^^^^^^^^^^^^^^^

The dyntopo package can be installed from the pypi server (via `pip install`)

.. code-block:: text

    source env.csh
    pip install dyntopo.laasv2

To upgrade to the latest version:

.. code-block:: text

    source env.csh
    pip uninstall dyntopo
    pip install --upgrade dyntopo.laasv2

How to invoke
-------------

In order to select LaaSv2 Bringup:

- Specify the following block of text in your
  :ref:`-clean_file <clean_schema>`::

.. code-block:: yaml

    bringup:
        BringUpWorker:
            module: dyntopo.laasv2

You should also pass a `laasv2` arguments to `bringup`. This argument accepts the following arguments:

- **domain:** The domain ID (obtained from LaaSv2).
- **reservation_duration_hours:** The duration of the reservation (in hours). Defaults to 8 hours.

Below, you can find an example of how the `bringup` block could be declared:

.. code-block:: yaml

  bringup:
    BringUpWorker:
      module: dyntopo.laasv2
      laasv2:
        domain: 0a1b20cd-...
        reservation_duration_hours: 8

For more details on other arguments that can be passed to `bringup`, see the :ref:`dyntopo clean schema` and :ref:`schema`.

LaaSv2 Device Orchestration
---------------------------
Users can provide a virtual topology specification by passing a path to a yaml file to the `--logical_testbed` argument when running pyats.

Logical Testbed
^^^^^^^^^^^^^^^
This file describes a topology (devices, links, and interfaces) that will be used by LaaSv2 to create a topology using devices from a cloud-based pool (`domain`) as long as these devices meet the topology requirements.
All devices in the topology must have the `logical` attribute set to ``True``. You can find examples of logical testbed files here: :ref:`_laasv2_example`.

Supported Device Types
^^^^^^^^^^^^^^^^^^^^^^
To specify the device type for a given device in a topology, you just need to add the `type` argument to the device in the logical testbed file.
Examples of device types supported are:

- iosxe
- isr4k
- cat9k

Before requesting a topology, it is recommended to check which devices (and device types) are available in your lab domain.

Supported Links
^^^^^^^^^^^^^^^
LaaSv2 allows users to configure the link between devices in a topology. To do this, you need to declare a link in the `topology`, under `links`.

The following arguments can be passed:

- **type:** connection type. Accepted values are: ``QINQ``, ``ACI_L1``, ``ACI_L2``, ``STATIC``
- **tunnel_cdp:** Accepted values are ``true`` or ``false``.
- **vlan_policy:** Accepted values are ``auto_assign`` and ``vlan_range``. Defaults to auto assign.
- **port_mode:** Supported modes are: ``access_mode`` and ``trunk_mode``
- **vlan_range:** If ``port_mode`` is ``access_mode``, then a single value should be provided. If ``trunk_mode``, then a range (e.g. "2000-300") should be provided.

Reserving Specific Devices
^^^^^^^^^^^^^^^^^^^^^^^^^^
It is possible to request specific devices for your topology. To do that, simply add the attribute `device_id` to the device declaration in your logical testbed.
The ID has to match an existing device ID in LaaSv2.
For example:

.. code-block:: yaml

  devices:
    r1:
      device_id: 0d1x2a34...

.. note::
    Make sure that the device is currently not being used by any other reservation as you will not be able to reserve a device that is already reserved.

.. _laasv2_example:
Examples
^^^^^^^^
The following logical testbed YAML snippet is an example of a topology with two cat9k devices (``r1`` and ``r2``) that share a link. 
Note how both devices have interfaces that contain a link attribute pointing to the same link name.

.. code-block:: yaml

  devices:
    r1:
      type: cat9k
      os: iosxe
      logical: True
    r2:
      type: cat9k
      os: iosxe
      logical: True
  topology:
    links:
      n1:
        type: QINQ
        tunnel_cdp: true
        vlan_policy: auto_assign
    r1:
      interfaces:
        if1.1:
          link: n1
          type: ethernet
    r2:
      interfaces:
        if2.1:
          link: n1
          type: ethernet

.. note::
    All interfaces containing a ``link`` annotation are connected to a link with the same name.

.. note::
    The interface and device names will be used as aliases as the names will depend on which devices were reserved.

.. note::
    The orchestrator assigns a source device and interface, and a destination device and interface nodes to the link according to the order in which the devices and interfaces were declared.

In this next example, the topology is created with two isr4k devices using different link settings. ``n1`` is a QinQ link with a VLAN rage.

.. code-block:: yaml

  devices:
    r1:
      type: isr4k
      os: iosxe
      logical: True
    r2:
      type: isr4k
      os: iosxe
      logical: True
  topology:
    links:
      n1:
        type: QINQ
        vlan_policy: trunk_mode
        vlan_range: 2000-3000
    r1:
      interfaces:
        if1.1:
          link: n1
          type: ethernet
    r2:
      interfaces:
        if2.1:
          link: n1
          type: ethernet

Running pyats clean
-------------------

As previously mentioned, one of the possible ways to create a topology and run tests over it is to run ``pyats clean``.
pyATS Clean expects a clean YAML file and a logical testbed YAML file. 

Once the topology is requested, it will make a reservation of the topology and return the merged testbed YAML file (named ``merged_testbed.yaml``) in the current working directory.
This file can be used to run other tests, like interacting with the devices using ``pyats shell``, for example.
pyATS Clean will halt its execution waiting for the user to press ``Ctrl + C`` to delete the reservation and free the resources.
Below you can find an example of how to use pyATS clean:

.. code-block:: text

    pyats clean -logical_testbed_file logical_tb.yaml --clean-file clean.yaml

Running pyats run job
---------------------

If you are only interested in bringing up a topology for a single job run, you can do that using ``pyats run job``.
pyATS will expect the same arguments, i.e., a clean YAML file and a logical testbed YAML file.

Once the topology is requested, it will make a reservation of the topology, create the merged testbed YAML file (named ``merged_testbed.yaml``) in the current working directory.
The difference this time, is that the execution will not be halted. pyATS will use the merged testbed to connect to the devices and use the job script to interact with the topology.
Below you can find an example of how to use pyATS run job:

.. code-block:: text

    pyats run job job.py --clean-file clean.yaml --logical-testbed logical_tb.yaml

.. note::
    Note how this alternative requires a job script. If you need more information on how to run jobs using pyATS, please refer to `pyATS documentation <https://developer.cisco.com/docs/pyats/>`_.

Limitations
-----------

- Currently, it is not possible to determine the capability of a link via logical testbed YAML file yet. An enhancement will be made to support this feature.
