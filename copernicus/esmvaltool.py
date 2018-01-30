import os
import os.path
import shutil
from shutil import ignore_patterns
import glob
from subprocess import check_output, STDOUT, CalledProcessError
from copernicus._compat import urlparse
from netCDF4 import Dataset
from cdo import Cdo

from mako.lookup import TemplateLookup

from copernicus import config
# from copernicus._compat import escape

import logging
LOGGER = logging.getLogger("PYWPS")

mylookup = TemplateLookup(directories=[os.path.join(os.path.dirname(__file__), 'templates')],
                          output_encoding='utf-8', encoding_errors='replace')

VERSION = "2.0.0"


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


def run_diag(workdir=None):
    workdir = workdir or os.curdir
    # ncl path
    LOGGER.debug("NCARG_ROOT=%s", os.environ.get('NCARG_ROOT'))
    # build cmd
    # esmvaltool -c esmvaltool/config-user_demo.yml -n esmvaltool/namelists/namelist_MyVar_demo.yml
    cmd = ["esmvaltool",
           "-c", os.path.join(workdir, 'config.yml'),
           "-n", os.path.join(workdir, 'namelist.yml')]
    logfile = os.path.abspath(os.path.join(workdir, 'log.txt'))
    # run cmd
    try:
        output = check_output(cmd, stderr=STDOUT)
    except CalledProcessError as err:
        LOGGER.error('esmvaltool failed! %s', err.output)
        raise Exception('ESMValTool diag failed! Check the logs.')
        # raise Exception('esmvaltool failed: {0}'.format(escape(err.output)))
    else:
        # debug: show logfile
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(output)
        with open(logfile, 'w') as f:
            f.write(output)
    # check if data is found
    # if os.path.isfile(os.path.join(workdir, 'esgf_coupling_report.txt')):
    #    raise Exception("Could not find data in ESGF archive.")
    return logfile


def generate_namelist(diag, constraints=None, start_year=2000, end_year=2005, output_format='pdf', workdir=None):
    constraints = constraints or {}
    workdir = workdir or os.curdir
    workdir = os.path.abspath(workdir)
    output_dir = os.path.join(workdir, 'output')
    # write config.yml
    config_templ = mylookup.get_template('config.yml')
    rendered_config = config_templ.render_unicode(
        archive_root=config.archive_root(),
        obs_root=config.obs_root(),
        output_dir=output_dir,
        output_format=output_format,
    )
    config_filename = os.path.abspath(os.path.join(workdir, "config.yml"))
    with open(config_filename, 'w') as fp:
        fp.write(rendered_config)

    # write namelist.xml
    namelist = 'namelist_{0}.yml'.format(diag)
    namelist_templ = mylookup.get_template(namelist)
    rendered_namelist = namelist_templ.render_unicode(
        diag=diag,
        workdir=workdir,
        constraints=constraints,
        start_year=start_year,
        end_year=end_year,
    )
    outfile = os.path.abspath(os.path.join(workdir, "namelist.yml"))
    with open(outfile, 'w') as fp:
        fp.write(rendered_namelist)
    return outfile


def find_output(workdir=None, path_filter=None, name_filter=None, output_format="pdf"):
    workdir = workdir or os.curdir
    path_filter = path_filter or os.path.join('*', '*')
    name_filter = name_filter or "*"
    # output/namelist_20180130_111116/plots/ta_diagnostics/test_ta/ta.pdf
    matches = glob.glob(os.path.join(
        workdir, 'output', 'namelist_*', 'plots', path_filter, '{0}.{1}'.format(name_filter, output_format)))
    if len(matches) == 0:
        raise Exception("no output found in workdir")
    elif len(matches) > 1:
        LOGGER.warn("more then one output found %s", matches)
    LOGGER.debug("output found=%s", matches[0])
    return matches[0]
