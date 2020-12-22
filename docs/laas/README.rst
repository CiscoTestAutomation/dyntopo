
.. _laasngbringup:


This `orchestrator`_ is designed to command a
`LaaS`_ backend server to bring up and tear down dynamic topologies.

.. _orchestrator: https://wiki.cisco.com/display/PYATS/Kleenex+Bringup+Documentation#KleenexBringupDocumentation-Orchestration


Support Mailers
---------------

.. sidebar:: Quick References

    - `LaaS`_
    - `XRVR`_


.. _LaaS: http://wiki.cisco.com/display/LAAS/LaaS
.. _XRVR: http://wiki.cisco.com/display/REFPLATS/XRVR+Reference+Platform



The `LaaS-NG Support Team`_ is available to help you with any issues
relating to the `LaaS`_ backend.

The `pyATS Support Team`_ would be happy to help you with any
issues relating to the dyntopo LaaS orchestrator.

Please consider creating a question under `PieStack`_.

You may also consider making use of one of the following mailers :
`pyATS Users`_, `LaaS Users`_, `VmCloud DT Users`_.

.. _pyATS Support Team: pyats-support@cisco.com
.. _LaaS-NG Support Team: vmcloud-dev@cisco.com
.. _pyATS Users: pyats-users@cisco.com
.. _LaaS Users: laas-users@cisco.com
.. _VmCloud DT Users: vmcloud-dt@cisco.com
.. _PieStack: http://piestack.cisco.com


Introduction
------------

LaaS-NG Bringup supports hardware-based and/or virtual device topologies.


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
`installation <http://wwwin-pyats.cisco.com/documentation/html/install/install.html>`_
please check the documentation.


Package Installation
^^^^^^^^^^^^^^^^^^^^

This package can be installed from pypi server(using `pip`)

First-time installation steps:

.. code-block:: text

    source env.csh
    pip install dyntopo.laas


Steps to upgrade to latest:

.. code-block:: text

    source env.csh
    pip uninstall dyntopo
    pip install --upgrade dyntopo.laas


Post-Installation Requirements
------------------------------

- Ensure a TCL tree is sourced.
    The reason is because pyATS scripts interact with devices via the abstract
    connection model, and the most robust and complete implementation of this
    model requires a TCL backend.  If you do not have your own TCL
    ATS tree, the default ATS tcl tree may be used, refer to
    `Linking to default ATS tree`_.

- You must have `passwordless SSH`_ enabled.  You must be able to ssh to your
  LaaS server without being prompted for a password.

- If using a public LaaS server VM, please consider disabling
  the :ref:`remote copy<laas_remote_copy>` option whenever possible,
  as these VMs come with automount capabilities already turned on.

- If you have a private LaaS server,

  - Here are a few ways you could provide passwordless access:

    - Install  Vintella_  (this requires a call to the help desk to do
      pre-setup)

    - Or, if you don't want to intall Vintella and support only local admin
      user access, create a private key for the admin user and have each user
      needing to launch topologies on the server import the key.  For example:

      .. code-block:: bash

         scp lab@<hostname>:.ssh/id_rsa-lab ~/.ssh

         # Then, add the following text into your home directory under ~/.ssh/config:
           Host <hostname>
               User lab
               IdentityFile ~/.ssh/id_rsa-lab


  - Consider installing the automounter.  This will allow you to disable the
    :ref:`remote copy<laas_remote_copy>` option in most cases and save time
    by allowing LaaS to access virtual device images directly.

.. _passwordless SSH: https://apps.na.collabserv.com/wikis/home/wiki/W52d8c1c91d6a_41eb_a30f_021c10f3ec18/page/Engineering%20Non?interactive%20SSH%20Setup%20Instructions

.. _Vintella: https://wiki.cisco.com/display/ECBU/Ubuntu+Vintela+Migration

.. _Linking to default ATS tree: https://wiki.cisco.com/display/PYATS/Activating+Instance#ActivatingInstance-LinkingtodefaultATStree


How to invoke
-------------
In order to select LaaS-NG Bringup, either:

- Invoke the :ref:`laasng_decoupled_bringup`

- or, specify the following block of text in your
  :ref:`-clean_file <clean_schema>`::

    bringup:
        BringUpWorker:
            module: dyntopo.laas

