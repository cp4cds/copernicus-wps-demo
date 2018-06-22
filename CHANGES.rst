Changes
*******

0.3.0 (2018-06-22)
==================

* Generated from cookiecutter template (#13).
* Skipped buildout just relying on conda and werkzeug.
* Use sphinx documentation (#12).
* Added "fake" processes rainfarm and rmse from MAGIC demo (#16, #22).
* Using static diagnostics description from MAGIC demo (#20).

0.2.2 (2018-06-18)
==================

* Added WPS client examples (#7).
* Added WPS client examples with x509 certificate (#10).

0.2.1 (2018-02-08)
==================

* fixed ncl installation (#3).
* added demo service using werkzeug.

0.2.0 (2018-02-06)
==================

* using ESMValTool 2.x
* diag list: mydiag and py_demo

0.1.1 (2018-01-29)
==================

* cleaned up Dockerfile.
* added pscopg2 for postgres.
* updated pywps recipe 0.9.3.
* added workaround for broken ncl conda package.
* updated Readme with birdy examples.

0.1.0 (2017-06-06)
==================

* added tutorial diagnostics from esmvaltool (MyDiag, Overview, timeseriesplot).
* timeseriesplot both added with a generic wps profile (opendap, netcdf) and with esgf search facets.
* added NCL coutour plot with opendap and netcdf input.
