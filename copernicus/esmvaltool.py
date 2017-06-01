import os
import os.path
import glob
from subprocess import check_output, STDOUT, CalledProcessError

from copernicus import config

import logging
LOGGER = logging.getLogger("PYWPS")

from mako.lookup import TemplateLookup
mylookup = TemplateLookup(directories=[os.path.join(os.path.dirname(__file__), 'templates')],
                          output_encoding='utf-8', encoding_errors='replace')

VERSION = "1.1.0"


def prepare(workdir="."):
    return config.esmval_root()


def run_diag(namelist, workdir='.'):
    # ncl path
    LOGGER.debug("NCARG_ROOT=%s", os.environ.get('NCARG_ROOT'))

    home_path = prepare(workdir=workdir)

    # build cmd
    main_py = os.path.join(home_path, "main.py")
    logfile = os.path.abspath(os.path.join(workdir, 'log.txt'))
    cmd = ["python", main_py, namelist]

    # run cmd
    try:
        output = check_output(cmd, stderr=STDOUT, cwd=home_path)
    except CalledProcessError as err:
        LOGGER.error('esmvaltool failed! %s', err.output)
        raise Exception('esmvaltool failed: {0}'.format(err.output))
    else:
        # debug: show logfile
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(output)
        with open(logfile, 'w') as f:
            f.write(output)

    # check if data is found
    if os.path.isfile(os.path.join(workdir, 'esgf_coupling_report.txt')):
        raise Exception("Could not find data in ESGF archive.")

    return logfile


def generate_namelist(diag, constraints=None, start_year=2000, end_year=2005, output_format='pdf', workdir='.'):
    constraints = constraints or {}
    workdir = os.path.abspath(workdir)

    home_path = prepare(workdir=workdir)

    # write esgf_config.xml
    esgf_config_templ = mylookup.get_template('esgf_config.xml')
    rendered_esgf_config = esgf_config_templ.render_unicode(
        workdir=workdir,
        archive_root=config.archive_root(),
    )
    esgf_config_filename = os.path.abspath(os.path.join(workdir, "esgf_config.xml"))
    with open(esgf_config_filename, 'w') as fp:
        fp.write(rendered_esgf_config)

    # write namelist.xml
    namelist = 'namelist_{0}.xml'.format(diag)
    namelist_templ = mylookup.get_template(namelist)
    rendered_namelist = namelist_templ.render_unicode(
        diag=diag,
        prefix=home_path,
        workdir=workdir,
        constraints=constraints,
        start_year=start_year,
        end_year=end_year,
        output_format=output_format
    )
    outfile = os.path.abspath(os.path.join(workdir, "namelist.xml"))
    with open(outfile, 'w') as fp:
        fp.write(rendered_namelist)
    return outfile


def find_output(workdir='.', path_filter=None, output_format="pdf"):
    path_filter = path_filter or os.path.join('plot*', '*')
    # work/temp_XzZnMo/plot/tsline/tsline_tas_nomask_noanom_nodetr_-90_90_historical_2000-2005.pdf
    matches = glob.glob(os.path.join(workdir, 'work', '*', path_filter, '*.{0}'.format(output_format)))
    if len(matches) == 0:
        raise Exception("no output found in workdir")
    elif len(matches) > 1:
        LOGGER.warn("more then one output found %s", matches)
    LOGGER.debug("output found=%s", matches[0])
    return matches[0]
