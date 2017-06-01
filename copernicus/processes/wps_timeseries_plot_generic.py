import os

from pywps import Process
from pywps import LiteralInput, LiteralOutput
from pywps import ComplexInput, ComplexOutput
from pywps import Format, FORMATS
from pywps.app.Common import Metadata

from copernicus import esmvaltool

import logging
LOGGER = logging.getLogger("PYWPS")


class GenericTimeSeriesPlot(Process):
    def __init__(self):
        inputs = [
            ComplexInput('dataset', 'Dataset',
                         abstract='You may provide a URL or upload a NetCDF file.',
                         min_occurs=0,
                         max_occurs=100,
                         supported_formats=[Format('application/x-netcdf')]),
            LiteralInput('dataset_opendap', 'Remote OpenDAP Data URL',
                         data_type='string',
                         abstract="Or provide a remote OpenDAP data URL,"
                                  " for example:"
                                  " http://www.esrl.noaa.gov/psd/thredds/dodsC/Datasets/ncep.reanalysis2.dailyavgs/surface/mslp.2016.nc",  # noqa
                         metadata=[
                            Metadata(
                                'application/x-ogc-dods',
                                'https://www.iana.org/assignments/media-types/media-types.xhtml')],
                         min_occurs=0,
                         max_occurs=100),
            LiteralInput('start_year', 'Start year', data_type='integer',
                         abstract='Start year of model data.',
                         metadata=[
                             Metadata('start',
                                      role='https://www.earthsystemcog.org/spec/esgf_search/2.1.0/def/coverage/year/start',  # noqa
                                      href='http://esgf-data.dkrz.de/esg-search/search?project=CMIP5&time_frequency=mon&variable=tas&distrib=false&replica=false&latest=true&limit=0&start=1990-01-01T00:00:00Z'),  # noqa
                         ],
                         default="1990"),
            LiteralInput('end_year', 'End year', data_type='integer',
                         abstract='End year of model data.',
                         metadata=[
                             Metadata('end',
                                      role='https://www.earthsystemcog.org/spec/esgf_search/2.1.0/def/coverage/year/end',  # noqa
                                      href='http://esgf-data.dkrz.de/esg-search/search?project=CMIP5&time_frequency=mon&variable=tas&distrib=false&replica=false&latest=true&limit=0&end=2000-12-31T00:00:00Z'),  # noqa
                         ],
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

        super(GenericTimeSeriesPlot, self).__init__(
            self._handler,
            identifier="ts_plot_generic",
            title="Generic Timeseries Plot",
            version=esmvaltool.VERSION,
            abstract="Generates a timeseries plot using ESMValTool."
                     " Input data is provided as NetCDF or OpenDAP datasets."
                     " It works only on the following CMIP5 data:"
                     " project=CMIP5, variable=tas, time_frequency=mon",  # noqa
            metadata=[
                Metadata('ESMValTool',
                         role='http://www.opengis.net/spec/wps/2.0/def/process/description/documentation',
                         href='http://www.esmvaltool.org/'),
                Metadata('ESGF Testdata',
                         'https://esgf1.dkrz.de/thredds/catalog/esgcet/7/cmip5.output1.MPI-M.MPI-ESM-LR.historical.mon.atmos.Amon.r1i1p1.v20120315.html?dataset=cmip5.output1.MPI-M.MPI-ESM-LR.historical.mon.atmos.Amon.r1i1p1.v20120315.tas_Amon_MPI-ESM-LR_historical_r1i1p1_185001-200512.nc'),  # noqa
                Metadata('Freva Example with MURCSS',
                         'https://freva.met.fu-berlin.de/plugins/murcss/setup/'),
                Metadata('Example WPS Process Description',
                         'http://docs.opengeospatial.org/is/14-065/14-065.html#103'),
                Metadata('The ESGF Search RESTful API',
                         role='http://www.opengis.net/spec/wps/2.0/def/process/description/documentation',
                         href='https://www.earthsystemcog.org/projects/cog/esgf_search_restful_api'),
                Metadata('Allowed CMIP5 Datasets',
                         role='https://www.earthsystemcog.org/spec/esgf_search/2.1.0/def/query',  # noqa
                         href='http://esgf-data.dkrz.de/esg-search/search?project=CMIP5&time_frequency=mon&variable=tas&distrib=false&replica=false&latest=true&limit=0&facets=model,experiment,ensemble'),  # noqa
            ],
            inputs=inputs,
            outputs=outputs,
            status_supported=True,
            store_supported=True)

    def _handler(self, request, response):
        response.update_status("starting ...", 0)
        # collect all datasets
        response.update_status("prepare input data ...", 5)
        datasets = []
        if 'dataset' in request.inputs:
            for dataset in request.inputs['dataset']:
                datasets.append(dataset.file)
        # append opendap urls
        if 'dataset_opendap' in request.inputs:
            for dataset in request.inputs['dataset_opendap']:
                datasets.append(dataset.data)
        # build datastore and esgf search constraints
        constraints = esmvaltool.create_esgf_datastore(datasets)
        # generate namelist
        response.update_status("generate namelist ...", 10)
        namelist = esmvaltool.generate_namelist(
            diag='ts_plot_generic',
            constraints=constraints,
            start_year=request.inputs['start_year'][0].data,
            end_year=request.inputs['end_year'][0].data,
            output_format='pdf',
        )

        # run diag
        response.update_status("running diag ...", 20)
        logfile = esmvaltool.run_diag(namelist)

        # namelist output
        response.outputs['namelist'].output_format = FORMATS.TEXT
        response.outputs['namelist'].file = namelist

        # log output
        response.outputs['log'].output_format = FORMATS.TEXT
        response.outputs['log'].file = logfile

        # result plot
        # work/temp_XzZnMo/plot/tsline/tsline_tas_nomask_noanom_nodetr_-90_90_historical_2000-2005.pdf
        response.update_status("collect output plot ...", 90)
        response.outputs['output'].output_format = Format('application/pdf')
        response.outputs['output'].file = esmvaltool.find_output(
            path_filter=os.path.join('plot', 'tsline'),
            output_format="pdf")

        # reformatted input dataset
        # work/temp_fqNUZN//tsline/tsline_tas_nomask_noanom_nodetr_historical__-90_90_1980-2000.nc
        response.outputs['output_ds'].output_format = Format('application/x-netcdf')
        response.outputs['output_ds'].file = esmvaltool.find_output(
            path_filter=os.path.join('tsline'),
            output_format="nc")
        # done
        response.update_status("done.", 100)
        return response
