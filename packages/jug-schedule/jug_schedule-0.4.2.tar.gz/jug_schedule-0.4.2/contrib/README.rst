Contributed and helper scripts
==============================

find_drmaa
----------

This script performs a system scan in search of ``libdrmaa.so``.

If found, a file ``~/.libdrmaa/<hostname>``, where ``hostname`` is the name of the machine where the command was run, is created.

You can then easily source (sh/bash/zsh only) the created file to have ``DRMAA_LIBRARY_PATH`` set on your shell environment.
