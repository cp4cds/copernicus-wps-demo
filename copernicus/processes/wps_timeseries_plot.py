import os

from pywps import Process
from pywps import LiteralInput, LiteralOutput
from pywps import ComplexInput, ComplexOutput
from pywps import Format, FORMATS
from pywps.app.Common import Metadata

from copernicus import runner

import logging
LOGGER = logging.getLogger("PYWPS")


class TimeSeriesPlot(Process):
    def __init__(self):
        inputs = [
            LiteralInput('model', 'Model',
                         abstract='Choose a model like MPI-ESM-LR.',
                         data_type='string',
                         allowed_values=['MPI-ESM-LR', 'MPI-ESM-MR'],
                         default='MPI-ESM-LR'),
            LiteralInput('experiment', 'Experiment',
                         abstract='Choose an experiment like historical.',
                         data_type='string',
                         allowed_values=['historical', 'rcp26', 'rcp45', 'rcp85'],
                         default='historical'),
            LiteralInput('ensemble', 'Ensemble',
                         abstract='Choose an ensemble like r1i1p1.',
                         data_type='string',
                         allowed_values=['r1i1p1', 'r2i1p1', 'r3i1p1'],
                         default='r1i1p1'),
            LiteralInput('start_year', 'Start year', data_type='integer',
                         abstract='Start year of model data.',
                         default="1990"),
            LiteralInput('end_year', 'End year', data_type='integer',
                         abstract='End year of model data.',
                         default="2000"),
        ]
        outputs = [
            ComplexOutput('namelist', 'namelist',
                          abstract='ESMValTool namelist used for processing.',
                          as_reference=True,
                          supported_formats=[Format('text/plain')]),
            ComplexOutput('log', 'Log File',
                          abstract='Log File of ESMValTool processing.',
                          as_reference=True,
                          supported_formats=[Format('text/plain')]),
            ComplexOutput('output', 'Output plot',
                          abstract='Generated output plot of ESMValTool processing.',
                          as_reference=True,
                          supported_formats=[Format('application/pdf')]),
            ComplexOutput('output_ds', 'Reformatted dataset',
                          abstract='Reformatted dataset of the input files.',
                          as_reference=True,
                          supported_formats=[Format('application/x-netcdf')]),
        ]

        super(TimeSeriesPlot, self).__init__(
            self._handler,
            identifier="ts_plot",
            title="Timeseries Plot",
            version="1.1.0",
            abstract="Generates a timeseries plot using ESMValTool."
                     " The default run uses the following CMIP5 data: "
                     "project=CMIP5, experiment=historical, ensemble=r1i1p1, variable=tas, model=MPI-ESM-LR, time_frequency=mon",  # noqa
            metadata=[
                Metadata('ESMValTool', 'http://www.esmvaltool.org/'),
                Metadata('ESGF Testdata', 'https://esgf1.dkrz.de/thredds/catalog/esgcet/7/cmip5.output1.MPI-M.MPI-ESM-LR.historical.mon.atmos.Amon.r1i1p1.v20120315.html?dataset=cmip5.output1.MPI-M.MPI-ESM-LR.historical.mon.atmos.Amon.r1i1p1.v20120315.pr_Amon_MPI-ESM-LR_historical_r1i1p1_185001-200512.nc'),  # noqa
            ],
            inputs=inputs,
            outputs=outputs,
            status_supported=True,
            store_supported=True)

    def _handler(self, request, response):
        # build esgf search constraints
        constraints = dict(
            model=request.inputs['model'][0].data,
            experiment=request.inputs['experiment'][0].data,
            time_frequency='mon',
            cmor_table='Amon',
            ensemble=request.inputs['ensemble'][0].data,
        )

        # generate namelist
        result = runner.diag(
            'reformat',
            constraints=constraints,
            start_year=request.inputs['start_year'][0].data,
            end_year=request.inputs['end_year'][0].data,
            output_format='pdf')

        # namelist output
        response.outputs['namelist'].output_format = FORMATS.TEXT
        response.outputs['namelist'].file = result['namelist']

        # log output
        response.outputs['log'].output_format = FORMATS.TEXT
        response.outputs['log'].file = result['logfile']

        # result plot
        # work/temp_XzZnMo/plot/tsline/tsline_tas_nomask_noanom_nodetr_-90_90_historical_2000-2005.pdf
        response.outputs['output'].output_format = Format('application/pdf')
        response.outputs['output'].file = runner.find_output(
            path_filter=os.path.join('plot', 'tsline'),
            output_format="pdf")

        # reformatted input dataset
        # work/temp_fqNUZN//tsline/tsline_tas_nomask_noanom_nodetr_historical__-90_90_1980-2000.nc
        response.outputs['output_ds'].output_format = Format('application/x-netcdf')
        response.outputs['output_ds'].file = runner.find_output(
            path_filter=os.path.join('tsline'),
            output_format="nc")

        return response
