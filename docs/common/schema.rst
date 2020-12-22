.. _dyntopo clean schema:

Dyntopo Clean Schema
====================

The dyntopo clean schema extends the
:ref:`production clean schema<clean_schema>`.
The schema controls what information can go into the clean file,
and how that information must be structured.
If a clean file is provided to any dyntopo orchestrator,
it is checked against this schema.

Always keep in mind that YAML is a white-space indentation sensitive markup
language (like how Python is). If your clean file is having issues, check your
section indentations, and remember not to use tab characters.

.. note::
    The front-end `-clean_scope` parameter controls whether bringup is done
    at the job or the task scope.  Please refer to :ref:`easypy_arguments`
    for details.

.. note::
    Although images are specified in the devices block, since XR-UT can only
    load by platform, an exception is thrown unless all devices of the
    same platform type have the same image.  This restriction applies only
    to the XR-UT orchestrator.

.. note::
    When specifying images in the image list, the XR-UT and LaaS  orchestrators
    typically only use the first image in the list.  However, when both
    RP and LC XRVR images need to be specified, make sure the RP image is
    specified first and the LC image is specified second.

.. note::
    The local orchestrator allows specifying some images by role or directly
    by list.   When specifying dIOL images via list, make sure the RP
    image is specified first and the CI image is specified second.
    The following roles may be used to specify dIOL images : 'rp', 'ci'.

.. note::
    URL-based images are not supported, images are expected to be accessible
    via the local file system.

.. note::
    When type ``routem`` is specified using the local orchestrator, the
    following keys must be specified in the logical testbed YAML:
    tacacs/username
    passwords/linux


Dyntopo Clean YAML Schema
-------------------------

