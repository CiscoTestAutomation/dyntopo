
.. _vxrbringup:


This `orchestrator`_ is designed to command a
`VXR`_ backend server to bring up and tear down dynamic topologies.

.. _orchestrator: https://wiki.cisco.com/display/PYATS/Kleenex+Bringup+Documentation#KleenexBringupDocumentation-Orchestration

Support Mailers
---------------

.. sidebar:: Quick References

    - `PYVXR`_


.. _VXR: https://wiki.cisco.com/display/VXRSIM/VXR

.. _PYVXR: http://pyvxr.cisco.com/pyvxr

The `VXR Support Team`_ is available to help you with any issues
relating to the `VXR`_ orchestrator and backend.

You may also consider making use of one of the following mailers :
`pyATS Users`_.

.. _VXR Support Team: vxr-dev@cisco.com
.. _pyATS Users: pyats-users@cisco.com

Introduction
------------

VXR Bringup supports virtual device topologies.


Installation
------------

pyATS Installation
^^^^^^^^^^^^^^^^^^

User needs to create an empty directory and inside that new directory
the installation script can be called.

.. code-block:: text

    /auto/pyats/bin/pyats-install

.. note::

    ``--help`` can be used to check installation options

For more information about pyATS
`installation <https://wiki.cisco.com/pages/viewpage.action?pageId=80375302>`_
please check the documentation.


Package Installation
^^^^^^^^^^^^^^^^^^^^

This package can be installed from pypi server(using `pip`)

First-time installation steps:

.. code-block:: text

    source env.csh
    pip install dyntopo.vxr


Steps to upgrade to latest:

.. code-block:: text

    source env.csh
    pip uninstall dyntopo
    pip install --upgrade dyntopo.vxr


Post-Installation Requirements
------------------------------

- Ensure a TCL tree is sourced.
    The reason is because pyATS scripts interact with devices via the abstract
    connection model, and the most robust and complete implementation of this
    model requires a TCL backend.  If you do not have your own TCL
    ATS tree, the default ATS tcl tree may be used, refer to
    `Linking to default ATS tree`_.


- You must have access to a VXR simulation server. If you don't have one,
    you can reserve one of VXR's public server

For more information about VXR public server reservation, please check
the `SLURM <https://wiki.cisco.com/display/VXRSIM/VXR+SLURM>`_ documentation.

- You must have `passwordless SSH`_ enabled.  You must be able to ssh to VXR
  simulation server without being prompted for a password.

.. _passwordless SSH: https://apps.na.collabserv.com/wikis/home/wiki/W52d8c1c91d6a_41eb_a30f_021c10f3ec18/page/Engineering%20Non?interactive%20SSH%20Setup%20Instructions
.. _Linking to default ATS tree: https://wiki.cisco.com/display/PYATS/Activating+Instance#ActivatingInstance-LinkingtodefaultATStree


How to invoke
-------------
In order to select VXR Bringup:

- Specify the following block of text in your
  :ref:`-clean_file <clean_schema>`::

    bringup:
        BringUpWorker:
            module: dyntopo.vxr

- or, specify a value of
  `dyntopo.vxr.BringUpWorker<dyntopo.vxr.worker.BringUpWorker>`
  against the ``-orchestrator`` parameter when instantiating the
  `BringUp<ats.kleenex.bringup_manager.BringUp>` object in
  `standalone bringup`_ mode.

.. _standalone bringup: https://wiki.cisco.com/display/PYATS/Kleenex+Bringup+Documentation#KleenexBringupDocumentation-StandaloneBringup


VXR Virtual Device Orchestration
------------------------------------
Users are able to request a topology of virtual devices which are spun up
as virtual machines (VMs) on the VXR backend and virtually wired together.

Supported virtual platforms
^^^^^^^^^^^^^^^^^^^^^^^^^^^
The following virtual platforms may be requested by specifying the
indicated name in the device ``type`` field of the logical testbed YAML file:

- iosxrv9k
- iosxrv
- asr9k (asr9k lightspeed)
- spitfire_f
- spitfire_d
- ixia (virtual ixia traffic generator)
- spirent (virtual spirrent traffic generator)

.. _vxr_remote_copy:

Remote Image Copy Option
^^^^^^^^^^^^^^^^^^^^^^^^
The ``remote_copy`` option is enabled by default, this means that
all virtual device images are copied to the VXR server and removed
when the topology is torn down.

NOTE: ixia and spirent images will not be copied to the simulation directory
regardless of this flag. The path to ixia and spirent images must be accessible from the simulation directory on the simulation server.

It may be disabled by one of the following means:

- If launching via :ref:`vxr_decoupled_bringup` or
  :ref:`easypy <kleenex_easypy_integration>`.

    - Specifying ``bringup/BringUpWorker/vxr/remote_copy: False`` in your
      clean YAML file,

    - Specifying ``-no_remote_copy`` as a CLI command parameter.

- If launching from a `standalone script <standalone bringup>`_.

    - Specifying ``remote_copy=False`` when constructing the
      `BringUp<ats.kleenex.bringup_manager.BringUp>` object.

For more details, see the :ref:`dyntopo clean schema` and :ref:`schema`.