- or, specify a value of
  `dyntopo.laas.BringUpWorker<dyntopo.laas.worker.BringUpWorker>`
  against the ``-orchestrator`` parameter when instantiating the
  `BringUp<ats.kleenex.bringup_manager.BringUp>` object in
  `standalone bringup`_ mode.

.. _standalone bringup: https://wiki.cisco.com/display/PYATS/Kleenex+Bringup+Documentation#KleenexBringupDocumentation-StandaloneBringup



LaaS-NG Virtual Device Orchestration
------------------------------------
Users are able to request a topology of virtual devices which are spun up
as virtual machines (VMs) on the LaaS backend and virtually wired together.

Supported virtual platforms
^^^^^^^^^^^^^^^^^^^^^^^^^^^
The following virtual platforms may be requested by specifying the
indicated name in the device ``type`` field of the logical testbed YAML file:

- iosv
- iosv_pagent
- nxosv
- n9000v
- iosxrv (simplex, multinode or HA)
- iosxrv9k
- csr1000v

.. _laas_remote_copy:

Remote Copy Option
^^^^^^^^^^^^^^^^^^
The ``remote_copy`` option is enabled by default, this means that
all virtual device images are copied to the LaaS server and removed
when the topology is torn down.

It may be disabled by one of the following means:

- If launching via :ref:`laasng_decoupled_bringup` or
  :ref:`easypy <kleenex_easypy_integration>`.

    - Specifying ``bringup/BringUpWorker/laas/remote_copy: False`` in your
      clean YAML file,

    - Specifying ``-no_remote_copy`` as a CLI command parameter.

- If launching from a `standalone script <standalone bringup>`_.

    - Specifying ``remote_copy=False`` when constructing the
      `BringUp<ats.kleenex.bringup_manager.BringUp>` object.


If ``remote_copy`` option is enabled, additional configurations may be
specified in the logical testbed YAML file.

- You may optionally create a logical testbed VmCloud server block
  that looks like this::

    testbed:
        servers:
            <vmcloud_server_name>:
                type: laas
                username: # <name of user to use to log into server>
                          # If not specified, no username is used for
                          # remote ssh login and secure copy.  Default
                          # ssh settings are used instead.
                image_dir: # <name of server-local directory to copy images to>


For more details, see the :ref:`dyntopo clean schema` and :ref:`schema`.

External Access
^^^^^^^^^^^^^^^
Sometimes a script needs to connect to a launched virtual device via
inband IP (for example, when interacting with the device via NETCONF/YANG).

External access to a named interface on a LaaS server may be achieved
in several ways:

- Dedicated management external access : It is possible to expose the dedicated
  management interface of platforms such as NX/XR to devices outside the
  orchestrator's scope of control.  One example could be to enable users
  to initiate inband connections to virtual devices to perform
  YANG-based testing.
  The following clean YAML snippet shows a request to connect all such
  interfaces in the current topology to the default external interface::

   bringup:
       BringUpWorker:
           module: dyntopo.laas
           laas:
               vmcloud_server: <server_name>
               ext_itf:
                   mgt: True


- Inband external access : It is possible to annotate any link in the topology
  having at least one interface connected to it as having an external
  connection.  This allows orchestrated devices to interact with devices outside
  the orchestrator's scope of control.  Some examples could be having
  virtual devices access a centralized certificate server, or enabling
  users to initiate inband connections to virtual devices to perform
  YANG-based testing.
  The following logical testbed YAML snippet assumes devices R1 and R2
  do not have a dedicated management interface (ie. they could be XE devices).
  It shows a request to connect the management link ``_mgt_subnet``
  to the default external interface and link ``r1r2_ext``
  to the external interface ``eth3``::

    devices:
        R1:
            type: <virtual_platform_type>
            logical: True

        R2:
            type: <virtual_platform_type>
            logical: True

    topology:
        links:
            _mgt_subnet:
                ext_itf:
                mgt: True

            r1r2_ext:
                ext_itf:
                    name: eth3

        R1:
            interfaces:
                _r1_mgt:
                    link: _mgt_subnet
                    type: ethernet

                r1_1
                    link: r1r2_ext
                    type: ethernet

                r1_2
                    link: r1r2
                    type: ethernet

        R2:
            interfaces:
                _r2_mgt:
                    link: _mgt_subnet
                    type: ethernet

                r2_1
                    link: r1r2_ext
                    type: ethernet

                r2_2
                    link: r1r2
                    type: ethernet

