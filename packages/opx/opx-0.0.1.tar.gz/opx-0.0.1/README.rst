OpenSwitch Development Tool
===========================

-----

.. contents:: **Table of Contents**
    :backlinks: none

Installation
------------

opx is distributed on `PyPI <https://pypi.org>`_ as a universal
wheel and is available on Linux/macOS and Windows and supports
Python 3.6+ and PyPy.

.. code-block:: bash

    $ pip install opx

Requirements
~~~~~~~~~~~~

- `Docker <https://docs.docker.com/engine/installation/>`_
- `Repo <https://source.android.com/setup/downloading#installing-repo>`_

Getting Started
---------------

.. code-block:: bash

    $ opx init
    $ opx build

Command Line Completion
-----------------------

Run the command corresponding with your shell. Add to your shell startup file for persistent autocomplete.

.. code-block::

    # bash
    eval "$(_OPX_COMPLETE=source-bash opx)"

    # zsh
    eval "$(_OPX_COMPLETE=source-zsh opx)"

    # fish
    eval (env _OPX_COMPLETE=source-fish opx)

License
-------

opx is distributed under the terms of the
`MIT License <https://choosealicense.com/licenses/mit>`_.
