import os

from pywps import Process
from pywps import LiteralInput, LiteralOutput
from pywps import ComplexInput, ComplexOutput
from pywps import Format, FORMATS
from pywps.app.Common import Metadata

import Ngl
import Nio

import logging
LOGGER = logging.getLogger("PYWPS")


class SimplePlot(Process):
    def __init__(self):
        inputs = [
            ComplexInput('dataset', 'Dataset',
                         abstract='You may provide a URL or upload a NetCDF file.',
                         min_occurs=0,
                         max_occurs=1,
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
                         max_occurs=1),
            LiteralInput('variable', 'Variable', data_type='string',
                         abstract='Variable name.',
                         min_occurs=0,
                         max_occurs=1,
                         default="tas"),
        ]
        outputs = [
            ComplexOutput('output', 'Output plot',
                          abstract='Generated output plot of ESMValTool processing.',
                          as_reference=True,
                          supported_formats=[Format('application/pdf')]),
        ]

        super(SimplePlot, self).__init__(
            self._handler,
            identifier="simple_plot",
            title="Simple Plot",
            version="0.1",
            abstract="Generates a simple contour plot using NCL."
                     " Input data is provided as NetCDF or OpenDAP datasets.",
            metadata=[
                Metadata('Python NCL',
                         role='http://www.opengis.net/spec/wps/2.0/def/process/description/documentation',
                         href='http://www.pyngl.ucar.edu/'),
            ],
            inputs=inputs,
            outputs=outputs,
            status_supported=True,
            store_supported=True)

    def _handler(self, request, response):
        response.update_status("starting ...", 0)
        # collect all datasets
        datasets = []
        if 'dataset' in request.inputs:
            for dataset in request.inputs['dataset']:
                datasets.append(dataset.file)
        # append opendap urls
        if 'dataset_opendap' in request.inputs:
            for dataset in request.inputs['dataset_opendap']:
                datasets.append(dataset.data)
        # generate plot ...
        response.update_status("generate plot ...", 10)
        ds = Nio.open_file(datasets[0])
        if 'variable' in request.inputs:
            variable = request.inputs['variable'][0].data
        else:
            variable = 'tas'
        data = ds.variables[variable]
        lon = ds.variables["lon"][:]
        lat = ds.variables["lat"][:]
        wks = Ngl.open_wks("pdf", "plot")
        resources = Ngl.Resources()
        resources.cnFillOn = True
        resources.cnLineLabelsOn = False    # Turn off line labels.
        resources.cnInfoLabelOn = False
        resources.nglSpreadColorEnd = -2    # Don't include gray in contours.
        # bbox extend
        resources.sfXCStartV = lon.min()
        resources.sfXCEndV = lon.max()
        resources.sfYCStartV = lat.min()
        resources.sfYCEndV = lat.max()
        # caption
        caption = os.path.basename(datasets[0])
        resources.pmTickMarkDisplayMode = "Never"  # Turn off map tickmarks.
        resources.tiMainString = caption    # Set a title.
        plot = Ngl.contour_map(wks, data[0, :, :], resources)
        # clean up
        del resources
        del plot
        # result plot
        response.outputs['output'].output_format = Format('application/pdf')
        response.outputs['output'].file = "plot.pdf"
        Ngl.end()
        # done
        response.update_status("done.", 100)
        return response
