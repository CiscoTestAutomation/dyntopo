.. _xrutbringup:


This `orchestrator`_ uses the community supported
toolchain `XR-UT`_ to bring up dynamic topologies.

.. _orchestrator: https://wiki.cisco.com/display/PYATS/Kleenex+Bringup+Documentation#KleenexBringupDocumentation-Orchestration

Support Mailers
---------------

If XR-UT Bringup is failing due to an XR-UT issue, you may contact the
`XRUT Support Mailer`_.  This mailer is community-supported.

The `pyATS Support Team`_ would be happy to help you with any
issues relating to the dyntopo XR-UT orchestrator.

Please consider creating a question under `PieStack`_.

If you are hitting problems related to using Moonshine under pyATS, you may
contact the `Moonshine Support Mailer`_.

You may also consider making use of one of the following mailers :
`pyATS Users`_.


.. _XRUT Support Mailer: xrut-support@cisco.com
.. _pyATS Support Team: pyats-support@cisco.com
.. _PieStack: http://piestack.cisco.com
.. _pyATS Users: pyats-users@cisco.com
.. _Moonshine Support Mailer: moonshine-support@cisco.com


.. _EnXR: http://enwiki.cisco.com/EnXR
.. _Moonshine: https://confluence-eng-sjc1.cisco.com/conf/display/ENXR/Moonshine
.. _Dynamips 7200 emulator: https://en.wikipedia.org/wiki/Dynamips
.. _XRVR: http://wiki.cisco.com/display/REFPLATS/XRVR+Reference+Platform
.. _LaaS: http://wiki.cisco.com/display/LAAS/LaaS
.. _CSR1000v: https://wiki.cisco.com/display/REFPLATS/Ultra+Reference+Platform

.. sidebar:: Quick References

    - `XR-UT`_
    - `EnXR`_
    - `Moonshine`_
    - `Dynamips 7200 emulator`_
    - `XRVR`_
    - `LaaS`_
    - `CSR1000v`_


Introduction
------------

XR-UT Bringup supports software-based device topologies only.


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
    pip install dyntopo.xrut


Steps to upgrade to latest:

.. code-block:: text

    source env.csh
    pip uninstall dyntopo
    pip install --upgrade dyntopo.xrut



Post-Installation Requirements
------------------------------

1. A TCL tree must be sourced.
    The reason is because pyATS scripts interact with devices via the abstract
    connection model, and the most robust and complete implementation of this
    model requires a TCL backend.  If you do not have your own TCL
    ATS tree, the default ATS tcl tree may be used, refer to
    `Linking to default ATS tree`_.

2. An ATS patch is required.
    A special ATS tree patch is required in order for users to log onto EnXR
    simplex and HA devices.  This patch has been placed in the
    default ATS tree for your convenience.

    If you have your own tarball ATS tree, please follow these instructions to
    install the patch:

    a) ``source /your/ats/tree/location/env.csh # env.sh in case of bash shell``

    b) ``$AUTOTEST/atsc.csh -setup_repo 1 -repo_type transparent # atsc.sh in case of bash shell``

    c) ``teacup install Csccon  -exact 5.6.4``

    d) ``teacup install ha      -exact 4.4.2``

    e) ``teacup install ngclean -exact 5.4.2``

    f) ``teacup install Cisco   -exact 5.4.0``

    g) ``teacup install AEtest  -exact 5.4.0``

    h) ``$AUTOTEST/atsc.csh -setup_repo 1 -repo_type transparent-devtest # atsc.sh in case of bash shell``

    i) ``teacup install ha      -exact 6.0.1b1``

    j) ``teacup install Csccon  -exact 6.0.1b1``

    k) ``setenv TCL_PKG_PREFER_LATEST  1    # export TCL_PKG_PREFER_LATEST=1 in case of bash shell``


    If you have your own centralized ATS tree, please follow these
    instructions to install the patch:

    a) ``source /your/ats/tree/location/env.csh # env.sh in case of bash shell```

    b) ``$AUTOTEST/atsc.csh -setup_repo 1 -repo_type opaque # atsc.sh in case of bash shell``

    c) ``teacup install Csccon  -exact 5.6.4``

    d) ``teacup install ha      -exact 4.4.2``

    e) ``teacup install ngclean -exact 5.4.2``

    f) ``teacup install Cisco   -exact 5.4.0``

    g) ``teacup install AEtest  -exact 5.4.0``

    h) ``$AUTOTEST/atsc.csh -setup_repo 1 -repo_type opaque-devtest # atsc.sh in case of bash shell``

    i) ``teacup install ha      -exact 6.0.1b1``

    j) ``teacup install Csccon  -exact 6.0.1b1``

    k) ``setenv TCL_PKG_PREFER_LATEST  1    # export TCL_PKG_PREFER_LATEST=1 in case of bash shell``



