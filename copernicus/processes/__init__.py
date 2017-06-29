from .wps_mydiag import MyDiag
from .wps_overview import Overview
from .wps_timeseries_plot import TimeSeriesPlot
from .wps_timeseries_plot_generic import GenericTimeSeriesPlot
# from .wps_contour_plot import ContourPlot

processes = [
    MyDiag(),
    Overview(),
    TimeSeriesPlot(),
    GenericTimeSeriesPlot(),
    # ContourPlot(),
]
