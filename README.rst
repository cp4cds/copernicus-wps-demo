Copernicus WPS Demo
===================

.. image:: https://travis-ci.org/cp4cds/copernicus-wps-demo.svg?branch=master
   :target: https://travis-ci.org/cp4cds/copernicus-wps-demo
   :alt: Travis Build

.. image:: https://img.shields.io/github/license/cp4cds/copernicus-wps-demo.svg
   :target: https://github.com/cp4cds/copernicus-wps-demo/raw/master/LICENSE.txt
   :alt: GitHub license

Demo with WPS processes for Copernicus.

Overview
********

In `Copernicus`_ we want to provide processing capabilities for a climate data store.
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

Running WPS service in test environment
---------------------------------------

For development purposes you can run the WPS service without Nginx and supervisor.
Use the following instructions:

.. code-block:: sh

    # get the source code
    $ git clone https://github.com/cp4cds/copernicus-wps-demo.git
    $ cd copernicus-wps-demo

    # create conda environment
    $ conda env create -f environment.yml

    # activate conda environment
    $ source activate copernicus-wps-demo

    # install copernicus code into conda environment
    $ python setup.py develop

    # start the WPS service
    $ copernicus

    # open your browser on the default service url
    $ firefox http://localhost:5000/wps

    # ... and service capabilities url
    $ firefox http://localhost:5000/wps?service=WPS&request=GetCapabilities

The ``copernicus`` service command-line has more options:

.. code-block:: sh

    $ copernicus -h

For example you can start the WPS with enabled debug logging mode:

.. code-block:: sh

    $ copernicus --debug

Or you can overwrite the default `PyWPS`_ configuration by providing your own
PyWPS configuration file (just modifiy the options you want to change):

.. code-block:: sh

    # edit your local pywps configuration file
    $ cat mydev.cfg
    [logging]
    level = WARN
    file = /tmp/mydev.log

    # start the service with this configuration
    $ copernicus -c mydev.cfg


WPS Client Examples
*******************

The examples for the WPS clients are using a demo WPS serivce on the bovec test machine at DKRZ.

https://bovec.dkrz.de/ows/proxy/copernicus?Service=WPS&Request=GetCapabilities&Version=1.0.0

There is currently not much data attached (especially for oberstation data).
Please use the default data selection parameters, otherwise no result might be returned.


CURL with HTTP Get requests
---------------------------

GetCapabilities
+++++++++++++++

Run ``GetCapabilities`` request to see which processes are available::

  $ curl -s -o caps.xml \
    "https://bovec.dkrz.de/ows/proxy/copernicus?Service=WPS&Request=GetCapabilities&Version=1.0.0"


DescribeProcess
+++++++++++++++

Run ``DescribeProcess`` request to see input/output parameters of the ``mydiag`` process::

  $ curl -s -o describe.xml \
    "https://bovec.dkrz.de/ows/proxy/copernicus?Service=WPS&Request=DescribeProcess&Version=1.0.0&identifier=mydiag"

Execute (sync mode)
+++++++++++++++++++

Run ``Exceute`` in synchronous mode for ``mydiag`` with default input parameters:

.. code-block:: bash

  $ curl -s -o execute.xml \
    "https://bovec.dkrz.de/ows/proxy/copernicus?Service=WPS&Request=Execute&Version=1.0.0&identifier=mydiag&DataInputs=model=MPI-ESM-LR;experiment=historical;ensemble=r1i1p1;start_year=2000;end_year=2001"

.. warning::
  The execution request my have a time-out. Please use the *asynchronous* mode for real testing.

A status document is returned. Open the URL with the reference to the output plot:

.. code-block:: xml

  <wps:Output>
    <ows:Identifier>output</ows:Identifier>
    <wps:Reference xlink:href="https://bovec.dkrz.de/download/wpsoutputs/copernicus/75ad4c42-207b-11e8-9a75-109836a7cf3a/ta_u_y2we.pdf" mimeType="application/pdf"/>
  </wps:Output>

Execute (async mode)
++++++++++++++++++++

Run ``Exceute`` in asynchronous mode for ``mydiag``:

.. code-block:: bash

    $ curl -s -o execute.xml \
      "https://bovec.dkrz.de/ows/proxy/copernicus?Service=WPS&Request=Execute&Version=1.0.0&identifier=mydiag&DataInputs=model=MPI-ESM-LR;experiment=historical;ensemble=r1i1p1;start_year=2000;end_year=2001&storeExecuteResponse=true&status=true"

A status document is returned.