3. If you want to launch jobs on a LaaS_ server, you must have
   `passwordless SSH`_ enabled.  You must be able to ssh to your
   server without being prompted for a password.  If you have a public LaaS
   server this should be all the configuration that is necessary.
   If, however, you have a private LaaS server, here are a few ways you could
   provide passwordless access:

   - Install  Vintella_  (requires a call to the help desk to do pre-setup)

   - On servers with only local admin user access, create a private key for
     the admin user and export it to the home directory of all users needing
     to launch topologies on the server.  For example:

     .. code-block:: bash

        scp lab@<hostname>:.ssh/id_rsa-lab ~/.ssh

        # Then, add the following text into your home directory under ~/.ssh/config:
          Host <hostname>
              User lab
              IdentityFile ~/.ssh/id_rsa-lab


.. _passwordless SSH: https://apps.na.collabserv.com/wikis/home/wiki/W52d8c1c91d6a_41eb_a30f_021c10f3ec18/page/Engineering%20Non?interactive%20SSH%20Setup%20Instructions

.. _Vintella: https://wiki.cisco.com/display/ECBU/Ubuntu+Vintela+Migration

.. _Linking to default ATS tree: https://wiki.cisco.com/display/PYATS/Activating+Instance#ActivatingInstance-LinkingtodefaultATStree


How to invoke
-------------
In order to select the XR-UT Bringup orchestrator, either:

- Use the :ref:`xrut_decoupled_bringup`

- or, specify the following block of text in your
  :ref:`-clean_file <clean_schema>`::

    bringup:
        BringUpWorker:
            module: dyntopo.xrut

- or, specify a value of
  `dyntopo.xrut.BringUpWorker<dyntopo.xrut.worker.BringUpWorker>`
  against the ``-orchestrator`` parameter when instantiating the
  `BringUp<ats.kleenex.bringup_manager.BringUp>` object in
  `standalone bringup`_ mode.

.. _standalone bringup: https://wiki.cisco.com/display/PYATS/Kleenex+Bringup+Documentation#KleenexBringupDocumentation-StandaloneBringup

XR-UT Local orchestration
-------------------------

XR-UT Bringup is capable of launching software-based devices on a
local execution server, which is expected to be running Cisco Enterprise
Linux.  This is the same server that pyATS tests are normally run from.
This model is most common for DE workflows, in which users are
building and testing device images on the same development server.

Virtual wiring is created to interconnect the locally orchestrated devices.

XR-UT Remote orchestration
--------------------------

XR-UT Bringup is capable of launching software-based device topologies
on a `LaaS`_ (Lab as a Service) execution server.


XR-UT Supported Platforms
-------------------------

XR-UT Bringup is capable of bringing up networks containing any of the
following types of devices:

- Locally orchestrated:

    - IOL (traditional or Pagent-enabled)
    - IOS Dynamips (traditional or Pagent-enabled)
    - EnXR (simplex or HA, with or without multinode)
    - XRVR (simplex)
    - NXOSv (Titanium)

- Remotely orchestrated via LaaS:

    - IOSv
    - NXOSv (Titanium)
    - XRVR (simplex or HA)
    - CSR1000v (Ultra)

- Locally orchestrated, but under-the-covers launched on a remote host
  (UCS/LaaS), with the connections exposed on the local machine:

    - Moonshine (simplex or HA, with or without multinode)


XR-UT Bringup User Roles
------------------------

Please refer to `User Roles`_ for more details.

.. table:: XR-UT Bringup user roles

    ===============================     ==============================
    DE Role                             DT Role
    ===============================     ==============================
    Plug and play                       Not plug and play
    No YAML files needed                Must specify YAML files
    Specify most parameters via CLI     Specify few parameters via CLI
    No logical-to-actual mapping        Logical-to-actual mapping done
    ===============================     ==============================