.. code-block:: yaml

    log_level: # One of (error, warning, info, debug, critical)
               # May be specified in UPPERCASE or lowercase.
               # (default: warning)
               # (optional)

    max_launch_time_minutes: # Maximum number of minutes before
                             # an attempt to launch a dynamic topology is
                             # aborted.  This can include time spent waiting
                             # for a reservation to be confirmed.
                             #
                             # NOTE: This parameter does not apply when the
                             # topology is being brought up using the
                             # standalone tool.
                             #
                             # NOTE: Please be aware that if the clean
                             # scope is set to 'task' then the existing
                             # easypy task run() API also allows a
                             # max_runtime parameter (measured in seconds)
                             # to be specified.
                             # (default: 960 minutes)
                             # (optional)

    generate_legacy_credentials: # If True, generate legacy-style
                                 # tacacs and passwords blocks.
                                 # If False, then generate credentials block.
                                 #
                                 # This key is not used by the dyntopo.xrut
                                 # orchestrator.
                                 #
                                 # The dyntopo.local orchestrator uses this
                                 # key to set the user input expectation
                                 # for routem device authentication, if
                                 # True then legacy password/tacacs blocks
                                 # are expected, and if False then a
                                 # credential block is expected.
                                 #
                                 # (Optional)
                                 # (Default : True)


    laas: # Configuration for a LaaS-NG backend

        vmcloud_server: # The name of the VmCloud server on which
                        # to launch the requested topology.
                        # Additional VmCloud server configurations are
                        # specified in the testbed topology under
                        # servers/<vmcloud_server_name>.
                        # (mandatory)

        lab_domain: # Lab domain containing reservable physical
                    # devices.
                    # (defaults to the lab domain set on the
                    # vmcloud server under the file name
                    # /etc/vmcloud/vmcloudrc).
                    # (optional)

        max_lifetime_minutes: # Maximum number of minutes before
                              # a dynamic topology automatically
                              # tears itself down after it is
                              # reserved.
                              #
                              # NOTE: Please be aware that if the clean
                              # scope is set to 'task' then the existing
                              # easypy task run() API also allows a
                              # max_runtime parameter (measured in seconds)
                              # to be specified.
                              # (default: 480 minutes)
                              # (optional)

        remote_copy: # If specified as True, copy all virtual device
                     # images to the vmcloud server before launching the
                     # topology, and remove the images from the server
                     # after tearing down the topology.
                     # This allows bringing up automounted images
                     # on a vmcloud server without automount capabilities.
                     # NOTE: This is the preferred option for bringing up
                     # crypto images on a LaaS backend, since these typically
                     # cannot be brought up directly from an automount.
                     # If specified as False, do not copy the images
                     # (assume the images are accessible both on
                     # the execution server and the LaaS server).
                     # This is the most time efficient option but may not
                     # work on all servers for all image types.
                     # (default: True)
                     # (optional)

        ext_itf: # External access interface default configuration.
                 # Specifying this key makes connections possible between
                 # virtual devices inside a LaaS topology
                 # and devices outside that topology.
                 # If not specified, the default for name still
                 # applies if referenced by the logical testbed configuration
                 # key /topology/links/<link_name>/ext_itf.
                 # (optional)

           name: # External access interface name.
                 # (default: eth1)
                 # (optional)

           mgt: # If specified as True, the vmcloud server must connect
                # all virtual device management interfaces to the
                # indicated external access interface.
                # Only some devices (such as XR and NX) have
                # explicitly named management interfaces (such as mgmt0).
                # Some devices (such as XE) that do not have an explicitly
                # named management interface would not be covered
                # by this option.
                # Management interfaces never appear in the actual
                # testbed topology block.
                # (default: False)
                # (optional)

        disable_netclean: # If set to True, the netclean option will be 
                          # disabled

        disable_power_reset: # If set to True, the power reset option 
                             # will be disabled


    xrut: # Configuration to bring up a dynamic topology on an XR-UT
          # backend.
          # (optional)

        base_dir   # The base directory of the XR-UT toolchain to
                   # use to spawn dynamic topologies.
                   # (default: /auto/xrut/xrut-gold)
                   # (optional)

        workspace: # Directory containing built images.
                   # XR-UT also populates this directory with metadata
                   # required for connection.
                   #
                   # The workspace may be specified in an environment
                   # variable named "XRUT_WS" if the user doesn't want
                   # to place this information in the clean YAML file.
                   #
                   # (required if enxr logical devices are requested,
                   # otherwise, optional)

        sim_dir: # XR-UT populates this directory with copied images and
                 # metadata required for connection.
                 # (defaults to current working directory)
                 # (optional)

        default_device_type : # One of the following:
              # (iol, iol_pagent, ios_dynamips, ios_dynamips_pagent,
              # iosv, iosv_pagent, enxr, iosxrv, nxosv, csr1000v)
              # (defaults to the type of the first device in the
              # testbed configuration YAML with
              # "logical: True" specified)
              # (optional)

        dynamips_idlepc: # This block contains the idlepc value to use.
                         # These values are tied to the particular IOS
                         # Dynamips image being used.
                         #
                         # If a Dynamips IOS image is launched with a
                         # mismatching IdlePc value, the image will
                         # continually consume 100% of the CPU
                         # it is running on.
                         #
                         # They may be specified in environment variables
                         # named "<platform>_dynamips_idlepc" in case the
                         # user doesn't want to place all this information
                         # in the clean YAML file.
                         # For example :
                         # export ios_pagent_dynamips_idlepc=0x60612868
                         #
                         # NOTE: Some IOS Dynamips image names contain the
                         # idlepc as a suffix, in this case XR-UT will
                         # auto-detect the idlepc value and it does not
                         # have to be specified separately.
                         # (optional)

            ios: int # (optional)
            ios_pagent: int # (optional)

        log_level: # One of (quiet, info, debug)
                   # XR-UT still generates important notes when in
                   # quiet mode.
                   # May be specified in UPPERCASE or lowercase.
                   # (default: quiet)
                   # (optional)

        xrvr_nic_type : # An XRVR NIC type (e1000, virtio)
                        # (default: e1000)
                        # (optional)

        vmcloud_server: # The name of the VmCloud (LaaS) server on which
                        # to launch the requested topology.
                        # Additional VmCloud server configurations are
                        # specified in the testbed topology under
                        # servers/<vmcloud_server_name>.
                        # (optional)

        iol_flags: # Extra flags to pass to IOL instances when they are
                   # launched (ie. "-console_timeout 1000").

        moonshine_host: # The Moonshine host to use.
                        # This must be a host machine which supports
                        # launching Moonshine, e.g. a LaaS or UCS machine.
                        # See https://confluence-eng-sjc1.cisco.com/conf/display/ENXR/Moonshine
                        # for more information about the Moonshine platform.
                        #
                        # (required if moonshine logical devices are requested,
                        # otherwise, optional)

        moonshine_dir: # The base Moonshine working directory to use on the
                       # Moonshine host. Defaults to /nobackup/$USER.
                       # A unique directory name is appended to this for
                       # each run, to avoid conflicts from multiple runs.
                       # See https://confluence-eng-sjc1.cisco.com/conf/display/ENXR/Moonshine
                       # for more information about the Moonshine platform.
                       # (optional)

        pass_through: # A set of parameters to be sent directly to XR-UT.
                      # WARNING : This is an advanced option.
                      # It is possible to specify parameters that directly
                      # conflict with orchestrator-formed parameters.
                      # Example : --parameter1=value1 --parameter2=value2


    # NOTE: The XR-UT orchestrator allows platform images to be specified
    # in an environment variable named "<platform_name>_image"
    # in case the user doesn't want to place image names in the clean YAML file.
    #       For example :
    #       export ios_pagent_image=/path/to/ios_pagent_img
    #       export xrvr_rp_image=/path/to/xrvr_rp_img
    #       export xrvr_lc_image=/path/to/xrvr_lc_img
    #       export ultra_image=/path/to/xrvr_lc_img
    #       export moonshine_image=/path/to/moonshine_img
    #
    # The Moonshine host and directory parameters may also be specified in
    # environment variables named "moonshine_host" and "moonshine_dir":
    #       export moonshine_host=your_ucs
    #       export moonshine_dir=/nobackup/username/moonshine_dir
    #
    # Pass-through XR-UT parameters may be specified in the environment
    # variable "bringup_xrut_pass_through".

    vxr: # Configuration for a VXR backend

        sim_host: # The name of the VXR capable server on which to launch the
                  # requested topology.
                  # (optional)
                  # (default: a server allocated from Vxr SLURM cloud)

        sim_rel: # The path to a VXR release to be used to launch vxr
                 # simulation. Official vxr releases are located under:
                 # /auto/vxr/vxr2_user. The 'alpha' soft link
                 # points to the most recent official release.
                 # (optional)
                 # (default: chosen by vxr backend based on image type)

        sim_host_username: # The username that will be used to log on to
                           # the simulation host
                           # (default: current user)
                           # (optional)

        sim_host_password: # The password that will be used to log on to
                           # the simulation host
                           # (default: empty string to indicate password-less
                           # ssh)
                           # (optional)

        sim_dir: # The directory on the simulation server where the simulation
                 # will run.
                 # (default: /nobackup/<sim_host_username>/pyvxr)
                 # (optional)

        skip_auto_bringup: # Indicate whether or not to skip automatic
                           # bringup of all devices to a testable state.
                           # For most XR devices, a testable state is reached
                           # when XR reaches ios prompt
                           # (default: False)
                           # (optional)

        pyvxr_flags: # Pass custom pyvxr flags
                     # (default: {})
                     # (optional)

        slurm_flags: # Pass slurm specifc pyvxr flags
                     # These flags are relevant only when `sim_host`
                     # is not explicitly specified (defaulting to a dynamically
                     # allocated slurm server)
                     # (optional)
                     # (default: {})

                cluster: # Slurm cluster to use
                         # (optional)
                         # (default: m2)

                hours: # Number of reservation hours
                       # (optional)
                       # NOTE: slurm limit is 120 hours (5 days)
                       # (default: 24)

                partition: # Slurm cluster partition
                           # (optional)
                           # (default: slurm)

                node: # A specific slurm node to target
                      # (optional)
                      # (default: any slurm node in the cluster/partition)

                cores: # The number of cores to reserve
                       # (optional)
                       # (default: estimated based on the router topology)

                distributed: # Whether or not to enable distributed slurm
                             # simulation
                             # (optional)
                             # (default: False)

                pending_timeout: # The max number of minutes to wait for a
                                 # PENDING slurm reservation to become active
                                 # (optional)
                                 # (default: 5)


        remote_copy: # Whether or not to first copy images to the
                     # simulation directory on the simulation server.
                     # If specified as `False`, images will not be
                     # copied to the simulation directory. In that
                     # case, it is assumed that the server already has
                     # access to user-specified images.
                     # NOTE: ixia and spirent images will not be
                     # copied to the simulation directory regardless
                     # of this flag. The path to ixia and spirent
                     # images must be accessible from the simulation
                     # directory on the simulation server.
                     # (optional)
                     # (default: True)

    local: # Configuration for the dyntopo.local backend.

        sim_dir: # Directory to run local devices in.
                 # Defaults to /tmp/dyntopo_iol_sim_dir

        iol_flags: # Extra flags to pass to all IOL instances.
                   # These flags are only passed to IOL RPs, and not to
                   # dIOL CI devices.
                   # (optional)
                   # example : -m 1024

        iourc: # Location of the iourc file to use.
               # (optional)
               # If not specified, defaults to the value of the $IOURC
               # environment variable, or if not set, to the file $HOME/.iourc,
               # or if not set, tries to use the one from ~/.iourc
               # If no iourc file is found, the orchestrator will attempt to 
               # generate one.

        remote_copy: # If specified as True, copy all images locally before
                     # launching the topology, and remove the images after
                     # tearing down the topology.
                     # A unique directory is created under
                     # /tmp/local_images* to hold the image and is removed
                     # when the topology is torn down.
                     # If specified as False, do not copy the images locally.
                     # (optional)
                     # (default: True)


