
.. _localbringup:


This `orchestrator`_ is designed to bring up and tear down dynamic IOL
topologies on an execution server.

.. _orchestrator: https://wiki.cisco.com/display/PYATS/Kleenex+Bringup+Documentation#KleenexBringupDocumentation-Orchestration


Support Mailers
---------------

.. sidebar:: Quick References

    - `IOL`_
    - `Routem`_

The `pyATS Support Team`_ would be happy to help you with any
issues relating to the dyntopo Local orchestrator.

You may create a question under `PieStack`_.

The `IOL`_ support mailer is `IOL Support`_.

You may also consider using the `pyATS Users`_ mailer.


.. _IOL: https://wiki.cisco.com/display/IOU/IOL%20Information
.. _Routem: http://wwwin-routem.cisco.com/
.. _int2netio: https://wiki.cisco.com/display/L2IOL/int2netio
.. _pyATS Support Team: pyats-support@cisco.com
.. _pyATS Users: pyats-users@cisco.com
.. _IOL Support: iou@cisco.com
.. _PieStack: http://piestack.cisco.com


Introduction
------------

This package allows multiple users to simultaneously launch IOL topologies
on the same execution server.


Installation
------------

pyATS Installation
^^^^^^^^^^^^^^^^^^

User needs to create an empty directory and inside that new directory
the installation script can be called.

.. code-block:: text

    /auto/pyats/bin/pyats install

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

    pip install dyntopo.local


Steps to upgrade to latest:

.. code-block:: text

    pip install --upgrade dyntopo.local


Post-Install Requirements
^^^^^^^^^^^^^^^^^^^^^^^^^

1. If this is the first time you are running IOL devices on an execution server,
the IOL launch command is expected to fail with the following error::

    BootException: BOOTEXCEPTION: Failed to get IOL license for xxxx, key yyyy

