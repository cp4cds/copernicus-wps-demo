import os
from netCDF4 import Dataset
from cdo import Cdo
from copernicus._compat import urlparse


def create_esgf_datastore(datasets, workdir=None):
    """
    Prepares an ESGF datastore from datasets (files or opendap) for ESMValTool ESGF coupling module.
    """
    workdir = workdir or os.curdir
    datastore_root = os.path.join(workdir, 'esgf_datastore')
    constraints = dict(
        model=[],
        experiment=[],
        time_frequency='mon',
        cmor_table='Amon',
        variable='tas',
        ensemble=['r1i1p1'],
    )
    try:
        LOGGER.info("Creating datastore with %s datasets ...", len(datasets))
        cdo = Cdo()
        os.makedirs(datastore_root)
        for ds_path in datasets:
            dest = os.path.join(datastore_root, os.path.basename(ds_path))
            parsed_url = urlparse(ds_path)
            if not parsed_url.scheme:
                LOGGER.info("Linking dataset %s", ds_path)
                os.symlink(ds_path, dest)
            elif parsed_url.scheme in ['http', 'https']:
                # copy opendap dataset
                LOGGER.info("Downloading OpenDAP dataset %s ...", ds_path)
                cdo.copy(input=ds_path, output=dest)
            else:
                LOGGER.warn("Skipping dataset %s", ds_path)
                continue
            ds = Dataset(ds_path)
            if ds.model_id not in constraints['model']:
                constraints['model'].append(ds.model_id)
            if ds.experiment_id not in constraints['experiment']:
                constraints['experiment'].append(ds.experiment_id)
            # if ds.parent_experiment_rip not in constraints['ensemble']:
            #    constraints['ensemble'].append(ds.parent_experiment_rip)
    except OSError:
        msg = "Could not create esgf datastore."
        LOGGER.exception(msg)
        raise Exception(msg)
    return constraints