.. _dyntopo logical testbed schema:

Dyntopo Logical Testbed Schema
==============================

The `Logical Testbed File`_ specified by the
``-logical_testbed_file`` parameter is expected to conform to the
following schema, which is an extension of the
`Logical Testbed Schema`_:

.. _Logical Testbed Schema: https://wiki.cisco.com/display/PYATS/Kleenex+Bringup+Documentation#KleenexBringupDocumentation-LogicalTestbedSchema

.. _Logical Testbed File: https://wiki.cisco.com/display/PYATS/Kleenex+Bringup+Documentation#KleenexBringupDocumentation-LogicalTestbedFile



.. code-block:: yaml

    # devices block
    # -------------
    #   all testbed devices are described here
    devices:
        <device_name>

            type:   # device type generic string
                    # use this to describe the type of device
                    # The meaning of this type depends on the bringup
                    # orchestrator used.
                    # (required)
                    #
                    # If "logical: True" and the XR-UT orchestrator is
                    # being used then only the following logical virtual
                    # router types are accepted:
                    # (iol, iol_pagent, ios_dynamips, ios_dynamips_pagent,
                    # iosv, iosv_pagent, enxr, iosxrv, nxosv, csr1000v,
                    # moonshine)
                    #
                    # If "logical: True" and the LaaS-NG orchestrator is
                    # being used, then this key is used to declare the
                    # requested device or hierarchy pattern to match against
                    # the requested lab domain's profile hierarchy.
                    # NOTE: The LaaS-NG orchestrator also accepts
                    # the following virtual router types:
                    # iosv, iosv_pagent, nxosv, iosxrv, iosxrv9k, csr1000v.
                    # If the type is not one of the supported virtual router
                    # types, it is assumed to be a physical device name
                    # or hierarchy pattern.
                    #
                    # If "logical: True" and the VXR orchestrator is
                    # being used then only the following logical virtual
                    # router types are accepted:
                    # (iosxrv9k, asr9k, spitfire_f, spitfire_d, ixia, spirent,
                    # iosxrv, linux)
                    #
                    # If "logical: True" and the local orchestrator is
                    # being used then only the following logical virtual
                    # router types are accepted:
                    # (iol, routem)

            multinode_requested: # Request separate line cards.
                        # If True, and if "logical: True" is also specified,
                        # then the orchestrator must bind this logical device
                        # to a device capable of terminating its interfaces on
                        # separate line cards.
                        #
                        # If False, then the orchestrator must bind this
                        # logical device to a device where all interfaces
                        # terminate directly on the route processor itself.
                        #
                        # This key is recognized by the XR-UT orchestrator.
                        # It is also recognized by the LaaS orchestrator
                        # for the following virtual devices : iosxrv.
                        #
                        # (optional)
                        # (default: False)


            ha_requested:  # If True, and if "is_logical: True" is also
                           # specified, then the orchestrator must bind this
                           # logical device to a HA-capable device.
                           #
                           # If False, then the orchestrator must bind this
                           # logical device to a simplex (non-HA) device.
                           #
                           # This key is recognized by the XR-UT orchestrator,
                           #
                           # It is also recognized by the LaaS orchestrator
                           # for the following virtual devices : iosxrv.
                           #
                           # It is also recognized by the local orchestrator
                           # for the following virtual devices : iol.
                           #
                           # It is also recognized by the Vxr orchestrator
                           # for the following virtual devices : spitfire_d,
                           # asr9k.
                           #
                           # (optional)
                           # (default: False)

            vxr: # Configuration for a VXR device

                sim_host: # Simulation server override for this device.
                          # Should be specified only if distributed simulation
                          # is desired.
                          # (default: value of clean file key
                          # /bringup/BringUpWorker/vxr/sim_host)
                          # (optional)

                memory: # A 'human readable' (e.g. 40M, 5G, etc) string that
                        # represents the amount of virtual memory to be
                        # allocated for this device.
                        # (default: platform specific)
                        # (optional)

                vcpu: # An integer value that indicates the number of virtual
                      # cores # allocated for this device.
                      # (default: platform specific)
                      # (optional)

                cvac: # Path to a CVAC (Cisco Virtual Appliance Configuration)
                      # file to be used to configure this device (valid for
                      # iosxrv9k platform only). For more information see:
                      # https://wiki.cisco.com/display/SUNSTONE/Sunstone+and+CVAC+-+bootstrap+CLI
                      # NOTE: unlike device images, the cvac file is not copied
                      # to the remote simulation server. Therefore, the cvac
                      # file path must be accessiable on the simulation server
                      # from the simulation directory
                      # (optional)

                cpu_pin: # A comma separated list of the UCS cores to which the
                         # virtual cores (vcpus) will be 'pinned'. For example,
                         # [0,1,2,3] will pin the first 4 virtual cores of this
                         # device to the UCS cores 0,1,2, and 3.
                         # NOTE: valid for iosxrv9k platform only.
                         # (optional)

                host_pci: # A comma separated list of pci-passthrough devices
                          # for iosxrv9k routers (e.g [02:00.0, 03:00.0,
                          # 04:00.0])
                          # NOTE: root privilages required on the simulation
                          # server (these are specified via sim_host_username,
                          # and sim_host_password in the 'simulation' section)
                          # NOTE: valid for iosxrv9k platform only
                          # For more informattion on iosxrv9k pci-passthrough
                          # see:
                          # https://wiki.cisco.com/display/SUNSTONE/How+to+map+NIC+to+PCI+ID
                          # (optional)

                dual_rp: # Indicate whether or not to use a standby RP.
                         # (asr9k and spitfire_d platforms only)
                         # (optional)
                         # (default: False)

                linecard_slots: # A comma separated list of integers to denote
                                # which slots the available LCs are inserted
                                # into (e.g. [0,2])
                                # NOTE: valid for spitfire_d platform only
                                # (optional)
                                # (default: [0])

                data_interface_order: # An ordered list of the data interfaces
                                  # used in the logical testbed file for this
                                  # device. The order is used to map a logical
                                  # interface name to a specific data port of
                                  # the simulated device. For example,
                                  # [foo , bar] will map in the following way:
                                  # spitfire f/d and asr9k platform:
                                  # foo -> first front panel port
                                  # bar -> second front panel port
                                  # iosxrv9k:
                                  # foo -> first data vNic
                                  # bar -> second data vNic
                                  # ixia/spirent:
                                  # foo -> first tgen data port
                                  # bar -> second tgen data port
                                  # (optional only if no intefaces are declared
                                  # for this device in the logical testbed file)

            local:         # Configuration for the dyntopo.local orchestrator.

                arguments: # String containing arguments to pass to the program
                           # when launching the device.
                           # Optionally, for devices with type routem, may
                           # contain one of the following tags:
                           # {appid} : expands to the dynamically generated
                           #           netio appid.
                           # {port} :  expands to the dynamically generated port
                           #           used to log into the device.
                           # (optional)
                           # Example : -m 512

                link_files: # list of files to link into the directory where
                            # this device is run.
                            # (optional)

                max_interfaces: # Maximum number of interfaces supported.
                                # Applies only to devices with type 'routem'.
                                # (optional)
                                # (default: 3)

                iol_flags: # Extra flags to pass to this IOL device.
                           # These flags are only passed to IOL RPs, and not to
                           # dIOL CI devices.
                           # (optional)
                           # example : -m 1024


            laas:          # Configuration for the dyntopo.laas orchestrator.

                autoclean: # Content that is merged into the autogenerated
                           # uniclean content produced by the orchestrator.
                           # Uniclean is used to wait for newly launched
                           # virtual devices to come up and undergo initial
                           # configuration.
                           # (optional)
                           #
                           # Example :
                           # autoclean:
                           #     uniclean:
                           #         settings:
                           #             PRE_INITIAL_CONNECT_DELAY_SEC: 600
                           #             PRE_DEVICE_CHECK_DELAY_SEC: 240




    # topology block
    # --------------
    #   describes the actual or logical interfaces and links
        topology:

            links:
                # This section describes additional/custom values for a named
                # link.
                # (optional)

                <name>: # Link name.  Each link that has extended descriptions
                        # needs to have its own section under links.
                        # (optional)

                        type: # Allowable values are L1 or L2
                              # If L1 specified, the link is constrained to be
                              # a layer 1 (physical) link.
                              # If L2 specified, the link is constrained to be
                              # a layer 2 (bridged or switched) link.
                              # Currently, only the LaaS orchestrator
                              # recognizes this key, and only on links
                              # connecting physical devices.
                              # Mixed case is allowed.
                              # (optional)
                              # (default: L2)

                        speed: # Allowable values are 1G or 10G
                               # Currently, only the LaaS orchestrator
                               # recognizes this key, and only on links
                               # connecting physical devices.
                               # type: L1 must be specified in order to
                               # use this key.
                               # Mixed case is allowed.
                               # (mandatory if type: L1 specified)

                        media: # Allowable values are RJ45 or Optical
                               # Currently, only the LaaS orchestrator
                               # recognizes this key, and only on links
                               # connecting physical devices.
                               # type: L1 must be specified in order to
                               # use this key.
                               # Mixed case is allowed.
                               # (optional)
                               # (default: RJ45)

                        ext_itf: # External access request.
                                 # Specifying this key makes connections
                                 # possible between virtual devices inside a
                                 # LaaS topology and devices outside that
                                 # topology.  The vmcloud server must connect
                                 # all interfaces connected to this link to the
                                 # indicated external interface.
                                 # It is acceptable to specify this key
                                 # without a value, the default name is
                                 # still applied as described below.
                                 # Currently, only the LaaS orchestrator
                                 # recognizes this key.
                                 # (optional)

                           name: # External access interface name.
                                 # (default: value of clean file key
                                 # /bringup/BringUpWorker/laas/ext_itf/name)
                                 # (optional)

                        mgt: # If specified as True, this link is
                             # considered a management link and logical virtual
                             # device interfaces connected to it do not appear
                             # in the actual testbed topology block.
                             # Interfaces on platforms with or without
                             # a dedicated management interface are
                             # allowed to connect to such a link.
                             # Currently, only the LaaS orchestrator
                             # recognizes this key.
                             # (default: False)
                             # (optional)

                        port_channel : # Name of this link's port channel.
                                       # A port channel allows multiple
                                       # L2 links to be aggregated into
                                       # a single logical link.
                                       # This key may be specified with
                                       # topology/devices/<device>/
                                       # interfaces/<interface>/channel_mode.
                                       #
                                       # Currently, only the LaaS orchestrator
                                       # recognizes this key and only on
                                       # point-to-point physical device links.
                                       # (optional)

            <device>:   # each device's interface/link gets its own block named
                        # using the device name/hostname. the device mentioned
                        # here must be also described under the device block.
                        # (optional)

                interfaces: # begin the device interface description section
                            # (required)

                    <intfname>: # each device interface requires its own
                                # section under the interfaces block
                                # interface names must be unique per device.
                                #
                                # If the device has "logical: True" in its
                                # devices: block, then this interface name is
                                # to be interpreted as a logical interface
                                # name.
                                # The orchestrator is responsible for binding
                                # this interface name to an actual interface
                                # name.
                                # (optional)

                        actual_name: # Actual interface name to use
                                     #
                                     # If not specified, the orchestrator
                                     # is responsible for choosing a
                                     # platform-appropriate actual interface
                                     # to bind with the requested
                                     # logical interface.
                                     #
                                     # If specified, the orchestrator must
                                     # bind this logical interface to
                                     # the indicated actual interface name.
                                     # The user is responsible
                                     # for ensuring that the requested name is
                                     # platform-appropriate.
                                     # (optional)

                        channel_mode: # Requested Port Channel mode for an
                                      # interface connected to an L2 link.
                                      # Some examples of supported values
                                      # include auto, desirable, active
                                      # and passive.
                                      #
                                      # If specified, the port channel this
                                      # interface's link belongs to must
                                      # also be specified via the
                                      # links/<link_name>/port_channel
                                      # key/value pair.
                                      #
                                      # Currently, only the LaaS orchestrator
                                      # recognizes this key and only on
                                      # point-to-point physical device links.
                                      #
                                      # (default: active)
                                      # (optional)


