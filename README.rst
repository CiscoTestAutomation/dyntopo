dyntopo - Dynamic Topology Orchestrators for pyATS
==================================================

This file is included with the dyntopo namespace package
and provides detailed instructions on how to add new orchestrator packages.

.. note::

        For better viewing/reading of this document, use restview_.

        .. _restview: https://pypi.python.org/pypi/restview

        For example::

            restview -l 0:8080 README.rst

        And then browse to http://your_machine:8080



Here is the location of the dyntopo `online documentation`_.

For architectural and design details, please refer to the
 `dyntopo plugin designers guide`_.

.. _dyntopo plugin designers guide:  https://wiki.cisco.com/pages/viewpage.action?pageId=50886280

.. _online documentation: http://wwwin-pyats.cisco.com/cisco-shared/html/dyntopo/docs/index.html

.. _pyATS argument propagation policy: http://wwwin-pyats.cisco.com/documentation/html/easypy/usages.html#argument-propagation

.. _cisco-shared: http://wwwin-pyats.cisco.com/cisco-shared/html/README.html

Contribute to documentation
---------------------------

To contribute, you need to fork the repository, do your modifications and create a new pull request. 

.. note:: 
        
        **Please make sure you have the full pyats package installed via ```pip install pyats[full]```.**

To build the docs locally on your machine. Please follow the instructions below 

  - Go to the `dyntopo Github repository <https://github.com/CiscoTestAutomation/dyntopo>`

  - On the top right corner, click ```Fork```. (see `<https://help.github.com/en/articles/fork-a-repo>`)
  
  - In your terminal, clone the repo using the command shown below: 
    ```shell
    git clone https://github.com/<your_github_username>/dyntopo.git
    ```

  - ```cd dyntopo/docs```
  
  - Use ```make install_build_deps```  to install all of the build dependencies
  
  - Run ```make docs``` to generate documentation in HTML

  - Wait until you see ```Done``` in your terminal
  
  - The documentation is now built and stored under the directory 
  ```unicon.plugins/__build__```

  - Run ```make serve``` to view the documentation on your browser

    - Please create a PR after you have made your changes (see [commit your changes](https://pubhub.devnetcloud.com/media/pyats-development-guide/docs/contribute/contribute.html#commit-your-changes) & [open a PR](https://pubhub.devnetcloud.com/media/pyats-development-guide/docs/contribute/contribute.html#open-a-pull-request))

Here are a few examples that could be great pull request:

- Fix Typos
- Better wording, easier explanation
- More details, examples
- Anything else to enhance the documentation


How to contribute to the pyATS community
----------------------------------------

- For detail on contributing to pyATS, please follow the [contribution guidelines](https://pubhub.devnetcloud.com/media/pyats-development-guide/docs/contribute/contribute.html#)


Developer's Guide
-----------------
This guide contains details on how to extend dyntopo with new platforms,
capabilities and device platform types.


Adding a new Orchestrator
^^^^^^^^^^^^^^^^^^^^^^^^^
There are a few things to keep in mind when you want to add a new orchestrator:

- Be aware of cisco-shared_ policies.

- Use the ``laas`` module as a template, create new directory
  ``dyntopo/<your_orch_name>/src/dyntopo/<your_orch_name>``. Your orchestrator
  code, examples, tests and README.rst are placed under this directory.

- Please ensure you place your examples under the following directory:
  ``dyntopo/<your_orch_name>/src/dyntopo/<your_orch_name>/examples/dyntopo_<your_orch_name>``.
  This allows for consistency among user plugins, as examples are automatically
  written into the top-level ``examples`` directory in the pyATS workspace
  where ``dyntopo`` is pip-installed.

- Create a new directory 
  ``dyntopo/<your_orch_name>/docs``. 

- Create softlinks ``dyntopo/<your_orch_name>/examples``, 
  ``dyntopo/<your_orch_name>/tests`` and
  ``dyntopo/<your_orch_name>/README.rst``.

- Update the top-level ``dyntopo/Makefile`` and ``dyntopo/setup.py``
  with your orchestrator.

- Add a softlink ``dyntopo/docs/<your_orch_name>``. Link your documentation
  to the top-level ``dyntopo/docs/index.rst``.

- You must inherit from ``ats.kleenex.BringUpWorkerBase`` and call
  the parent ``__init__`` in the first line of your ``__init__``.

- You should inherit from ``ats.kleenex.ArgvQuotingParser`` as it provides
  extra debugging in the event an exception is thrown in CLI argument
  processing.

- You should use ``ats.kleenex.parse_cli_args`` as all required common
  logic is provided for you, this adheres to the
  `pyATS argument propagation policy`_.

- You should use exceptions such as ``ats.kleenex.TopologyDidntComeUpInTime``
  as they provide a consistent way of reporting issues common to multiple
  orchestrators.

- Expect ``ats.kleenex.SignalError`` to be raised at any time as part of
  pyATS core bringup's signal handling model.

- You must implement ``_launch_topology`` and ``_tear_down_topology``
  which are asyncio coroutines.

- You must define a CLI parser that contains the same parameter names as
  those in your ``__init__`` prototype (as per
  `pyATS argument propagation policy`_.
  Any parameter specified via CLI must override parameters given in the
  constructor.  Any internal parameters that don't directly face the user
  may be excused from this policy as long as they are documented.

- You must implement a version of ``main.py`` that auto-assigns the
  ``-orchestrator``
  input to the pyATS core bringup tool to your worker class, think up a
  name for your decoupled bringup tool and update setup.py entry_points.
  Have your tool's ``main`` call ``ats.kleenex.main()``.
  Ensure the tool name ends with the characters ``bringup`` so that the
  ``-orchestrator`` parameter does not appear in the tool's ``-help`` display.

- You must provide in the ``console_scripts`` section of ``setup.py`` an
  entry defining the decoupled bringup tool name to use for your orchestrator.
  The name of this tool must be of the form ``xxxbringup``, where ``xxx`` is
  the name of your orchestrator.

- You must check ``self.help`` and follow the appropriate logic path when
  bringup is being run via a decoupled tool in ``-help`` mode.  Typically
  this means skipping bringup altogether.

- You must implement ``update_help`` so that your decoupled bringup tool will
  have a correct help display.

- You must identify those CLI parameters that have an equivalent in the
  clean schema, and must tag them with ``help_suppress_kleenex`` when
  adding arguments to your orchestrator's CLI command parser.

- You must implement ``_set_log_level`` and set the log level of all your
  modules.

- You must provide the actual-to-logical device name translation
  by populating ``self.dev_name_xref`` prior to calling ``_process_tb_config``.

- You must call ``self._process_tb_config`` when the actual topology
  configuration is ready to be handed off to pyATS core bringup for
  post-processing and ultimate exposure to the user.

- Add new configuration keys to
 ``dyntopo/common/src/dyntopo/common/schema.py`` for your orchestrator and
  ensure you validate clean configuration by calling
  ``config_loader.load(self.clean_config)`` and update the common/schema
  documentation.

- If you introduce new orchestrator-specific keys into the logical topology
  schema, be sure to document them and append them to the worker's
  ``self._logical_device_keys_to_ignore`` and
  ``self._logical_interface_keys_to_ignore`` members to ensure they are
  not merged into the final testbed content.  Don't forget to update the
  common/schema documentation.

- Make sure that if you need to raise an exception in the worker's
  constructor that you call ``self._raise_exception(exception)`` to ensure the
  worker is shut down properly.

- Make sure that if you need to raise an exception in any worker coroutine
  that you call ``self._store_exception(exception)`` to store the exception
  for later processing.

- Ensure you add a timer for max_launch_time_minutes handling.   See other
  orchestrators for implementation details.
