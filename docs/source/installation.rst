.. _installation:

Installation
============

Install from Anaconda
---------------------

.. todo::

   Prepare Conda package.

Install from GitHub
-------------------

Check out code from the copernicus-wps-demo GitHub repo and start the installation:

.. code-block:: sh

   $ git clone https://github.com/cp4cds/copernicus-wps-demo.git
   $ cd copernicus-wps-demo
   $ conda env create -f environment.yml
   $ source activate copernicus
   $ python setup.py develop

... or do it the lazy way
+++++++++++++++++++++++++

The previous installation instructions assume you have Anaconda installed.
We provide also a ``Makefile`` to run this installation without additional steps:

.. code-block:: sh

   $ git clone https://github.com/cp4cds/copernicus-wps-demo.git
   $ cd copernicus-wps-demo
   $ make clean    # cleans up a previous Conda environment
   $ make install  # installs Conda if necessary and runs the above installation steps

Start copernicus-wps-demo PyWPS service
---------------------------------------

After successful installation you can start the service using the ``copernicus`` command-line.

.. code-block:: sh

   $ copernicus --help # show help
   $ copernicus start  # start service with default configuration

   OR

   $ copernicus start --daemon # start service as daemon
   loading configuration
   forked process id: 42

The deployed WPS service is by default available on:

http://localhost:5000/wps?service=WPS&version=1.0.0&request=GetCapabilities.

.. NOTE:: Remember the process ID (PID) so you can stop the service with ``kill PID``.

You can find which process uses a given port using the following command (here for port 5000):

.. code-block:: sh

   $ netstat -nlp | grep :5000

Check the log files for errors:

.. code-block:: sh

   $ tail -f  pywps.log

... or do it the lazy way
+++++++++++++++++++++++++

You can also use the ``Makefile`` to start and stop the service:

.. code-block:: sh

  $ make start
  $ make status
  $ tail -f pywps.log
  $ make stop


Run copernicus-wps-demo as Docker container
-------------------------------------------

You can also run copernicus-wps-demo as a Docker container, see the :ref:`Tutorial <tutorial>`.

Use Ansible to deploy copernicus-wps-demo on your System
--------------------------------------------------------

Use the `Ansible playbook`_ for PyWPS to deploy copernicus-wps-demo on your system.
Follow the `example`_ for copernicus-wps-demo given in the playbook.

Building the docs
-----------------

First install dependencies for the documentation::

  $ make bootstrap_dev
  $ make docs


.. _Ansible playbook: http://ansible-wps-playbook.readthedocs.io/en/latest/index.html
.. _example: http://ansible-wps-playbook.readthedocs.io/en/latest/tutorial.html