.. note::
    All interfaces connected to a link having an ``ext_itf`` annotation
    are instead connected to a new autogenerated link named after the
    the external interface being connected to.
    Thus, the original user-specified topology is maintained and extended
    with the new external connection.

.. note::
    Management links and the interfaces connected to them
    never appear in the actual testbed topology.

.. note::
    The orchestrator writes the managment interface name of the device
    into the ``clean/mgt_itf/name`` key in the actual testbed configuration
    as described in the :ref:`dyntopo actual testbed schema`.

.. note::
    Although the management link and interfaces may be given any name,
    they are shown here starting with an underscore to emphasize that
    they are not exposed to the user in the actual topology.

.. note::
    The orchestrator assigns a type of ``ext`` to interfaces connected to
    non-management external links to ensure they are not confused
    with interfaces connecting topology devices.  The actual interfaces that
    bind with logical interfaces ``r1_1`` and ``r2_1`` in the above example
    would be given this special type.


An external interface is modelled as a shared resource that any topology
requesting external access may connect to.

On a public LaaS server, the default external access interface is connected
to the corporate intranet.  A DHCP server is reachable via this interface
and can grant corporate-routable addresses to any device with DHCP client
capability.

For more details, see the ``ext_itf`` key in the :ref:`dyntopo clean schema`
and the :ref:`dyntopo logical testbed schema`.


Managment Links Without External Access
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It is also possible to designate a link to be a managment link and ensure that
it doesn't appear in the actual testbed topology.  This works for both platforms
with dedicated management interfaces (such as XR and NX) and those without
(such as IOSXE).  The management interface is populated as described in the
:ref:`dyntopo actual testbed schema`. ::

    devices:
        R1:
            type: <virtual_platform_type>
            logical: True

        R2:
            type: <virtual_platform_type>
            logical: True

    topology:
        links:
            _mgt_subnet:
                mgt: True

        R1:
            interfaces:
                _r1_mgt:
                    link: _mgt_subnet
                    type: ethernet

                r1_1
                    link: r1r2
                    type: ethernet

        R2:
            interfaces:
                _r2_mgt:
                    link: _mgt_subnet
                    type: ethernet

                r2_1
                    link: r1r2
                    type: ethernet

.. note::
    Although the management link and interfaces may be given any name,
    they are shown here starting with an underscore to emphasize that
    they are not exposed to the user in the actual topology.


LaaS-NG Hybrid Device Orchestration
-----------------------------------
Users are also able to request a hybrid topology consisting of
interconnected virtual and physical devices.


LaaS-NG Physical Device Orchestration
-------------------------------------
Users are able to reserve hardware devices from cloud-based pools
called *domains*.

LaaS-NG Bringup is able to reserve topologies of hardware devices
from a particular cloud-based domain,
and can virtually wire them together according to a topology you specify.

.. _laasng profile hierarchy:

LaaS-NG Hardware Domain Profile Hierarchy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The lab manager of every LaaS-NG domain organizes the domain's devices into a
hierarchy of names.  As we'll see a little later, the user is able to request
logical devices under any level of the hierarchy.

For example, the following command shows that the device ``c2921-1`` is under
the ``ISR`` category, while the devices ``c3745-2`` and ``c3745-1``
are under both the ``ISR/3700`` and ``ISR`` categories.


::

    my_laas_server> vmcloud profiles -D vmcloud-dev
    Listing Profile Devices: SUCCESS
    - ISR
        c2921-1 (free)
    ----- 3700
            c3745-2 (free)
            c3745-1 (free)



LaaS-NG Bringup User Role
-------------------------

Only the DT role is supported.
Please refer to `User Roles` for more details.

.. _User Roles: https://wiki.cisco.com/display/PYATS/Kleenex+Bringup+Documentation#KleenexBringupDocumentation-UserRoles


YAML inputs for DT workflows
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

LaaS-NG Bringup requires a logical testbed YAML file and a clean YAML file
as input.

Please see `YAML inputs for DT workflows`_ for more details.

.. _YAML inputs for DT workflows: https://wiki.cisco.com/display/PYATS/Kleenex+Bringup+Documentation#KleenexBringupDocumentation-YAMLinputsforDTworkflows

See :ref:`dyntopo clean schema` for details on ``dyntopo``-specific
configuration keys that are allowed in the clean YAML file.

See :ref:`dyntopo logical testbed schema` for details on ``dyntopo``-specific
configuration keys that are allowed in the logical testbed YAML file.

