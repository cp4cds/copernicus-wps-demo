from .wps_mydiag import MyDiag
from .wps_overview import Overview
from .wps_cloud_taylor import CloudTaylor
from .wps_portrait import Portrait
from .wps_timeseries_plot import TimeSeriesPlot
from .wps_timeseries_plot_generic import GenericTimeSeriesPlot
# from .wps_contour_plot import ContourPlot

processes = [
    MyDiag(),
    Overview(),
    CloudTaylor(),
    Portrait(),
    TimeSeriesPlot(),
    GenericTimeSeriesPlot(),
    # ContourPlot(),
]
