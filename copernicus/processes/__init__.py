from .wps_say_hello import SayHello
from .wps_mydiag import MyDiag
from .wps_overview import Overview

processes = [
    SayHello(),
    MyDiag(),
    Overview(),
]