If the user defines in their logical topology interfaces of type ``loopback``
or having a name containing the string ``loopback`` (case insensitive),
these interfaces are transferred directly over to the actual topology and are
not sent for orchestration.

By default, all links are L2 (meaning that a L2 switch is used to provision
the requested topology).  However, it is possible to request a link to be L1,
which means the link is provisioned using an L1 switch).   Various speed and
media options may be requested for L1 links
(please see :ref:`dyntopo logical testbed schema` for details).


.. _laasng logical topology example:

Example Logical Topology Configuration File
"""""""""""""""""""""""""""""""""""""""""""

Here is an example of a testbed configuration file that requests a logical
topology connecting two available devices under the "3700" category
via a single link (see :ref:`laasng profile hierarchy` for details):

.. code-block:: yaml

    devices:
        r1:
            type: 3700
            logical: True
            custom:
                r1_custom_key: r1_custom_value
        r2:
            type: 3700
            logical: True

    topology:
        links:
            n1:
                custom_link_n1_key: custom_link_n1_value
        r1:
            interfaces:
                if1.1:
                    link: n1
                    type: ethernet
                    custom_key_for_if1.1: custom_value_for_if1.1
        r2:
            interfaces:
                if2.1:
                    link: n1
                    type: ethernet

Semantics of the logical device type field
""""""""""""""""""""""""""""""""""""""""""
The previous example used the device ``type`` field to request the category
from which to reserve the device.  We could have also used a non-leaf
category such as ``ISR``, which would have expanded the set of potentially
reservable devices.  For example, one of the logical devices may have been
bound to the actual ``c2921-1`` device, which is under the ``ISR`` category
but not under the ``3700`` category.

YAML output for DT workflows
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Here is an example of the resulting testbed configuration file after
LaaS-NG Bringup performs its topology launch and logical-to-actual
mapping.  Note that the device names reflect the actual devices chosen,
but the original logical device and interface names are preserved
through the use of aliases.  This file contains all the details necessary
for pyATS to connect to the already running topology:

.. code-block:: yaml

    devices:
      c3745-1:
        alias: r1
        connections:
          a: {ip: 1.1.1.1, port: 9876, protocol: telnet}
        type: router
        clean:
            mgt_itf:
                name: GigabitEthernet0/0
                ipv4:
                    address: 2.2.2.2
                    gateway_address: 2.2.2.1
                    net:
                        mask: 255.255.255.0
                        prefixlen: 24

        r1_custom_key: r1_custom_value

      c3745-2:
        alias: r2
        connections:
          a: {ip: 2.2.2.2, port: 9875, protocol: telnet}
        type: router
        clean:
            mgt_itf:
                name: GigabitEthernet0/0
                ipv4:
                    address: 3.3.3.3
                    gateway_address: 3.3.3.1
                    net:
                        mask: 255.255.255.0
                        prefixlen: 24

    topology:
        links:
            n1:
                custom_link_n1_key: custom_link_n1_value
      c3745-1:
        interfaces:
          GigabitEthernet0/1:
            alias: if1.1
            link: n1
            type: ethernet
            custom_key_for_if1.1: custom_value_for_if1.1

      c3745-2:
        interfaces:
          GigabitEthernet0/1: {alias: if2.1, link: n1, type: ethernet}


Content Transfer from Logical to Actual Topology Configuration File
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

The example just given shows custom key/value pairs being specified at logical
device, link and interface levels.  This content is transferred from the logical
to the actual topology configuration file.

Also, in the event of a collision between user-specified
logical testbed configuration content and orchestrator-autogenerated content,
the user-specified content is always applied,
the orchestrator's content is overwritten, and a warning is given.

Please see `How Actual Testbed Configuration is Built`_ for more details.

.. _How Actual Testbed Configuration is Built: https://wiki.cisco.com/display/PYATS/Kleenex+Bringup+Documentation#KleenexBringupDocumentation-HowActualTestbedConfigurationisBuilt


.. _laasng_decoupled_bringup:

LaaS-NG Decoupled Bringup Tool
------------------------------

The decoupled tool may be used to bring up a dynamic topology and
emit a pyATS-compatible testbed YAML file that allows scripts to
connect with the newly created topology.
Please see `Decoupled Bringup`_ for more details.

.. _Decoupled Bringup: https://wiki.cisco.com/display/PYATS/Kleenex+Bringup+Documentation#KleenexBringupDocumentation-DecoupledBringup