.. code-block:: xml

    <wps:ExecuteResponse
      statusLocation="https://bovec.dkrz.de/download/wpsoutputs/copernicus/621d8f28-207d-11e8-99d0-109836a7cf3a.xml">
      <wps:Process wps:processVersion="2.0.0">
        <ows:Identifier>mydiag</ows:Identifier>
        <ows:Title>Simple plot</ows:Title>
        <ows:Abstract>Generates a plot for temperature using ESMValTool. It is a diagnostic used in the ESMValTool tutoriaal doc/toy-diagnostic-tutorial.pdf. The default run uses the following CMIP5 data: project=CMIP5, experiment=historical, ensemble=r1i1p1, variable=ta, model=MPI-ESM-LR, time_frequency=mon</ows:Abstract>
      </wps:Process>
      <wps:Status creationTime="2018-03-05T14:59:12Z">
        <wps:ProcessAccepted>PyWPS Process mydiag accepted</wps:ProcessAccepted>
      </wps:Status>
    </wps:ExecuteResponse>

Check the status document given by the ``statusLoction`` URL until the job has finished:

.. code-block:: bash

  $ curl -s -o status.xml \
    "https://bovec.dkrz.de/download/wpsoutputs/copernicus/621d8f28-207d-11e8-99d0-109836a7cf3a.xml"

The final status document should similar to this one:

.. code-block:: xml

    <wps:ExecuteResponse
      statusLocation="https://bovec.dkrz.de/download/wpsoutputs/copernicus/621d8f28-207d-11e8-99d0-109836a7cf3a.xml">
    <wps:Process wps:processVersion="2.0.0">
     <ows:Identifier>mydiag</ows:Identifier>
    </wps:Process>
    <wps:Status creationTime="2018-03-05T14:59:27Z">
     <wps:ProcessSucceeded>PyWPS Process Simple plot finished</wps:ProcessSucceeded>
    </wps:Status>
    <wps:ProcessOutputs>
     <wps:Output>
       <ows:Identifier>output</ows:Identifier>
       <wps:Reference xlink:href="https://bovec.dkrz.de/download/wpsoutputs/copernicus/621d8f28-207d-11e8-99d0-109836a7cf3a/ta_ZqKo5r.pdf" mimeType="application/pdf"/>
     </wps:Output>
    </wps:ProcessOutputs>
    </wps:ExecuteResponse>

Open the URL pointing to the plot output.


OWSLib Python module
--------------------

.. todo::
  Add IPython notebook.

http://birdhouse-workshop.readthedocs.io/en/latest/advanced/owslib.html

Birdy Command line client
-------------------------

Birdy is a WPS command line client.

Install birdy (Linux, macOS)::

  $ conda install -c birdhouse -c conda-forge birdhouse-birdy

Set WPS service::

  $ export WPS_SERVICE=https://bovec.dkrz.de/ows/proxy/copernicus # demo service on bovec
  # OR
  $ export WPS_SERVICE=http://localhost:8096/wps  # your local WPS service

See what processes are available::

  $ birdy -h

Run *mydiag*::

  $ birdy mydiag -h
  $ birdy mydiag --model MPI-ESM-LR --experiment historical --ensemble r1i1p1 --start_year 2000 --end_year 2001

Check the process status. The processes should finish after 10 seconds with a response simliar to this one::

  [ProcessSucceeded 100/100] PyWPS Process Simple plot finished
  Output:
  namelist=https://bovec.dkrz.de/download/wpsoutputs/copernicus/eceb7ef8-2078-11e8-acba-109836a7cf3a/namelist_sr0bYf.yml (text/plain)
  log=https://bovec.dkrz.de/download/wpsoutputs/copernicus/eceb7ef8-2078-11e8-acba-109836a7cf3a/main_log_fXjRR1.txt (text/plain)
  output=https://bovec.dkrz.de/download/wpsoutputs/copernicus/eceb7ef8-2078-11e8-acba-109836a7cf3a/ta_XWGYZt.pdf (application/pdf)

Open the ouptut URL in Browser to see the plot.


Phoenix Web Client
------------------

You can run the demo processes directly without log-in on Phoenix.

* GetCapabilites: https://bovec.dkrz.de/processes/list?wps=copernicus
* DescribeProcess: https://bovec.dkrz.de/processes/execute?wps=copernicus&process=mydiag
* Execute: press ``Submit`` button.

Job status is monitored. When job has finished you can either show the output directly or show the output details:
https://bovec.dkrz.de/monitor/details/79eb1c39-e6a3-4944-b90d-00cc71addcaf/outputs


WPS Client Examples with x509 Certificate
*****************************************

A WPS service can be secured with x509 certificates by using the `Twitcher`_ OWS security proxy.
A WPS ``Execute`` request can only be run when the WPS client provides a valid x509 proxy certificate.

