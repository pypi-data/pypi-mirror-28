About
=====

| **jug_schedule** is a `jug <https://github.com/luispedro/jug>`_ subcommand that provides automatic deployment to queueing systems.
| Currently supports **SGE/GE** (Grid Engine), **LSF** (IBM LSF), and **SLURM**.

This project is currently experimental so bug reports are welcome.

Requirements
------------

This project depends on `drmaa <https://github.com/pygridtools/drmaa-python>`_ and obviously `jug <https://github.com/luispedro/jug>`_.

Installation
------------

Install **jug_schedule** with::

    pip install jug-schedule

or from Anaconda with::

    conda install -c unode jug-schedule

and then simply add the following to your ``~/.config/jug/jug_user_commands.py``::

    try:
        from jug_schedule.schedule import ScheduleCommand
        schedule = ScheduleCommand()
    except Exception as e:
        import sys
        sys.stderr.write("Couldn't import schedule, error was {0}\n".format(e))

If you are running directly from git you can instead use::

    import sys

    sys.path.insert(0, "/path/to/clone/of/jug_schedule/")

    try:
        from jug_schedule.schedule import ScheduleCommand
        schedule = ScheduleCommand()
    except Exception as e:
        sys.stderr.write("Couldn't import schedule, error was {0}\n".format(e))

.. note::
    If you have never setup **DRMAA** on your environment, check the *Configuration* section below.

Usage
-----

If installed properly, running ``jug`` should now include a ``schedule`` subcommand.

Running it will try to detect a queueing system and submit jobs to it.
``jug schedule`` will only produce warning and errors. Use ``--verbose debug`` for detailed messages.

``jug status`` will behave as usual and is the recommended way to check progress of execution.

Script
^^^^^^

If your system requires additional setup for jug to run on remote servers you will need to use the `--script` option.
The script should call `jug` with all given arguments. As an example::

    #!/usr/bin/env bash

    # Enabling modules (http://modules.sourceforge.net/) in the current shell
    if [ -f /etc/profile.d/modules.sh ]; then
        source /etc/profile.d/modules.sh
    fi

    # Loading (ana)conda
    module add conda
    # and an environment called py3 where jug was installed
    source activate py3

    # Then calling jug with all given arguments. Make sure to keep the quotes on $@
    jug "$@"

Assuming the above content is saved in a file `script.helper` you can then call::

    jug schedule --script script.helper

if instead you give it the same name as your jugfile it will be automatically loaded::

    $ ls
    myjugfile.helper myjugfile.py
    $ jug schedule myjugfile.py  # <- will use myjugfile.helper


Configuration
-------------

**jug_schedule** relies on **DRMAA** for interaction with the queueing system.

| **DRMAA** support is limited and its quality varies considerably across platforms.
| Currently supported platforms include **LSF**, **SGE** and **SLURM**.

In order to use ``jug_schedule`` your environment needs to define ``DRMAA_LIBRARY_PATH``.
If running ``env | grep DRMAA_LIBRARY_PATH`` returns no match, ask your system administrators for the location of this library.

Then use::

    export DRMAA_LIBRARY_PATH=/path/to/libdrmaa.so

You only need to set this option on the environment that runs ``jug schedule``.

.. note::
    You can also use ``contrib/find_libdrmaa`` to locate ``libdrmaa.so`` on your system.
    Check the ``README`` inside the ``contrib/`` folder for more information.

Resources
---------

An additional feature of **jug_schedule** is the ability to define job resources.

If you already know jug's ``TaskGenerator`` decorator you can simply replace it with the following where applicable::

    from jug_schedule.resources import ResourcesTaskGenerator

    @ResourcesTaskGenerator(cpu=10, mem=100, queue="default")
    def func(...):
        ...

Supported arguments include: ``cpu``, ``mem`` (in MB), ``queue`` and ``custom`` for arbitrary options.

.. note::
    When using ``custom``, be aware that providing invalid or misformatted options may cause crashes.
    SLURM is a known offender as reported `on this issue <https://git.io/vQzY7>`_.

Command-line options
--------------------

The following options are available::

    --script            - command used to run jug on the cluster. Point this to a shell script if you need to setup jug's environment prior to execution
    --max-jobs          - how big is the pool of jug jobs (max number of simultaneous jobs)
    --max-array         - when submitting jobs to the queue system, limit the maximum number of jobs per submission
    --logs              - where to write job logs. Defaults to a directory 'jug_logs' in the current directory.
    --cycle-time        - how many seconds to wait between every interaction with the queue system. Defaults to 60
    --stop-on-error     - jug_schedule will continue until all jobs fail. Default is to continue queueing jobs when a job fails.
    --recycle           - when a job fails, instead of removing one job from the pool, recycle it and keep the pool size constant.


