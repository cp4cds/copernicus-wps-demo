from pywps import configuration

import logging
LOGGER = logging.getLogger("PYWPS")


def archive_root():
    return configuration.get_config_value("extra", "archive_root")


def esmval_root():
    return configuration.get_config_value("extra", "esmval_root")
