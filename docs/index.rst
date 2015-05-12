.. pypbs documentation master file, created by
   sphinx-quickstart on Fri Mar 27 15:46:28 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pypbs's documentation!
=================================

pypbs aims to be a super simple api that sits on top of the common pbs commands.
Some pbs commands output xml such as qstat and pbsnodes. This output is in turn
parsed and used to build the api.

You may also want to check out the 
`pbs_python <https://oss.trac.surfsara.nl/pbs_python>`_ project
pbs_python requires that you compile the project where pypbs is just a wrapper
on top of the pbs commands.

Contents:

.. toctree::
    :maxdepth: 3

    commands
    apiexamples
    api/modules

Installation
------------

#. Download the code

    .. code-block:: bash

        git clone https://github.com/VDBWRAIR/pypbs.git

#. CD to pypbs directory

    .. code-block:: bash

        cd pypbs

#. (Optional) Highly recommended to install into a virtualenv

    #. Create virtualenv

        .. code-block:: bash

            virtualenv myenv

    #. Activate virtualenv

        .. code-block:: bash

            . myenv/bin/activate

#. Install project

    .. code-block:: bash

        python setup.py install
    

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

