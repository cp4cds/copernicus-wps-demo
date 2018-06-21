import os


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
