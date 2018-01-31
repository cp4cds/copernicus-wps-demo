import os
import glob

from jinja2 import Environment, PackageLoader, select_autoescape

from copernicus import config

import logging
LOGGER = logging.getLogger("PYWPS")

template_env = Environment(
    loader=PackageLoader('copernicus', 'templates'),
    autoescape=select_autoescape(['yml', 'xml'])
)

VERSION = "2.0.0"


def run(namelist_file, config_file):
    """Run esmvaltool"""
    from esmvaltool.main import configure_logging, read_config_file, process_namelist
    namelist_name = os.path.splitext(os.path.basename(namelist_file))[0]
    cfg = read_config_file(config_file, namelist_name)

    # Create run dir
    if os.path.exists(cfg['run_dir']):
        print("ERROR: run_dir {} already exists, aborting to "
              "prevent data loss".format(cfg['output_dir']))
    os.makedirs(cfg['run_dir'])

    # configure logging
    configure_logging(
        output=cfg['run_dir'], console_log_level=cfg['log_level'])

    # log header
    # LOGGER.info(__doc__)
    LOGGER.debug("Using config file %s", config_file)

    # check NCL version
    # ncl_version_check()

    cfg['synda_download'] = False

    try:
        LOGGER.info("run esmvaltool ...")
        process_namelist(namelist_file=namelist_file, config_user=cfg)
        LOGGER.info("esmvaltool ... done.")
    except Exception as err:
        LOGGER.exception('esmvaltool failed!')
        raise Exception('esmvaltool failed: {0}'.format(err.output))
    # find the log
    logfile = os.path.join(cfg['run_dir'], 'main_log.txt')
    return logfile, cfg['plot_dir']


def generate_namelist(diag, constraints=None, start_year=2000, end_year=2005, output_format='pdf', workdir=None):
    constraints = constraints or {}
    workdir = workdir or os.curdir
    workdir = os.path.abspath(workdir)
    output_dir = os.path.join(workdir, 'output')
    # write config.yml
    config_templ = template_env.get_template('config.yml')
    rendered_config = config_templ.render(
        archive_root=config.archive_root(),
        obs_root=config.obs_root(),
        output_dir=output_dir,
        output_format=output_format,
    )
    config_file = os.path.abspath(os.path.join(workdir, "config.yml"))
    with open(config_file, 'w') as fp:
        fp.write(rendered_config)

    # write namelist.xml
    namelist = 'namelist_{0}.yml'.format(diag)
    namelist_templ = template_env.get_template(namelist)
    rendered_namelist = namelist_templ.render(
        diag=diag,
        workdir=workdir,
        constraints=constraints,
        start_year=start_year,
        end_year=end_year,
    )
    namelist_file = os.path.abspath(os.path.join(workdir, "namelist.yml"))
    with open(namelist_file, 'w') as fp:
        fp.write(rendered_namelist)
    return namelist_file, config_file


def get_output(output_dir, path_filter, name_filter=None, output_format='pdf'):
    name_filter = name_filter or '*'
    # output/namelist_20180130_111116/plots/ta_diagnostics/test_ta/ta.pdf
    output_filter = os.path.join(
        output_dir, path_filter, '{0}.{1}'.format(name_filter, output_format))
    LOGGER.debug("output_fitler %s", output_filter)
    matches = glob.glob(output_filter)
    if len(matches) == 0:
        raise Exception("no output found in workdir")
    elif len(matches) > 1:
        LOGGER.warn("more then one output found %s", matches)
    LOGGER.debug("output found=%s", matches[0])
    return matches[0]