In the following examples we will use a Copernicus WPS demo service which is protected by a Twitcher security proxy.
It will only accept x509 proxy certificates from `ESGF`_ to execute a process. The ``GetCapabilites`` and ``DescribeProcess``
requests are public.

CURL with HTTP Get requests
---------------------------

The following examples are using ``curl``. You may also like to use the Firefox `RestClient`_ plugin.

GetCapabilities
+++++++++++++++

Run ``GetCapabilities`` request to see which processes are available::

  $ curl -s -o caps.xml \
    "https://bovec.dkrz.de:5000/ows/proxy/copernicus?Service=WPS&Request=GetCapabilities&Version=1.0.0"


DescribeProcess
+++++++++++++++

Run ``DescribeProcess`` request to see input/output parameters of the ``mydiag`` process::

  $ curl -s -o describe.xml \
    "https://bovec.dkrz.de:5000/ows/proxy/copernicus?Service=WPS&Request=DescribeProcess&Version=1.0.0&identifier=mydiag"

Execute (sync mode)
+++++++++++++++++++

Run ``Exceute`` in synchronous mode for ``mydiag`` with default input parameters:

.. code-block:: bash

  $ curl -s -o execute.xml \
    "https://bovec.dkrz.de:5000/ows/proxy/copernicus?Service=WPS&Request=Execute&Version=1.0.0&identifier=mydiag&DataInputs=model=MPI-ESM-LR;experiment=historical;ensemble=r1i1p1;start_year=2000;end_year=2001"

You should get an exception report asking you to provide a x509 certificate:

.. code-block:: xml

   <ExceptionReport>
     <Exception exceptionCode="NoApplicableCode" locator="AccessForbidden">
       <ExceptionText>A valid X.509 client certificate is needed.</ExceptionText>
     </Exception>
   </ExceptionReport>

Get a valid x509 certifcate from `ESGF`_, for example using the `esgf-pyclient`_.
See the `logon example`_.
Let's say your proxy certificate is in the file ``cert.pem``.
Run the curl example above with this certificate:

.. code-block:: bash

  $ curl -s -o execute.xml --cert cert.pem --key cert.pem \
    "https://bovec.dkrz.de:5000/ows/proxy/copernicus?Service=WPS&Request=Execute&Version=1.0.0&identifier=mydiag&DataInputs=model=MPI-ESM-LR;experiment=historical;ensemble=r1i1p1;start_year=2000;end_year=2001"

If your certificate is valid then your process will be executed (sync mode) and you will get a XML result document
providing you with URL references to a generated plot:

.. code-block:: xml

  <wps:Output>
    <ows:Identifier>output</ows:Identifier>
    <wps:Reference xlink:href="http://bovec.dkrz.de:8000/wpsoutputs/copernicus/3c0eb52e-2608-11e8-b551-dea873cae3fc/ta_P9MhKW.pdf" mimeType="application/pdf"/>
  </wps:Output>

Try more examples as shown in the examples above using a x509 certificate.

Using Python requests library
-----------------------------

In this example we show how you can use the Python `requests`_ library to run WPS requests as with ``curl``.

.. code-block:: python

    import requests

    # GetCapabilites
    url = "https://bovec.dkrz.de:5000/ows/proxy/emu?request=GetCapabilities&service=WPS"
    requests.get(url, verify=True).text
    # DescribeProcess
    url = "https://bovec.dkrz.de:5000/ows/proxy/emu?request=DescribeProcess&service=WPS&version=1.0.0&identifier=hello"
    requests.get(url, verify=True).text
    # Execute with client certifcate cert.pem
    url = "https://bovec.dkrz.de:5000/ows/proxy/emu?request=Execute&service=WPS&version=1.0.0&identifier=hello&DataInputs=name=Copernicus"
    requests.get(url, cert="cert.pem" verify=True).text

See the `requests documentation`_ for details.


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
.. _ESGF: https://esgf.llnl.gov/
.. _PyWPS: http://pywps.org/
.. _ESMValTool: http://www.esmvaltool.org/
.. _NCL: http://www.ncl.ucar.edu/
.. _esgf-pyclient: http://esgf-pyclient.readthedocs.io/en/latest/index.html
.. _Buildout: http://www.buildout.org/
.. _Anaconda: http://www.continuum.io/
.. _Twitcher: http://twitcher.readthedocs.io/en/latest/
.. _RestClient: http://birdhouse-workshop.readthedocs.io/en/latest/pywps/testing.html?highlight=rest#restclient-firefox-only
.. _logon example: http://esgf-pyclient.readthedocs.io/en/latest/examples.html
.. _requests: http://docs.python-requests.org/en/master/
.. _requests documentation: http://docs.python-requests.org/en/master/user/advanced/?highlight=ssl#client-side-certificates
