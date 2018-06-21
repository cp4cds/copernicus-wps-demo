import os


# wps roles
WPS_ROLE_BASE_URL = 'http://www.opengis.net/spec/wps/2.0/def/process/description'
WPS_ROLE_DOC = WPS_ROLE_BASE_URL + '/documentation'
WPS_ROLE_MEDIA = WPS_ROLE_BASE_URL + '/media'
# magic roles
MAGIC_ROLE_BASE_URL = 'http://c3s-magic.eu/spec/diagnostic/2.0'
MAGIC_ROLE_DOC = MAGIC_ROLE_BASE_URL + '/documentation'
MAGIC_ROLE_METADATA = MAGIC_ROLE_BASE_URL + '/metadata'


def diagdata_file(filepath):
    return os.path.join(diagdata_directory(), filepath)


def diagdata_directory():
    return os.path.join(static_directory(), 'diagnosticsdata')


def static_directory():
    """Helper function to return path to the static directory"""
    return os.path.join(os.path.dirname(__file__), 'static')


def static_url():
    # return 'http://localhost:5000/static'
    return 'https://raw.githubusercontent.com/cp4cds/copernicus-wps-demo/master/copernicus/static'


def diagdata_url():
    return static_url() + '/diagnosticsdata'
