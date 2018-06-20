from .wps_wordcounter import WordCounter
from .wps_inout import InOut
from .wps_sleep import Sleep
from .wps_mydiag import MyDiag
from .wps_pydemo import PyDemo
from .wps_perfmetrics import Perfmetrics

processes = [
    WordCounter(),
    InOut(),
    Sleep(),
    MyDiag(),
    PyDemo(),
    Perfmetrics(),
]