.. _User Roles: https://wiki.cisco.com/display/PYATS/Kleenex+Bringup+Documentation#KleenexBringupDocumentation-UserRoles

CLI inputs for DE workflows
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Here is an example of running the standalone ``xrutbringup`` command to launch
a two-device network consisting of an IOS device and a Pagent device:

.. code-block:: bash

    xrutbringup -cli_topology='{ "n1": ( "ios1", "ios-pagent-1" )}'
    -default_type=ios -sim_dir=/nobackup/$USER/xrut_sim_dir
    -bringup_no_mail -tb_yaml_output_file_name=/tmp/tb1.yaml


Testbed Configuration YAML output for DE workflows
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Here is an example of the YAML file emitted by the previous command
once the requested topology was spun up.  This YAML file may be
used as input to a pyATS script in order to run tests against the devices
in the topology:

.. code-block:: yaml

    devices:
        ios-pagent-1:
            connections:
                a: {protocol: xrutconnect}
                aux: {protocol: xrutconnect}
            passwords: {enable: lab, line: lab, tacacs: lab}
            tacacs: {username: lab}
            type: ios_pagent
        ios1:
            connections:
                a: {protocol: xrutconnect}
                aux: {protocol: xrutconnect}
            passwords: {enable: lab, line: lab, tacacs: lab}
            tacacs: {username: lab}
            type: ios

    testbed:
        bringup:
            xrut:
                base_dir: /auto/xrut/xrut-gold
                sim_dir: /nobackup/mdear/xrut_sim_dir

    topology:
        ios-pagent-1:
            interfaces:
                FastEthernet0/0:
                    ipv4: 10.10.10.2/24
                    ipv6: '10:10:10::2/64'
                    link: n1
                    type: ethernet
        ios1:
            interfaces:
                FastEthernet0/0:
                    ipv4: 10.10.10.1/24
                    ipv6: '10:10:10::1/64'
                    link: n1
                    type: ethernet


YAML inputs for DT workflows
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

XR-UT Bringup requires a logical testbed YAML file and a clean YAML file
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


.. note::
    Although it is possible to specify logical and non-logical devices
    in the same testbed configuration file, it is not possible to
    specify connections between them.  At present, XR-UT Bringup
    can only interconnect logical devices with other logical devices.

.. _logical topology example:

Example Logical Topology Configuration File
"""""""""""""""""""""""""""""""""""""""""""

Here is an example of a testbed configuration file that requests a logical
topology consisting of a simplex XR-VR device connected to a simplex
EnXR device via a single link:

.. code-block:: yaml

    devices:
        r1:
            type: iosxrv
            logical: True
            custom:
                r1_custom_key: r1_custom_value
        r2:
            type: enxr
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

YAML output for DT workflows
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Here is an example of the resulting testbed configuration file after
XR-UT Bringup performs its topology launch and logical-to-physical
mapping.  Note that the devices are assigned new names that reflect their
type while still containing the logical device name.  The original logical
device and interface names are preserved via the use of aliases.
This file contains all the details necessary for pyATS to connect to
the already running topology:


Example Actual Topology Configuration File
""""""""""""""""""""""""""""""""""""""""""

.. code-block:: yaml

    devices:
        enxrr2:
            alias: r2
            connections:
                a: {protocol: xrutconnect}
            passwords: {enable: lab, line: lab, tacacs: lab}
            tacacs: {username: lab}
            type: enxr

        xrvrr1:
            alias: r1
            connections:
                a: {protocol: xrutconnect}
                aux: {protocol: xrutconnect}
            passwords: {enable: password, line: password, tacacs: password}
            tacacs: {username: throwaway}
            type: iosxrv
            r1_custom_key: r1_custom_value

    testbed:
        bringup:
            xrut:
                base_dir: /auto/xrut/xrut-gold
                sim_dir: /nobackup/mdear/ci-531-two
    topology:
        links:
            n1:
                custom_link_n1_key: custom_link_n1_value

        enxrr2:
            interfaces:
                GigabitEthernet0/0/0/0:
                    alias: if2.1
                    ipv4: 10.10.10.1/24
                    ipv6: '10:10:10::1/64'
                    link: n1
                    type: ethernet

        xrvrr1:
            interfaces:
                GigabitEthernet0/0/0/0
                    alias: if1.1
                    ipv4: 10.10.10.2/24
                    ipv6: '10:10:10::2/64'
                    link: n1
                    type: ethernet
                    custom_key_for_if1.1: custom_value_for_if1.1


