.. _tutorial:


Tutorial
========


WPS Client Examples
*******************

The examples for the WPS clients are using a demo WPS serivce on the bovec test machine at DKRZ.

https://bovec.dkrz.de/ows/proxy/copernicus?Service=WPS&Request=GetCapabilities&Version=1.0.0

There is currently not much data attached (especially for observation data).
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

Run ``DescribeProcess`` request to see input/output parameters of the ``rainfarm`` process::

  $ curl -s -o describe.xml \
    "https://bovec.dkrz.de/ows/proxy/copernicus?Service=WPS&Request=DescribeProcess&Version=1.0.0&identifier=rainfarm"

Execute (sync mode)
+++++++++++++++++++

Run ``Exceute`` in synchronous mode for ``rainfarm`` with default input parameters:

.. code-block:: bash

  $ curl -s -o execute.xml \
    "https://bovec.dkrz.de/ows/proxy/copernicus?Service=WPS&Request=Execute&Version=1.0.0&identifier=rainfarm&DataInputs=regridding=0;slope=0"

.. warning::
  The execution request my have a time-out. Please use the *asynchronous* mode for real testing.

A status document is returned. Open the URL with the reference to the output plot:

.. code-block:: xml

  <wps:Output>
    <ows:Identifier>output</ows:Identifier>
    <wps:Reference xlink:href="https://bovec.dkrz.de/download/wpsoutputs/copernicus/40472cbe-8046-11e8-ad8f-109836a7cf3a/RainFARM_example_64x64_in8du35f.png" mimeType="image/png"/>
  </wps:Output>

Execute (async mode)
++++++++++++++++++++

Run ``Exceute`` in asynchronous mode for ``rainfarm``:

.. code-block:: bash

    $ curl -s -o execute.xml \
      "https://bovec.dkrz.de/ows/proxy/copernicus?Service=WPS&Request=Execute&Version=1.0.0&identifier=rainfarm&DataInputs=regridding=0;slope=0&storeExecuteResponse=true&status=true"

A status document is returned.

.. code-block:: xml

  <wps:ExecuteResponse
    statusLocation="https://bovec.dkrz.de/download/wpsoutputs/copernicus/8faddd84-8046-11e8-814d-109836a7cf3a.xml">
    <wps:Process wps:processVersion="2.0.0">
      <ows:Identifier>rainfarm</ows:Identifier>
      <ows:Title>RainFARM stochastic downscaling</ows:Title>
    </wps:Process>
    <wps:Status creationTime="2018-07-05T13:28:38Z">
      <wps:ProcessAccepted>PyWPS Process rainfarm accepted</wps:ProcessAccepted>
    </wps:Status>
  </wps:ExecuteResponse>

Check the status document given by the ``statusLoction`` URL until the job has finished:

.. code-block:: bash

  $ curl -s -o status.xml \
    "https://bovec.dkrz.de/download/wpsoutputs/copernicus/8faddd84-8046-11e8-814d-109836a7cf3a.xml"

The final status document should similar to this one:

.. code-block:: xml

  <wps:ExecuteResponse
    statusLocation="https://bovec.dkrz.de/download/wpsoutputs/copernicus/8faddd84-8046-11e8-814d-109836a7cf3a.xml">
    <wps:Process wps:processVersion="2.0.0">
      <ows:Identifier>rainfarm</ows:Identifier>
      <ows:Title>RainFARM stochastic downscaling</ows:Title>
    </wps:Process>
    <wps:Status creationTime="2018-07-05T13:28:38Z">
      <wps:ProcessSucceeded>PyWPS Process RainFARM stochastic downscaling finished</wps:ProcessSucceeded>
    </wps:Status>
    <wps:ProcessOutputs>
      <wps:Output>
        <ows:Identifier>output</ows:Identifier>
        <ows:Title>Output plot</ows:Title>
        <wps:Reference xlink:href="https://bovec.dkrz.de/download/wpsoutputs/copernicus/8faddd84-8046-11e8-814d-109836a7cf3a/RainFARM_example_64x64_s8lwoktx.png" mimeType="image/png"/>
      </wps:Output>
    </wps:ProcessOutputs>
  </wps:ExecuteResponse>

Open the URL pointing to the plot output.


OWSLib Python module
--------------------

`OWSLib`_ is a Python library to interact with OWS/OGC services like WPS, WMS, etc.
It is using the Python `requests`_ library.

.. todo::
  Add IPython notebook.

http://birdhouse-workshop.readthedocs.io/en/latest/advanced/owslib.html

Birdy Command line client
-------------------------

`Birdy`_ is a WPS command line client.

Install birdy (Linux, macOS)::

  $ conda install -c birdhouse -c conda-forge birdhouse-birdy

Set WPS service::

  $ export WPS_SERVICE=https://bovec.dkrz.de/ows/proxy/copernicus # demo service on bovec
  # OR
  $ export WPS_SERVICE=http://localhost:5000/wps  # your local WPS service

See which processes are available::

  $ birdy -h

Run *rainfarm*::

  $ birdy rainfarm -h
  $ birdy rainfarm --regridding 0 --slope 0