Obtain a license key at the following
`address <https://scripts.cisco.com/app/IOLLicenseGenerator>`_
(using yyyy from the error message as your "Key" and xxxx as the "Hostname":

Take the line of text emitted by the web tool and add it to your ``iourc``
file.



How to invoke
-------------
In order to select Local Bringup, either:

- Invoke the :ref:`local_decoupled_bringup`

- or, specify the following block of text in your
  :ref:`-clean_file <clean_schema>`::

    bringup:
        BringUpWorker:
            module: dyntopo.local

- or, specify a value of
  `dyntopo.local.BringUpWorker<dyntopo.local.worker.BringUpWorker>`
  against the ``-orchestrator`` parameter when instantiating the
  `BringUp<ats.kleenex.bringup_manager.BringUp>` object in
  `standalone bringup`_ mode.

.. _standalone bringup: https://wiki.cisco.com/display/PYATS/Kleenex+Bringup+Documentation#KleenexBringupDocumentation-StandaloneBringup


Local Device Orchestration
--------------------------
Users are able to request a topology of software-based devices which are spun up
directly on the execution server.  These devices are expected to communicate
via netio sockets.

For details on how to configure the orchestrator at a global and per-device
level, please review the :ref:`dyntopo clean schema` and the
:ref:`dyntopo logical testbed schema`.


Supported platforms
^^^^^^^^^^^^^^^^^^^
The following virtual platforms may be requested by specifying the
indicated name in the device ``type`` field of the logical testbed YAML file:

- iol
- routem

.. _local_remote_copy:


Remote Copy Option
^^^^^^^^^^^^^^^^^^
The ``remote_copy`` option is enabled by default, this means that
all device images are copied to the local server and removed
when the topology is torn down.

It may be disabled by one of the following means:

- If launching via :ref:`local_decoupled_bringup` or
  :ref:`easypy <kleenex_easypy_integration>`.

    - Specifying ``bringup/BringUpWorker/local/remote_copy: False`` in your
      clean YAML file,

- If launching from a `standalone script <standalone bringup>`_.

    - Specifying ``remote_copy=False`` when constructing the
      `BringUp<ats.kleenex.bringup_manager.BringUp>` object.


Routem Integration
^^^^^^^^^^^^^^^^^^

When the user specifies a virtual type of type ``routem``, the ``image``
field in the clean YAML's ``device`` block is expected to be set to a
user-provided script that launches a routem instance and does not exit.
The user may ask the local orchestrator to pass to the script dynamically
allocated arguments such as netio application ID and telnet access TCP port as
described in :ref:`dyntopo logical testbed schema`.

The local orchestrator then attempts to log into the newly spawned routem
device via unicon, so the user must provide appropriate authentication details
in the logical testbed YAML file.

Please refer to `local logical topology example`_ for an example of how this
may be specified.

When the time comes to tear down the routem device, the local orchestrator
terminates the routem launch script and any of its child processes.


Local Bringup User Role
-----------------------

Only the DT role is supported.
Please refer to `User Roles`_ for more details.

.. _User Roles: https://wiki.cisco.com/display/PYATS/Kleenex+Bringup+Documentation#KleenexBringupDocumentation-UserRoles


YAML inputs for DT workflows
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Local bringup requires a logical testbed YAML file and a clean YAML file
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


.. _local logical topology example:

Example Logical Topology Configuration File
"""""""""""""""""""""""""""""""""""""""""""

Here is an example of a testbed configuration file that requests a logical
topology connecting an IOL device and a dIOL device with each other and also
with a routem device:

.. note::
    This example assumes ``generate_legacy_credentials: False`` is specified
    in the clean YAML (see the :ref:`dyntopo clean schema` for details on
    how this setting influences user input expectations for routem devices).

.. code-block:: yaml

    devices:
        r1:
            type: iol
            logical: True
            connections: {defaults: {class: unicon.Unicon}}
            local:
                arguments: "-n 32"
                custom:
                r1_custom_key: r1_custom_value

        r2:
            type: iol
            logical: True
            ha_requested: True
            connections: {defaults: {class: unicon.Unicon}}
            custom:
                r2_custom_key: r2_custom_value

        routem1:
            type: routem
            logical: True
            credentials:
                default:
                    username: routem_username
                    password: routem_pw
            local:
                arguments: "{appid} {port}"

    topology:
        links:
            r1_routem:
                custom_link_key: custom_link_value

        r1:
            interfaces:
                r1r2_itf1:
                    link: r1r2_1
                    type: ethernet
                    actual_name: Ethernet1/0
                r1r2_itf2:
                    link: r1r2_2
                    type: ethernet
                    actual_name: Ethernet1/1
                r1_routem_itf1:
                    link: r1_routem
                    actual_name: Ethernet2/0
                    type: ethernet

        r2:
            interfaces:
                r2r1_itf1:
                    link: r1r2_1
                    type: ethernet
                    actual_name: Ethernet0/1
                r2r1_itf2:
                    link: r1r2_2
                    type: ethernet
                    actual_name: Ethernet0/3
                r2_routem_itf1:
                    link: r2_routem
                    actual_name: Ethernet1/0
                    type: ethernet
                    custom_key_for_if_r2_routem_itf1: custom_value


        routem1:
            interfaces:
                r1_itf:
                    link: r1_routem
                    type: ethernet
                    actual_name: eth2
                r2_itf:
                    link: r2_routem
                    type: ethernet
                    actual_name: eth1


YAML output for DT workflows
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Here is an example of the resulting testbed configuration file after
Local Bringup performs its topology launch and logical-to-actual
mapping.  Note that the device names reflect the actual devices chosen,
but the original logical device and interface names are preserved
through the use of aliases.  This file contains all the details necessary
for pyATS to connect to the already running topology.

.. code-block:: yaml

    testbed: {name: localbringup_2019Apr15_16_03_48.237795}

    devices:
      iolr1:
        alias: r1
        type: iol
        os: ios
        series: iol
        connections:
          a: {ip: 127.0.0.1, port: 11111, protocol: telnet}
          defaults: {class: unicon.Unicon}
        credentials:
            default: {username: lab, password: lab}
            enable {password: lab}

      iolr2:
        alias: r2
        type: iol
        os: ios
        series: iol
        connections:
          a: {ip: 127.0.0.1, port: 22222, protocol: telnet}
          b: {ip: 127.0.0.1, port: 33333, protocol: telnet}
          defaults: {class: unicon.Unicon}
        credentials:
            default: {username: lab, password: lab}
            enable {password: lab}
        custom: {r2_custom_key: r2_custom_value}

      routemroutem1:
        alias: routem1
        type: routem
        os: linux
        connections:
          a: {ip: 127.0.0.1, port: 44444, protocol: telnet}
        credentials:
            default: {username: routem_username, password: routem_pw}

    topology:
      links:
          r1_routem: {custom_link_key: custom_link_value}

      iolr1:
        interfaces:
          Ethernet1/0: {alias: r1r2_itf1, link: r1r2_1, type: ethernet}
          Ethernet1/1: {alias: r1r2_itf2, link: r1r2_2, type: ethernet}
          Ethernet2/0: {alias: r1_routem_itf1, link: r1_routem,
            type: ethernet}

      iolr2:
        interfaces:
          Ethernet0/1:
            alias: r2r1_itf1
            link: r1r2_1
            type: ethernet
            custom_key_for_if_r2_routem_itf1: custom_value

          Ethernet0/3: {alias: r2r1_itf2, link: r1r2_2, type: ethernet}
          Ethernet1/0: {alias: r2_routem_itf1, link: r2_routem,
            type: ethernet}

      routemroutem1:
        interfaces:
          eth1: {alias: r2_itf, link: r2_routem, type: ethernet}
          eth2: {alias: r1_itf, link: r1_routem, type: ethernet}



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


.. _local_decoupled_bringup:

Local Decoupled Bringup Tool
----------------------------

The decoupled tool may be used to bring up a dynamic topology and
emit a pyATS-compatible testbed YAML file that allows scripts to
connect with the newly created topology.
Please see `Decoupled Bringup`_ for more details.

.. _Decoupled Bringup: https://wiki.cisco.com/display/PYATS/Kleenex+Bringup+Documentation#KleenexBringupDocumentation-DecoupledBringup

It is possible to specify a user-defined cleaning tool that is automatically
invoked on newly brought up devices.

The value of parameter ``bringup_log_level`` may be specified
either in UPPERCASE or lowercase.

Here's an example::

    > localbringup -help
    usage: localbringup [-help] 
                        [-testbed_file FILE] [-clean_file FILE]
                        [-clean_devices [DEVICE [DEVICE ...]]]
                        [-loglevel LOGLEVEL] [-logdir DIR] [-no_mail] [-debug]
                        [-bringup_log_level {debug,info,warning,error,critical}]
                        [-logical_testbed_file FILE]
                        [-tb_yaml_output_file_name FILE]
                        [-topology_name TOPOLOGY_NAME]
                        [-max_launch_time_minutes MAX_LAUNCH_TIME_MINUTES]
                        [-sim_dir SIM_DIR] [-iol_flags IOL_FLAGS]

    A tool to perform dynamic topology bringup and/or device clean.

    localbringup command line arguments follow.
    Non-recognized args will be ignored (passed-through)

    Examples:
          localbringup -logical_testbed_file=/path/to/logical_testbed.yaml -clean_file=/path/to/clean.yaml

    --------------------------------------------------------------------------------

    Help:
      -help  show this help message and exit

    Testbed:
      -testbed_file FILE    Testbed YAML file.

    Clean:
      -clean_file FILE      YAML File containing clean/bringup configuration
                            details.
      -clean_devices [DEVICE [DEVICE ...]]
                            Specify list of devices to clean, separated by spaces.
                            To clean groups of devices sequentially, specify as
                            "[[dev1, dev2], dev3]".

    Logging:
      -loglevel LOGLEVEL    kleenex logging level. eg: -loglevel='INFO'
      -logdir DIR           Directory to save kleenex logs, defaults to current
                            working directory.

    Notification options:
      -no_mail              Disable sending email on abort.

    Debugging:
      -debug                Run kleenex in debugging mode (synchronous clean, pdb
                            on error)

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
      -topology_name TOPOLOGY_NAME
                            Optional topology name.

    Local Bringup options:
      -max_launch_time_minutes MAX_LAUNCH_TIME_MINUTES
                            The maximum number of minutes to wait before aborting
                            the virtual topology launch.
      -sim_dir SIM_DIR      A simulation directory to run the testbed in.
      -iol_flags IOL_FLAGS  Extra flags to pass to IOL instances.



Working Examples
----------------

The following example shows how to perform an all-in-one test that performs
the following steps:

   - Brings up a dynamic topology of an IOL and a dIOL device,
   - Runs a sample job that connects to the devices,
   - Tears down the dynamic topology.

.. code-block:: python

   cd examples/dyntopo_local
   easypy jobs/connect_test_job.py
   -logical_testbed_file yaml/iol_tb.yaml
   -clean_file yaml/iol_bringup.yaml
   -clean_scope=task

The job file has the following contents:

.. code-block:: python

    import os, sys
    from ats.easypy import run
    def main():
        test_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        testscript = os.path.join(test_path, 'tests', 'connect_test.py')

        run(testscript=testscript, uut1_name='r1', uut2_name='r2')

Please see :ref:`local logical topology example` for the input logical testbed file and
output actual testbed file contents.

The clean file has the following contents (images are not shown but must be
specified for each device):

.. code-block:: python

    bringup:
        BringUpWorker:
            module: dyntopo.local
            log_level: debug



Please refer to the following link for a complete set of working examples :
:download:`local_bringup_examples.rst <local_bringup_examples.rst.txt>`.


Netio Application ID Management
-------------------------------

Netio application IDs are managed on a server-wide basis and are allocated to
devices as they are launched.  This ensures multiple topologies may be run
on the same execution server by one or more users at the same time.

.. note::

    This server-wide appid registry is kept in shared memory and any appids
    that are blocked or in use are cleared upon server restart.


Help Display
^^^^^^^^^^^^

Help may be obtained as follows::

    > appid --help
    usage: appid [-h] {status,block,unblock} ...

    positional arguments:
      {status,block,unblock}
        status              Display the appid status on this server.
        block               Block one or more appids on this server.
        unblock             Unblock one or more appids on this server.

    optional arguments:
      -h, --help            show this help message and exit


Help may also be obtained for individual subcommands.  For example::

    > appid block --help
    usage: appid block [-h] --appids APPIDS

    optional arguments:
      -h, --help       show this help message and exit
      --appids APPIDS  One or more appids to block. For example : 1,2,3-5


Displaying Appid Status
^^^^^^^^^^^^^^^^^^^^^^^

The following command may be used to display the application IDs currently in
use on the server and which process was responsible for allocating them::

    >appid status
    Appid     Status     Owner PID     Owner Name
    312       In Use     1355          BringUpWorker_localbringup_2019Apr15_16_03_48.237795
    492       In Use     1355          BringUpWorker_localbringup_2019Apr15_16_03_48.237795
    704       In Use     1355          BringUpWorker_localbringup_2019Apr15_16_03_48.237795

Blocking and Unblocking Appids
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In cases where static IOL topologies are to coexist with dynamic IOL topologies
on the same server, it is possible to block and unblock appids from the
server-wide appid registry.

A blocked appid is never allocated to any dynamic device launched by this
orchestrator.

An appid cannot be blocked if it is in use, and an appid must be blocked
in order to be unblocked.


For example::

    >appid block --appids 3,5,7-9
    Appid     Status     Owner PID     Owner Name
    3         Blocked
    5         Blocked
    7         Blocked
    8         Blocked
    9         Blocked
    312       In Use     1355          BringUpWorker_localbringup_2019Apr15_16_03_48.237795
    492       In Use     1355          BringUpWorker_localbringup_2019Apr15_16_03_48.237795
    704       In Use     1355          BringUpWorker_localbringup_2019Apr15_16_03_48.237795

    >appid unblock --appids 7-9
    Appid     Status     Owner PID     Owner Name
    3         Blocked
    5         Blocked
    312       In Use     1355          BringUpWorker_localbringup_2019Apr15_16_03_48.237795
    492       In Use     1355          BringUpWorker_localbringup_2019Apr15_16_03_48.237795
    704       In Use     1355          BringUpWorker_localbringup_2019Apr15_16_03_48.237795



.. _local_telnet_server:

Telnet Server
-------------

The local orchestrator wraps programs such as software devices in order to
allow users to interact with these programs using telnet.

The ``telnetserver`` standalone command exposes this wrapper.

Help may be obtained as follows::

    >telnetserver --help
    usage: telnetserver [-h] --name NAME --program PROGRAM [--arguments ARGUMENTS]
                        [--run-dir RUN_DIR] [--sim-dir SIM_DIR] [--port PORT]
                        [--loglevel LOGLEVEL] [--json-console-log]

    optional arguments:
      -h, --help            show this help message and exit

    Program:
      --name NAME           The human-readable name of the program being run and
                            wrapped.
      --program PROGRAM     The path to the program to run and wrap.
      --arguments ARGUMENTS
                            The arguments to the program to run and wrap.

    Directories:
      --run-dir RUN_DIR     Path where logfiles are to be created. Defaults to
                            current working directory.
      --sim-dir SIM_DIR     Path where the program is to be run. Defaults to
                            current working directory.

    Server:
      --port PORT           The port number to telnet to in order to interact with
                            the program. If not specified, an available port is
                            allocated dynamically.

    Logging:
      --loglevel LOGLEVEL   telnetserver logging level. eg: -loglevel='INFO'
      --json-console-log    When specified, console logs become JSON-formatted.






.. _local bringup limitations:

Limitations
-----------

- The following features are not yet supported by the local orchestrator:

  - `int2netio`_ integration
  - L2 IOL
  - IOL multinode support (line card integration)
