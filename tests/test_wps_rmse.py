import pytest

from pywps import Service
from pywps.tests import assert_response_success

from . common import client_for
from copernicus.processes.wps_rmse import RMSE


def test_wps_rmse():
    client = client_for(Service(processes=[RMSE()]))
    datainputs = "eofs=false;experiment=historical"
    resp = client.get(
        service='WPS', request='Execute', version='1.0.0', identifier='rmse',
        datainputs=datainputs)
    print(resp.data)
    assert_response_success(resp)
