import sys
import os

from pywps import configuration

import logging
LOGGER = logging.getLogger("PYWPS")


def archive_root():
    return configuration.get_config_value("extra", "archive_root")


def obs_root():
    return configuration.get_config_value("extra", "obs_root")


def esmval_root():
    root = configuration.get_config_value("extra", "esmval_root")
    if not root:
        # guess conda env path
        root = os.path.join(os.path.dirname(sys.executable), '..', 'opt', 'esmvaltool')
    return root