It is possible to specify a user-defined cleaning tool that is automatically
invoked on newly brought up physical devices.

The value of parameter ``bringup_log_level`` may be specified
either in UPPERCASE or lowercase.

Here's an example::

    > laasbringup -help
    usage: laasbringup [-testbed_file FILE] [-clean_file FILE]
                       [-clean_devices [DEVICE [DEVICE ...]]] [-loglevel LOGLEVEL]
                       [-logdir DIR] [-no_mail] [-h]

                       [-bringup_log_level {debug,info,warning,error,critical}]
                       [-logical_testbed_file FILE]
                       [-tb_yaml_output_file_name FILE]
                       [-tb_virl_request_output_file_name FILE]
                       [-max_launch_time_minutes MINUTES]
                       [-vmcloud_server VMCLOUD_SERVER]
                       [-vmcloud_port VMCLOUD_PORT]
                       [-vmcloud_notification_port VMCLOUD_NOTIFICATION_PORT]
                       [-lab_domain LAB_DOMAIN]
                       [-max_lifetime_minutes MAX_LIFETIME_MINUTES]
                       [-vmcloud_image_dir VMCLOUD_IMAGE_DIR]
                       [-vmcloud_username VMCLOUD_USERNAME] [-no_remote_copy]


    A tool to perform dynamic topology bringup and/or physical device clean.

    laasbringup command line arguments follow.
    Non-recognized args will be ignored (passed-through)

    Examples:
      laasbringup -testbed_file=/path/to/testbed.yaml -clean_file=/path/to/clean.yaml
      laasbringup -logical_testbed_file=/path/to/logical_testbed.yaml -clean_file=/path/to/clean.yaml

    --------------------------------------------------------------------------------

    Testbed:
      -testbed_file FILE    Testbed YAML file.

    Clean:
      -clean_file FILE      YAML File containing clean/bringup configuration details.
      -clean_devices [DEVICE [DEVICE ...]]
                            Specify list of devices to clean

    Logging:
      -loglevel LOGLEVEL    kleenex logging level.
                            eg: -loglevel='INFO'
      -logdir DIR           Directory to save kleenex logs
                            default to current working directory.

    Bringup Notification options:
      -no_mail              Disable sending email on abort.

    Help:
      -h, -help             show this help message and exit


    Bringup Logging options:
      -bringup_log_level {debug,info,warning,error,critical}
                            Logging level for the bringup module.

    Bringup pyATS Integration options:
      -logical_testbed_file FILE
                            User-specified testbed configuration that may contain
                            actual static device configuration and logical device
                            constraints. Logical devices are placeholders for
                            actual devices.
      -tb_yaml_output_file_name FILE
                            The name of the synthesized pyATS testbed YAML file
                            that is created after a topology has been launched.

    LaaS pyATS integration options:
      -tb_virl_request_output_file_name FILE
                            A copy of the VIRL file used to reserve and/or create
                            the topology on the LaaS server is written to this
                            location.
      -max_launch_time_minutes MINUTES
                            How long before the topology is automatically torn
                            down if the launch in progress has not yet completed.

    LaaS server options:
      -vmcloud_server VMCLOUD_SERVER
                            VmCloud server to use.
      -vmcloud_port VMCLOUD_PORT
                            VmCloud server port to send requests to.
      -vmcloud_notification_port VMCLOUD_NOTIFICATION_PORT
                            VmCloud server port to get reservation notifications
                            from.
      -lab_domain LAB_DOMAIN
                            All requested logical physical devices come from this
                            lab domain.
      -max_lifetime_minutes MAX_LIFETIME_MINUTES
                            How long before topology is automatically torn down by
                            the VmCloud server.
      -vmcloud_image_dir VMCLOUD_IMAGE_DIR
                            Server-local destination directory for VmCloud image
                            copy, when -remote_copy is True. Defaults to /tmp.
      -vmcloud_username VMCLOUD_USERNAME
                            Use this username when logging onto the VmCloud server
                            when -remote_copy is specified as True.

    Image options:
      -no_remote_copy       Do not copy virtual images to local storage on the
                            LaaS server.


Working Examples
----------------

The following example shows how to perform an all-in-one test that performs
the following steps:

   - Brings up a dynamic topology of physical devices,
   - Runs a sample job that connects to the devices,
   - Tears down the dynamic topology.

