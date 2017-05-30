from .wps_say_hello import SayHello
from .wps_mydiag import MyDiag
from .wps_overview import Overview
from .wps_timeseries_plot import TimeSeriesPlot

processes = [
    SayHello(),
    MyDiag(),
    Overview(),
    TimeSeriesPlot(),
]