Management interface
^^^^^^^^^^^^^^^^^^^^
By default, each device has its management interface connected to the
libvirt's default virtual network switch (virbr0) on the simulation server.
The virtual network switch operates in NAT mode (using IP masquerading ).
This means any guests connected through it, use the host IP address for
communication to the outside world, and computers external to the host can't
initiate communications to the guests inside. The virtual network switch has
a range of IP addresses, to be provided to guests through DHCP.

There is no need to explicitly declare a management interface in the logical
topology file. The orchestrator will auto generate a default, platform specific
management interface entry. For example, for asr9k, spitfire, iosxrv,
and iosxrv9k platforms, the generated entry will be:

.. code-block:: yaml

    MgmtEth0/RP0/CPU0/0:
        type: MgmtEth
        alias: mgmt
        link: netboot

YAML inputs for DT workflows
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

VXR Bringup requires a logical testbed YAML file and a clean YAML file
as input.

Please see `YAML inputs for DT workflows`_ for more details.

.. _YAML inputs for DT workflows: https://wiki.cisco.com/display/PYATS/Kleenex+Bringup+Documentation#KleenexBringupDocumentation-YAMLinputsforDTworkflows

See :ref:`dyntopo clean schema` for details on ``dyntopo``-specific
configuration keys that are allowed in the clean YAML file.

See :ref:`dyntopo logical testbed schema` for details on ``dyntopo``-specific
configuration keys that are allowed in the logical testbed YAML file.

.. _vxr logical topology example:

Example Logical Topology Configuration File
"""""""""""""""""""""""""""""""""""""""""""

Here is an example of a testbed configuration file that requests a logical
topology connecting two xrv9k devices via a single link:

.. code-block:: yaml

    devices:
        r1:
            type: iosxrv9k
            logical: True
        r2:
            type: iosxrv9k
            logical: True

    topology:
        r1:
            interfaces:
                if1.0:
                    link: n1
                    type: ethernet
        r2:
            interfaces:
                if2.0:
                    link: n1
                    type: ethernet

YAML output for DT workflows
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Here is an example of the resulting testbed configuration file after
VXR Bringup performs its topology launch and logical-to-actual mapping.
This file contains all the details necessary for pyATS to connect to the
already running topology:

.. code-block:: yaml

    devices:
      r1:
        connections:
          a: {ip: 1.1.1.1, port: 9876, protocol: telnet}
        type: iosxrv9k
        os: iosxr
        series: iosxrv9k

      r1:
        connections:
          a: {ip: 2.2.2.2, port: 9875, protocol: telnet}
        type: iosxrv9k
        os: iosxr
        series: iosxrv9k

    topology:
      r1:
        interfaces:
          GigabitEthernet0/0/0/1:
            link: n1
            type: ethernet

      r2
        interfaces:
          GigabitEthernet0/0/0/1:
            link: n1
            type: ethernet


Content Transfer from Logical to Actual Topology Configuration File
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Custom key/value pairs specified at logical device, link and interface levels
are transferred from the logical to the actual topology configuration file.

.. _vxr_decoupled_bringup:

VXR Decoupled Bringup Tool
------------------------------

The decoupled tool may be used to bring up a dynamic topology and
emit a pyATS-compatible testbed YAML file that allows scripts to
connect with the newly created topology.
Please see `Decoupled Bringup`_ for more details.

.. _Decoupled Bringup: https://wiki.cisco.com/display/PYATS/Kleenex+Bringup+Documentation#KleenexBringupDocumentation-DecoupledBringup

It is possible to specify a user-defined cleaning tool that is automatically
invoked on newly brought up virtual/emulated devices.

Here's an example::

    > vxrbringup -help
    usage: vxrbringup [-testbed_file FILE] [-clean_file FILE]
                       [-clean_devices [DEVICE [DEVICE ...]]] [-loglevel LOGLEVEL]
                       [-logdir DIR] [-no_mail] [-h]

                       [-logical_testbed_file FILE]
                       [-tb_yaml_output_file_name FILE]
                       [-no_remote_copy]


    A tool to perform dynamic topology bringup.

    vxrbringup command line arguments follow.
    Non-recognized args will be ignored (passed-through)

    Examples:
      vxrbringup -logical_testbed_file=/path/to/logical_testbed.yaml -clean_file=/path/to/clean.yaml


Working Examples
----------------

The following example shows how to perform an all-in-one test that performs
the following steps:

   - Brings up a dynamic topology of virtual devices,
   - Runs a sample job that connects to the devices,
   - Tears down the dynamic topology.

.. code-block:: python

   cd examples/dyntopo_vxr
   easypy jobs/connect_test_job.py
   -logical_testbed_file yaml/xrv9k_testbed.yaml
   -clean_file yaml/xrv9k_clean.yaml
   -clean_scope=task

Please see :ref:`vxr logical topology example` for the input logical testbed
file and output actual testbed file contents.

Please refer to the following link for a complete set of working examples :
:download:`vxr_bringup_examples.rst <vxr_bringup_examples.rst.txt>`.


.. _vxr bringup limitations:

Limitations
-----------

- It is only possible for a user to orchestrate one topology at a time
  (multiple topologies raised via
  `task-scope bringup`_ are not supported).

.. _task-scope bringup: https://wiki.cisco.com/display/PYATS/Kleenex+Bringup+Documentation#KleenexBringupDocumentation-easypyBringup