.. code-block:: python

   cd examples/dyntopo_laas
   easypy jobs/connect_test_job.py
   -logical_testbed_file yaml/ios_connect_test_config.yaml
   -clean_file yaml/ios_connect_bringup_config.yaml
   -clean_scope=task

The job file has the following contents:

.. code-block:: python

    import os, sys
    from ats.easypy import run
    def main():
        test_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        testscript = os.path.join(test_path, 'tests', 'connect_test.py')

        run(testscript=testscript, uut1_name='r1', uut2_name='r2')

Please see :ref:`laasng logical topology example` for the input logical testbed file and
output actual testbed file contents.

The clean file has the following contents:

.. code-block:: python

    bringup:
        BringUpWorker:
            module: dyntopo.laas
            log_level: debug
            laas:
                lab_domain: vmcloud-dev
                vmcloud_server: ssr-vmc-01
                max_lifetime_minutes: 60


Please refer to the following link for a complete set of working examples :
:download:`laas_bringup_examples.rst <laas_bringup_examples.rst.txt>`.



LaaS-NG Bringup's Multiprocessing Model
---------------------------------------

Please see `Multiprocessing Model`_ for more details.

.. _Multiprocessing Model: https://wiki.cisco.com/display/PYATS/Kleenex+Bringup+Documentation#KleenexBringupDocumentation-MultiprocessingModel

LaaS-NG Bringup always launches its in its own subprocess.
This is done to ensure that a dynamic topology is always gracefully torn down
if interrupted via a signal or by the user hitting ``<Control><C>``.

LaaS-NG Bringup supports both task and job scopes
(see `easypy Bringup`_ for details).

.. _easypy Bringup: https://wiki.cisco.com/display/PYATS/Kleenex+Bringup+Documentation#KleenexBringupDocumentation-easypyBringup




Many processes are created when LaaS-NG Bringup is selected as part of an
easypy run (please see `async_index` for more details).

.. note::
    The name of the forked LaaS-NG bringup worker process contains the name
    of its worker class
    `dyntopo.laas.BringUpWorker<dyntopo.laas.worker.BringUpWorker>`.

For each newly spawned virtual router, an additional subprocess may be
created to bring it to a testable state.  A separate log file is created
for each of these subprocesses and contains the name ``DeviceLaunch``.

.. _LaaS bringup Governance Model:

Governance
----------
- `LaaS`_ is a supported toolchain with a large user base.

- LaaS-NG Bringup is a package supported in part by the pyATS core team.
  It provides a pluggable model that allows other teams to
  contribute (and support) plugins that extend the range of supported
  LaaS-NG platforms.

- `Kleenex Bringup`_ is supported by the pyATS core team and provides
  integration with the pyATS core.


.. _Kleenex Bringup: https://wiki.cisco.com/display/PYATS/Kleenex+Bringup+Documentation#KleenexBringupDocumentation-BringupModel

Bringup Feature Backlog
-----------------------
The following features are being considered for inclusion in
LaaS-NG Bringup:


Ideas for Community-Contributed Dyntopo Features
------------------------------------------------
The user community is invited to extend LaaS-NG Bringup, here are
some possible ideas:

- Support for additional virtual platforms

Ideas for Community-Contributed Post-Processing Libraries
---------------------------------------------------------
The pyATS :ref:`easypy_plugin` allows users to develop libraries that can
perform topology post-processing before control is handed to the user's script.
Some ideas include:

- Auto-generation and configuration of interface IP addresses, wait for
  interfaces to come up.
- Link connectivity verification (via either L2 ARP table or L3 ping).
- A topology transformer to model NX-OS VDC overlays.


.. _laasng bringup limitations:

Limitations
-----------

- The :ref:`remote copy<laas_remote_copy>` option must be used when bringing
  up crypto-enabled images, these cannot be brought up directly from an
  automount.  For more details, see the `Crypto Policy Guidelines`_.

- An attempt to launch an HA XRVR with ``ha_requested=True`` and
  ``multinode_requested=False`` fails since this platform's RP does not support
  more than two interfaces.  Typically a minimum of two RP interfaces are
  required, one for the console and one for the fabric interconnect.  Adding
  data-carrying interfaces directly to the RP requires explicit RP OVA support.

.. _Crypto Policy Guidelines: http://wwwin-eng.cisco.com/BMS/Mfg/Crypto_Policy_Guidelines/How_to_Request_Access_to_Encryption_Images.doc