Content Transfer from Logical to Actual Topology Configuration File
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

The example just given shows custom key/value pairs being specified at logical
device, link and interface levels.  This content is transferred from the logical
to the actual topology configuration file as shown in the next section.

Also, in the event of a collision between user-specified
logical testbed configuration content and orchestrator-autogenerated content,
the user-specified content is always applied,
the orchestrator's content is overwritten, and a warning is given.

For example, if the user chooses to specify their own IP address for a
particular interface in the logical testbed configuration, that address
appears in the actual testbed configuration instead of the autogenerated
address.  However, in doing so the user must take responsibility to apply
this interface configuration to the device themselves (since the
orchestrator already generates and applies its own IP configuration).


`XR-UT`_ does not support multiple parallel topologies
on on some virtual platforms.  Please see the list of
:ref:`xrut bringup limitations` for details.



.. _xrut_decoupled_bringup:

Decoupled Bringup Tool
----------------------

The decoupled tool may be used to bring up a dynamic topology and
emit a pyATS-compatible testbed YAML file that allows scripts to
connect with the newly created topology.  Please see
`decoupled Bringup`_ for more details.

.. _Decoupled Bringup: https://wiki.cisco.com/display/PYATS/Kleenex+Bringup+Documentation#KleenexBringupDocumentation-DecoupledBringup

Although it is possible to specify a user-defined cleaning tool that is
automatically invoked on newly brought up devices, as `XR-UT`_
does not support dynamic physical topologies, the ``-clean_devices`` parameter
may be ignored.

.. _XR-UT: https://wiki.cisco.com/display/PYATS/XR-UT

The parameters `bringup_log_level` and `bringup_xrut_log_level` may be
specified either in UPPERCASE or lowercase.

Here's an example:

.. code-block:: bash

    > xrutbringup -help
    usage: xrutbringup [-help] 
                       [-testbed_file FILE] [-clean_file FILE]
                       [-clean_devices [DEVICE [DEVICE ...]]] [-loglevel LOGLEVEL]
                       [-logdir DIR] [-no_mail]
                       [-bringup_log_level {debug,info,warning,error,critical}]
                       [-logical_testbed_file FILE]
                       [-tb_yaml_output_file_name FILE]
                       [-xrut_base_dir DIR]
                       [-max_launch_time_minutes MAX_LAUNCH_TIME_MINUTES]
                       [-cli_topology CLI_TOPOLOGY]
                       [-router_requirements ROUTER_REQUIREMENTS]
                       [-workspace WORKSPACE] [-sim_dir SIM_DIR]
                       [-default_type DEFAULT_TYPE] [-iol_flags IOL_FLAGS]
                       [-iol_image FILE] [-iol_pagent_image FILE]
                       [-ios_image FILE] [-ios_pagent_image FILE]
                       [-ios_dynamips_idlepc IDLEPC]
                       [-ios_pagent_dynamips_idlepc IDLEPC] [-ultra_image FILE]
                       [-xrvr_image FILE] [-xrvr_nic_type XRVR_NIC_TYPE]
                       [-xrvr_lc_image FILE] [-xrvr_rp_image FILE]
                       [-nxos_image FILE] [-vmcloud_server VMCLOUD_SERVER]
                       [-vmcloud_port VMCLOUD_PORT]
                       [-vmcloud_image_dir VMCLOUD_IMAGE_DIR]
                       [-moonshine_image FILE]
                       [-moonshine_host MOONSHINE_HOST]
                       [-moonshine_dir MOONSHINE_DIR]
                       [-bringup_xrut_log_level {debug,info,quiet}]

    A tool to perform dynamic topology bringup and/or physical device clean.

    xrutbringup command line arguments follow.
    Non-recognized args will be ignored (passed-through)

    Examples:
          xrutbringup -logical_testbed_file=/path/to/logical_testbed.yaml -clean_file=/path/to/clean.yaml
        
    --------------------------------------------------------------------------------

    Help:
      -help  show this help message and exit

    Testbed:
      -testbed_file FILE    Testbed YAML file.

    Clean:
      -clean_file FILE      YAML File containing clean/bringup configuration
                            details.
      -clean_devices [DEVICE [DEVICE ...]]
                            Specify list of devices to clean

    Logging:
      -loglevel LOGLEVEL    kleenex logging level. eg: -loglevel='INFO'
      -logdir DIR           Directory to save kleenex logs default to current
                            working directory.

    Notification options:
      -no_mail              Disable sending email on abort.

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

    XR-UT Bringup options:
      -xrut_base_dir DIR    The XR-UT base directory to use when launching virtual
                            topologies.
      -max_launch_time_minutes MAX_LAUNCH_TIME_MINUTES
                            The maximum number of minutes to wait before aborting
                            the virtual topology launch.

    XR-UT Bringup Execution options:
      -cli_topology CLI_TOPOLOGY
                            A topology description string
      -router_requirements ROUTER_REQUIREMENTS
                            An XR-UT style router requirements string.
      -workspace WORKSPACE  A workspace containing built loads.
      -sim_dir SIM_DIR      A simulation directory to hold testbed metadata.
      -default_type DEFAULT_TYPE
                            Default router type (ios, iol, enxr, xrvr, nxos)
      -iol_flags IOL_FLAGS  Extra flags to pass to IOL instances. This parameter
                            may be specified multiple times (ie.
                            -iol_flags="-console_timeout 1000" -iol_flags="-m
                            512")

    XR-UT Bringup IOS Image Options:
      -iol_image FILE
      -iol_pagent_image FILE
      -ios_image FILE
      -ios_pagent_image FILE
      -ios_dynamips_idlepc IDLEPC
                            The IdlePc value required by the Dynamips IOS image.
      -ios_pagent_dynamips_idlepc IDLEPC
                            The IdlePc value required by the Dynamips IOS Pagent
                            image.
      -ultra_image FILE     A CSR1000v OVA image.

    XR-UT Bringup XRVR Image Options:
      -xrvr_image FILE
      -xrvr_nic_type XRVR_NIC_TYPE
                            An XRVR NIC type (e1000, virtio, etc.)
      -xrvr_lc_image FILE   An XRVR Line Card Image
      -xrvr_rp_image FILE   An XRVR HA Route Processor Image

    XR-UT Bringup NX-OS Image Options:
      -nxos_image FILE

    XR-UT Bringup VmCloud options :
      -vmcloud_server VMCLOUD_SERVER
                            VM Cloud server to use
      -vmcloud_port VMCLOUD_PORT
                            VM Cloud server port to use
      -vmcloud_image_dir VMCLOUD_IMAGE_DIR
                            Directory to use for vm cloud images, can be scp
                            style.

    XR-UT Bringup Moonshine Options:
      -moonshine_image FILE
                            Moonshine image to use
      -moonshine_host MOONSHINE_HOST
                            Moonshine host machine to use, e.g. a UCS or LaaS
      -moonshine_dir MOONSHINE_DIR
                            Base directory to use on host machine, defaults to
                            /nobackup/$USER

    XR-UT Bringup Logging options:
      -bringup_xrut_log_level {debug,info,quiet}
                            Logging level for the XR-UT backend invoked by the
                            bringup module.

.. _dyntopo xrut working examples:

Working Examples
----------------

The following example shows how to perform an all-in-one test that
performs the following:

   - Brings up a dynamic topology consisting of an EnXR and a simplex
     XRVR device,
   - Runs a sample job that connects to the devices and pings between them,
   - Tears down the dynamic topology.

.. code-block:: python

   cd <pyats_root>/lib/py*/site-packages/dyntopo/xrut/examples
   easypy jobs/ping_test_job.py
   -logical_testbed_file yaml/enxr_xrvr_ping_test_config.yaml
   -clean_file yaml/enxr_xrvr_ping_bringup_config.yaml


The job file has the following contents:

.. code-block:: python

    import os, sys
    from ats.easypy import run
    def main():
        run(testscript=\
            "{}/lib/python3.4/site-packages/dyntopo/examples/xrut/" \
            "standalone_tests/standalone_ping_test.py".\
                format(sys.prefix) , uut1_name='r1',
                uut2_name='r2', uut1_if_name='if1.1', uut2_if_name='if2.1')


The clean file has the following contents (substitute your EnXR workspace):

.. code-block:: python

    bringup:
        BringUpWorker:
            module: dyntopo.xrut
            log_level: warning
            xrut:
                default_device_type: enxr
                workspace: /nobackup/<my_username>/<my_ws_name>
                log_level: quiet

    groups:
        iosxrv:
            devices: [r1]
            images: [/auto/xrut/images/iosxrv.vmdk.old]

See `logical topology example`_ for the logical testbed file and the
resulting actual (output) testbed file content.


Moonshine working example
^^^^^^^^^^^^^^^^^^^^^^^^^

.. _dyntopo xrut working examples moonshine:

Here is an example of how to launch the Moonshine environment and create a
Moonshine testbed file via the `xrutbringup` command (for a more complete
set of examples, see below).

Launch command, from root of pyATS workspace:

.. code-block:: bash

    $ xrutbringup -clean_file clean.yaml -logical_testbed_file config.yaml
      -tb_yaml_output_file_name=/tmp/tb1.yaml

Example clean.yaml file for Moonshine launch (here specifying a particular XRUT
repo). Note that it is necessary to specify the Moonshine host and image:

.. code-block:: python

    bringup:
        BringUpWorker:
            module: dyntopo.xrut
            xrut:
                base_dir: <xrut repo>
                moonshine_host: <host machine>
                moonshine_dir: <working dir on host - optional>
    devices:
        r1:
            images: [<path to Moonshine image>/enxr-router-spirit-64.vm]

Example config.yaml logical testbed file:

.. code-block:: python

    testbed:
        name: ios_moonshine

    devices:
        r1:
            type: moonshine
            logical: True
            ha_requested : True
            connections:
              defaults: {class: unicon.XRUTConnect}
        r2:
            type: ios_dynamips_pagent
            logical: True

    topology:
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

To see an example of the resulting testbed file, see :ref:`unicon user_guide connection moonshine` .

Complete set of working examples
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Please refer to the following link for a complete set of working examples :
:download:`various_xrut_examples.rst <various_xrut_examples.rst.txt>`.



Glossary
--------

.. glossary::
    :sorted:

    Sim-Dir
        A directory into which XR-UT captures metadata about a topology.
        In order to connect to devices running in the topology, the
        sim_dir must be known.
        Multiple topologies cannot simultaneously run in the same sim_dir.

    Workspace
        A directory containing a pulled and built workspace.  XR-UT
        requires a workspace when launching EnXR devices.  When a
        workspace is specified, XRUT locates the sim_dir under the
        workspace.

XR-UT Bringup's Multiprocessing Model
-------------------------------------

Please see `Multiprocessing Model`_ for more details.

.. _Multiprocessing Model: https://wiki.cisco.com/display/PYATS/Kleenex+Bringup+Documentation#KleenexBringupDocumentation-MultiprocessingModel

XR-UT Bringup always launches its in its own subprocesses.
This is done to ensure that a dynamic topology is always gracefully torn down
if interrupted via a signal or by the user hitting <Control><C>.

XR-UT Bringup supports both task and job scopes
(see `easypy Bringup`_ for details).

.. _easypy Bringup: https://wiki.cisco.com/display/PYATS/Kleenex+Bringup+Documentation#KleenexBringupDocumentation-easypyBringup

Many processes are created when XR-UT Bringup is selected as part of an
easypy run (please see :ref:`async_index` for more details).

.. note::
    The name of the forked XR-UT process contains the name of its
    worker class
    `dyntopo.xrut.BringUpWorker<dyntopo.xrut.worker.BringUpWorker>`.
    The `XR-UT`_ subprocess creates its own logs under the
    :ref:`easypy_runinfo` directory under the name `xrut_log_dir_taskid`.

Here's an example to illustrate:

.. code-block:: text

    Pictorial View of XR-UT Bringup Processes - Job-scope Launch
    ------------------------------------------------------------

    +--------------+    fork     +-----------------+
    | easypy       |-------------| AEReport Server |
    | (pid 1000)   |             | (pid 1001)      |
    +--------------+             +-----------------+
           |
           | fork          +-----------------+
           +---------------+ Bringup for Job |
                           | (pid 1002)      |
                           +--------+--------+
                                    | spawn
                                    | subprocess
                                    |
                                    |
                         +----------+----------+
                         | XR-UT cli-launch    +
                         | (pid 1003)          +
                         +---------------------+


    Pictorial View of XR-UT Bringup Processes - Task-scope Launch
    -------------------------------------------------------------

    +--------------+    fork     +-----------------+
    | easypy       |-------------| AEReport Server |
    | (pid 1000)   |             | (pid 1001)      |
    +--------------+             +-----------------+
           |
           |
           | fork          +---------------+ fork    +---------------------+
           +---------------+ Task __task1  +---------+ Bringup for __task1 |
           |               | (pid 1002)    |         | (pid 1003)          |
           |               +---------------+         +----------+----------+
           |                                                    | spawn
           |                                                    | subprocess
           |                                                    |
           |                                                    |
           |                                         +----------+----------+
           |                                         | XR-UT cli-launch    +
           |                                         | (pid 1004)          +
           |                                         +---------------------+
           |
           |
           | fork          +---------------+ fork    +---------------------+
           +---------------+ Task __task2  +---------+ Bringup for __task2 |
           |               | (pid 1005)    |         | (pid 1006)          |
           |               +---------------+         +----------+----------+
           |                                                    | spawn
           |                                                    | subprocess
           |                                                    |
           |                                                    |
           |                                         +----------+----------+
           |                                         | XR-UT cli-launch    +
           |                                         | (pid 1007)          +
           |                                         +---------------------+
           etc.

.. _XR-UT bringup Governance Model:

Governance
----------

- `Kleenex Bringup`_ is a community supported toolchain with a large user
  base.  It can launch topologies of software-based devices by offering a
  logical dynamic testbed bringup model that works across a variety
  of different backends (local orchestration, LaaS, VXR-2, VXR).

- `Kleenex Bringup`_ is supported by the pyAts core team and provides a
  bridge/wrapper to XRUT's dynamic testbed bringup model.

- This means that any new features must first be added to and hardened
  under native `XR-UT`_ before they can be made available from
  XR-UT Bringup.

- The `ASG team`_ provides best-effort support for XRUT core components
  and reviews proposed changes to core components from the user community
  to ensure architectural fidelity.

- By default, XR-UT Bringup always invokes the latest "gold" XRUT
  distribution, which is updated on a daily basis as new commits come in.
  If a commit breaks `XR-UT`_, then XR-UT Bringup
  would not be able to bring up dynamic topologies until the
  `XR-UT`_ community commits a fix.

.. _ASG team: http://wwwin-asg.cisco.com

.. _Kleenex Bringup: https://wiki.cisco.com/display/PYATS/Kleenex+Bringup+Documentation#KleenexBringupDocumentation-BringupModel

Bringup Feature Backlog
-----------------------
The following features are being considered for inclusion in
XR-UT Bringup:


- Support for eARMS launch of topologies containing EnXR nodes.
- Support for VXR-2 orchestration.
- Support for VXR orchestration.


.. _xrut bringup limitations:

Limitations
-----------

Please take note of the following limitations that were discovered during
feature development:

- XR-UT Bringup does not support multiple parallel locally orchestrated
  topologies of IOS or XR-VR.

- XR-UT does not model external connections between its topologies and
  the outside world.

- XR-UT cannot launch reference or modern dIOL images.

- XR-UT cannot launch more than one IOL topology at a time per user per
  execution server.

- XR-UT cannot launch multinode XRVR (simplex or HA) via local orchestration.

- Sporadic failures were seen in which a simplex XRVR could not ping a locally
  orchestrated IOS Dynamips or IOL device.

- An attempt to launch an HA XRVR with ``ha_requested=True`` and
  ``multinode_requested=False`` fails if the XRVR-RP OVA does not support
  more than two interfaces.  Typically a minimum of two RP interfaces are
  required, one for the console and one for the fabric interconnect.  Adding
  data-carrying interfaces directly to the RP requires explicit RP OVA support.

- If launching an HA XRVR, please specify ``default_device_type=iosxrv``.
  In some cases XR-UT disables multinode mode if this is not done,
  leading to the problem described above.

- If launching an IOSv and a CSR1000v, please specify ``default_device_type=iosv``.
  Otherwise, a CSR1000v is launched instead of an IOSv.

- When launching Moonshine, the ``moonshine_host`` option must be specified
  to indicate a host machine to launch the Moonshine session on.


Non-Requirements
----------------
The following requirements were specifically excluded from XR-UT Bringup:

- DRP support on EnXR nodes

