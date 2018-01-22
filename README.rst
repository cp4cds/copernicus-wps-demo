copernicus-wps-demo
===================

.. image:: https://travis-ci.org/cp4cds/copernicus-wps-demo.svg?branch=master
   :target: https://travis-ci.org/cp4cds/copernicus-wps-demo
   :alt: Travis Build

Demo with WPS processes for copernicus.

Overview
********

In `Copernicus`_ we want to provide processing capabilities next to a climate data store.
The processing capabilities are exposed using the Web Processing Service standard interface with
the `PyWPS`_ implementation. This demo contains several example processes implemented with
`ESMValTool`_ and `NCL`_. The processes are defined with different WPS profiles
mainly to show ways how the input data of the tools can be described and restricted.

Installation
************

The installation is done with `Buildout`_. It is using the Python distribution
system `Anaconda`_ to maintain software dependencies.

If Anaconda is not available then a minimal Anaconda will be installed during
the installation process in your home directory ``~/anaconda``.

The installation process setups a conda environment named ``copernicus``. All
additional packages are going into this conda environment.
The location is ``~/.conda/envs/copernicus``.

Now, check out the code from the GitHub repo and start the installation::

   $ git clone https://github.com/cp4cds/copernicus-wps-demo.git
   $ cd copernicus-wps-demo
   $ make clean install

After successful installation you need to start the services. All installed files (config etc ...) are by default in your home directory ``~/birdhouse``. Now, start the services::

   $ make start  # starts supervisor services
   $ make status # shows supervisor status

The deployed WPS service is available on http://localhost:8096/wps?service=WPS&version=1.0.0&request=GetCapabilities.

Check the log files for errors::

   $ cd ~/birdhouse
   $ tail -f  var/log/pywps/copernicus.log
   $ tail -f  var/log/supervisor/copernicus.log

For other install options run ``make help`` and read the documention of the
`Makefile <http://birdhousebuilderbootstrap.readthedocs.org/en/latest/>`_.


Configuration
*************

If you want to run on a different hostname or port then change the default values in ``custom.cfg``::

   $ cd wps
   $ vim custom.cfg
   $ cat custom.cfg
   [settings]
   hostname = localhost
   http-port = 8096
   archive-root = /path/to/esgf/cmip5/archive


The path to ESGF archive is configured in ``custom.cfg`` with the ``archive-root`` option.
The configuration file ``esgf_config.xml`` for the ESGF coupling module will be generated.

After any change to your ``custom.cfg`` you **need** to run ``make update`` (offline mode) or ``make install`` again
and restart the ``supervisor`` service::

  $ make install
  $ make restart
  $ make status

Examples with Birdy
*******************

Birdy is a WPS command line client.

Install birdy::

  $ conda install -c birdhouse -c conda-forge birdhouse-birdy


Set WPS service:

  $ export WPS_SERVICE=http://localhost:8096/wps

See what processes are available::

  $ birdy -h

Run *mydiag*::

  $ birdy mydiag -h
  $ birdy mydiag --model MPI-ESM-LR --experiment historical --ensemble r1i1p1 --start_year 2000 --end_year 2001

Run *overview*::

  $ birdy overview -h
  $ birdy overview --model MPI-ESM-LR --experiment historical --ensemble r1i1p1 --start_year 2000 --end_year 2001

Run *cloud_taylor*::

  $ birdy cloud_taylor -h
  $ birdy cloud_taylor --model MPI-ESM-LR --experiment historical --ensemble r1i1p1 --start_year 2000 --end_year 2001

Run *ts_plot*::

  $ birdy ts_plot -h
  $ birdy ts_plot --model MPI-ESM-LR --experiment historical --ensemble r1i1p1 --start_year 2000 --end_year 2001 --variable tas



Using Docker
************

Get docker images using docker-compose::

    $ docker-compose pull


Start the demo with docker-compose::

    $ docker-compose up -d  # runs with -d in the background
    $ docker-compose logs -f  # check the logs if running in background

By default the WPS service should be available on port 8080::

    $ firefox "http://localhost:8080/wps?service=wps&request=GetCapabilities"

Alternatively you can change the port by using environment variables, for example::

    $ HTTP_PORT=8096 docker-compose up -d # wps service will be available on port 8096

Run docker exec to watch logs::

    $ docker ps     # find container name
    copernicuswpsdemo_wps_1
    $ docker exec copernicuswpsdemo_wps_1 tail -f /opt/birdhouse/var/log/supervisor/copernicus.log
    $ docker exec copernicuswpsdemo_wps_1 tail -f /opt/birdhouse/var/log/pywps/copernicus.log

Use docker-compose to stop the containers::

    $ docker-compose down

Testdata
********

For the demo processes you can fetch CMIP5 test-data from the ESGF archive.
You need a valid ESGF credentials which you can fetch for example with `esgf-pyclient`_.

For the examples you need CMIP5 data with the following facets:

* project=CMIP5
* experiment=historical
* ensemble=r1i1p1
* variable=ta, tas, or pr
* model=MPI-ESM-LR
* time_frequency=mon


You can use wget to download ESGF NetCDF files (``-x`` option to create directories)::

    $ wget --certificate cert.pem --private-key cert.pem --ca-certificate cert.pem -N -x -P /path/to/esgf/cmip5/archive


.. _Copernicus: http://climate.copernicus.eu/
.. _PyWPS: http://pywps.org/
.. _ESMValTool: http://www.esmvaltool.org/
.. _NCL: http://www.ncl.ucar.edu/
.. _esgf-pyclient: http://esgf-pyclient.readthedocs.io/en/latest/index.html
.. _Buildout: http://www.buildout.org/
.. _Anaconda: http://www.continuum.io/