Check the process status. The processes should finish after 10 seconds with a response simliar to this one::

  ProcessSucceeded  [####################################]  100%
  Output:
  output=https://bovec.dkrz.de/download/wpsoutputs/copernicus/ecac32a0-8047-11e8-ad8f-109836a7cf3a/RainFARM_example_64x64_pe72ysqs.png

Open the ouptut URL in Browser to see the plot.

Phoenix Web Client
------------------

You can run the demo processes directly without log-in on Phoenix.

* GetCapabilites: https://bovec.dkrz.de/processes/list?wps=copernicus
* DescribeProcess: https://bovec.dkrz.de/processes/execute?wps=copernicus&process=rainfarm
* Execute: press ``Submit`` button.

Job status is monitored. When job has finished you can either show the output directly or show the output details:
https://bovec.dkrz.de/monitor/details/3cd6b18e-81ce-431d-990a-6fca36cae052/outputs


WPS Client Examples with x509 Certificate
*****************************************

A WPS service can be secured with x509 certificates by using the `Twitcher`_ OWS security proxy.
A WPS ``Execute`` request can only be run when the WPS client provides a valid x509 proxy certificate.

In the following examples we will use a CP4CDS WPS demo service which is protected by a Twitcher security proxy.
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

Run ``DescribeProcess`` request to see input/output parameters of the ``rainfarm`` process::

  $ curl -s -o describe.xml \
    "https://bovec.dkrz.de:5000/ows/proxy/copernicus?Service=WPS&Request=DescribeProcess&Version=1.0.0&identifier=rainfarm"

Execute (sync mode)
+++++++++++++++++++

Run ``Exceute`` in synchronous mode for ``rainfarm`` with default input parameters:

.. code-block:: bash

  $ curl -s -o execute.xml \
    "https://bovec.dkrz.de:5000/ows/proxy/copernicus?Service=WPS&Request=Execute&Version=1.0.0&identifier=rainfarm&DataInputs=regridding=0;slope=0"

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
    "https://bovec.dkrz.de:5000/ows/proxy/copernicus?Service=WPS&Request=Execute&Version=1.0.0&identifier=rainfarm&DataInputs=regridding=0;slope=0"

If your certificate is valid then your process will be executed (sync mode) and you will get an XML result document
providing you with URL references to a generated plot:

.. code-block:: xml

  <wps:Output>
    <ows:Identifier>output</ows:Identifier>
    <wps:Reference xlink:href="http://bovec.dkrz.de:8000/wpsoutputs/copernicus/aaaa6eb2-8056-11e8-9f87-dea873cae3fc/RainFARM_example_64x64_rx7m0ycd.png" mimeType="image/png"/>
  </wps:Output>

Try more examples as shown in the examples above using a x509 certificate.

Using Python requests library
-----------------------------

In this example we show how you can use the Python `requests`_ library to run WPS requests.

.. code-block:: python

    import requests

    # GetCapabilites
    url = "https://bovec.dkrz.de:5000/ows/proxy/copernicus?request=GetCapabilities&service=WPS"
    requests.get(url, verify=True).text
    # DescribeProcess
    url = "https://bovec.dkrz.de:5000/ows/proxy/copernicus?request=DescribeProcess&service=WPS&version=1.0.0&identifier=sleep"
    requests.get(url, verify=True).text
    # Execute with client certifcate cert.pem
    url = "https://bovec.dkrz.de:5000/ows/proxy/copernicus?request=Execute&service=WPS&version=1.0.0&identifier=sleep&DataInputs=delay=1"
    requests.get(url, cert="cert.pem" verify=True).text

See the `requests documentation`_ for details.

Using OWSLib Python library
---------------------------

An example with `OWSLib`_.

Make sure you have the latest version from the conda birdhouse channel:

.. code-block:: sh

    $ conda install -c birdhouse -c conda-forge owslib

Run the *hello* process with a client certificate:


.. code-block:: python

  from owslib.wps import WebProcessingService
  wps = WebProcessingService(url="https://bovec.dkrz.de:5000/ows/proxy/copernicus",
                             verify=True, cert="cert.pem")

  exc = wps.execute(identifier='sleep', inputs=[('delay', '1')])
  exc.checkStatus()
  exc.getStatus()
  exc.isSucceded()
  exc.processOutputs[0].data

Using Birdy
-----------

An example with `Birdy`_

Install latest birdy (Linux, macOS) from conda birdhouse channel:

.. code-block:: sh

    $ conda install -c birdhouse -c conda-forge birdhouse-birdy owslib

.. code-block:: sh

    $ export WPS_SERVICE=https://bovec.dkrz.de:5000/ows/proxy/copernicus
    $ birdy -h
    $ birdy sleep -h
    $ birdy --cert cert.pem sleep --delay 1

Using Docker
************

Get docker images using docker-compose::

    $ docker-compose pull

Start the demo with docker-compose::

    $ docker-compose up -d  # runs with -d in the background
    $ docker-compose logs -f  # check the logs if running in background

By default the WPS service should be available on port 5000::

    $ firefox "http://localhost:5000/wps?service=wps&request=GetCapabilities"

Run docker exec to watch logs::

    $ docker ps     # find container name
    copernicus-wps-demo_copernicus_1
    $ docker exec copernicus-wps-demo_copernicus_1 tail -f /opt/wps/pywps.log

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
.. _NCL: http://www.ncl.ucar.edu/
.. _esgf-pyclient: http://esgf-pyclient.readthedocs.io/en/latest/index.html
.. _Twitcher: http://twitcher.readthedocs.io/en/latest/
.. _RestClient: http://birdhouse-workshop.readthedocs.io/en/latest/pywps/testing.html?highlight=rest#restclient-firefox-only
.. _logon example: http://esgf-pyclient.readthedocs.io/en/latest/examples.html
.. _requests: http://docs.python-requests.org/en/master/
.. _requests documentation: http://docs.python-requests.org/en/master/user/advanced/?highlight=ssl#client-side-certificates
.. _OWSLib: http://geopython.github.io/OWSLib/
.. _Birdy: http://birdy.readthedocs.io/en/latest/
