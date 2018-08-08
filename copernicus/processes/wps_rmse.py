import os

from pywps import Process
from pywps import LiteralInput, LiteralOutput
from pywps import ComplexInput, ComplexOutput
from pywps import Format, FORMATS
from pywps.app.Common import Metadata

from copernicus import runner
from copernicus import util

import logging
LOGGER = logging.getLogger("PYWPS")


class RMSE(Process):
    def __init__(self):
        inputs = [
            LiteralInput('region', 'Region',
                         abstract='Choose a region like Arctic.',
                         data_type='string',
                         allowed_values=['Arctic', ],
                         default='Arctic'),
            LiteralInput('model', 'Model',
                         abstract='Choose a model like NASA.',
                         data_type='string',
                         allowed_values=['NASA', ],
                         default='NASA'),
            LiteralInput('variable', 'Variable',
                         abstract='Choose a variable like sic.',
                         data_type='string',
                         allowed_values=['sic', ],
                         default='sic'),
            LiteralInput('ncenters', 'Number of Centers',
                         abstract='Choose a number of centers.',
                         data_type='integer',
                         default='4'),
            LiteralInput('cluster_method', 'Cluster Method',
                         abstract='Choose a cluster method.',
                         data_type='string',
                         allowed_values=['kmeans', ],
                         default='kmeans'),
            LiteralInput('eofs', 'EOFS',
                         abstract='Choose EOFS.',
                         data_type='boolean',
                         default='0'),
            LiteralInput('detrend', 'detrend',
                         abstract='Choose a detrend.',
                         data_type='integer',
                         default='2'),
            LiteralInput('experiment', 'Experiment',
                         abstract='Choose an experiment.',
                         data_type='string',
                         allowed_values=['historical', 'rcp26', 'rcp85'],
                         default='historical'),
        ]
        outputs = [
            ComplexOutput('output', 'Output plot',
                          abstract='Generated output plot of ESMValTool processing.',
                          as_reference=True,
                          supported_formats=[Format('image/png')]),
        ]

        super(RMSE, self).__init__(
            self._handler,
            identifier="rmse",
            title="Modes of variability",
            version=runner.VERSION,
            abstract="Tool to compute the RMSE between the observed and modelled patterns of variability "
            " obtained through classification and their relative relative bias (percentage) "
            " in the frequency of occurrence and the persistence of each mode.",
            metadata=[
                Metadata('ESMValTool', 'http://www.esmvaltool.org/'),
                Metadata('Documentation',
                         'https://copernicus-wps-demo.readthedocs.io/en/latest/processes.html#rmse',
                         role=util.WPS_ROLE_DOC),
                Metadata('Media',
                         util.diagdata_url() + '/modes_of_variability/era_interim_1990-01-2010-01_clusters.png',
                         role=util.WPS_ROLE_MEDIA),
                Metadata('Diagnostic Description',
                         util.diagdata_url() + '/modes_of_variability/description.md',
                         role=util.MAGIC_ROLE_DOC),
                Metadata('Diagnostic Metadata',
                         util.diagdata_url() + '/modes_of_variability/modes_of_variability.yml',
                         role=util.MAGIC_ROLE_METADATA),
            ],
            inputs=inputs,
            outputs=outputs,
            status_supported=True,
            store_supported=True)

    def _handler(self, request, response):
        response.update_status("starting ...", 0)
        # run diag
        response.update_status("running diag ...", 20)
        # result plot
        response.update_status("collect output plot ...", 90)
        response.outputs['output'].output_format = Format('image/png')
        response.outputs['output'].file = util.diagdata_file(
            os.path.join('modes_of_variability', 'era_interim_1990-01-2010-01_clusters.png'))
        response.update_status("done.", 100)
        return response
