import pytest
from copernicus import util


@pytest.mark.skip(reason='not working yet')
def test_static_url():
    assert util.static_url() == 'http://localhost:5000/static'


@pytest.mark.skip(reason='not working yet')
def test_diagdata_url():
    assert util.diagdata_url() == 'http://localhost:5000/static/diagnosticsdata'