.. note::
    Only the LaaS orchestrator pays attention to the
    ``servers/name/<server_name>/laas/notification_port`` key
    as described in :ref:`schema`.


.. warning::

    When specifying ``actual_name`` for a virtual logical device, a user
    must specify ``actual_name`` for all the device's interfaces.
    Mixing and matching user-assigned and orchestrator-assigned interface names
    is not supported.


.. _dyntopo actual testbed schema:

Dyntopo Actual Testbed Schema
=============================

The actual testbed configuration generated by the orchestrator follows the
:ref:`schema`.  This section provides more details about fields that the
orchestrators populate.  For more details, please refer to
`How Actual Testbed Configuration is Built`_.

.. _How Actual Testbed Configuration is Built: https://wiki.cisco.com/display/PYATS/Kleenex+Bringup+Documentation#KleenexBringupDocumentation-HowActualTestbedConfigurationisBuilt

.. code-block:: yaml

    # devices block
    # -------------
    #   all testbed devices are described here
    devices:
        <device_name>

            clean:  # Autogenerated static clean block for device

                mgt_itf: # Management interface details
                         # populated by the LaaS orchestrator.
                         # Users would typically need to reference this data
                         # when populating their post-clean configuration.

                    name: # The name of the virtual or physical device's
                          # management interface.  For devices such as XR/NX,
                          # this is the name of the dedicated management
                          # interface (such as MgmtEth0/RP0/CPU0/0 or mgmt0).
                          # For devices such as XE, this key is populated
                          # only when the user defines a link
                          # with key mgt: True and connects an interface
                          # to that link.

                    ipv4: # Details of the IPv4 managment interface

                        address: # The physical device's IP address
                                 # in string form.

                        net: # The physical device's management subnet.

                            mask: # A string representation of the network
                                  # (for example, 255.255.255.0).

                            prefixlen: # The prefix length of the network
                                       # (for example, 24).

                        gateway_address: # The physical device's IPv4 gateway
                                         # address in string form.


            auto_bringup:
                # section containing key/value pairs autopopulated by
                # the LaaS orchestrator to describe how it brought
                # the device to a testable state.

    topology:
        <device_name>:
            interfaces:
                <interface_name>:
                    type : # The LaaS orchestrator forces any
                           # physical interface connected to a
                           # non-management external link to have a type
                           # of "ext" to show that this interface does not
                           # connect topology devices together, but rather
                           # connects topology devices to the outside world.
