from .wps_mydiag import MyDiag
from .wps_overview import Overview
from .wps_timeseries_plot import TimeSeriesPlot

processes = [
    MyDiag(),
    Overview(),
    TimeSeriesPlot(),
]
