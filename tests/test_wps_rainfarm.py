import pytest

from pywps import Service
from pywps.tests import assert_response_success

from . common import client_for
from copernicus.processes.wps_rainfarm import RainFarm


def test_wps_rainfarm():
    client = client_for(Service(processes=[RainFarm()]))
    datainputs = "regridding=false;slope=false"
    resp = client.get(
        service='WPS', request='Execute', version='1.0.0', identifier='rainfarm',
        datainputs=datainputs)
    print(resp.data)
    assert_response_success(resp)
