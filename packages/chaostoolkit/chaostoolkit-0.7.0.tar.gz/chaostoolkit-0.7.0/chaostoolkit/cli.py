# -*- coding: utf-8 -*-
import io
import json
import logging
import os
import sys


from chaoslib.exceptions import ChaosException
from chaoslib.discovery import discover as disco
from chaoslib.experiment import ensure_experiment_is_valid, load_experiment,\
    run_experiment
from chaoslib.types import Discovery, Experiment
import click
from click_plugins import with_plugins
import logzero
from logzero import logger
from pkg_resources import iter_entry_points

from chaostoolkit import __version__
from chaostoolkit.check import check_newer_version


__all__ = ["cli"]


@click.group()
@click.version_option(version=__version__)
@click.option('--verbose', is_flag=True, help='Display debug level traces.')
@click.option('--no-version-check', is_flag=True,
              help='Do not search for an updated version of the chaostoolkit.')
@click.option('--change-dir',
              help='Change directory before running experiment.')
@click.option('--no-log-file', is_flag=True,
              help='Disable logging to file entirely.')
@click.option('--log-file', default="experiment.log", show_default=True,
              help='File path where to write the experiment log.')
def cli(verbose: bool = False, no_version_check: bool = False,
        change_dir: str = None, no_log_file: bool = False,
        log_file: str = "experiment.log"):

    if verbose:
        logzero.loglevel(logging.DEBUG, update_custom_handlers=False)
        fmt = "%(color)s[%(asctime)s %(levelname)s] "\
              "[%(module)s:%(lineno)d]%(end_color)s %(message)s"
    else:
        logzero.loglevel(logging.INFO, update_custom_handlers=False)
        fmt = "%(color)s[%(asctime)s %(levelname)s]%(end_color)s %(message)s"

    if not no_log_file:
        # let's ensure we log at DEBUG level
        logger.setLevel(logging.DEBUG)
        logzero.logfile(
            click.format_filename(log_file), mode='w',
            loglevel=logging.DEBUG)

    logzero.formatter(
        formatter=logzero.LogFormatter(fmt=fmt, datefmt="%Y-%m-%d %H:%M:%S"),
        update_custom_handlers=False)

    if not no_version_check:
        check_newer_version()

    if change_dir:
        logger.warning("Moving to {d}".format(d=change_dir))
        os.chdir(change_dir)


@cli.command()
@click.option('--report-path', default="./chaos-report.json",
              help='Path where to save the report from the plan execution.')
@click.option('--dry', is_flag=True,
              help='Run the experiment without executing activities.')
@click.option('--no-validation', is_flag=True,
              help='Do not validate the experiment before running.')
@click.argument('path', type=click.Path(exists=True))
def run(path: str, report_path: str = "./chaos-report.json", dry: bool = False,
        no_validation: bool = False):
    """Run the experiment given at PATH."""
    experiment = load_experiment(click.format_filename(path))
    if not no_validation:
        try:
            ensure_experiment_is_valid(experiment)
        except ChaosException as x:
            logger.error(str(x))
            logger.debug(x)
            sys.exit(1)

    experiment["dry"] = dry
    journal = run_experiment(experiment)

    with io.open(report_path, "w") as r:
        json.dump(journal, r, indent=2, ensure_ascii=False)


@cli.command()
@click.argument('path', type=click.Path(exists=True))
def validate(path: str):
    """Validate the experiment at PATH."""
    experiment = load_experiment(click.format_filename(path))
    try:
        ensure_experiment_is_valid(experiment)
        logger.info("experiment syntax and semantic look valid")
    except ChaosException as x:
        logger.error(str(x))
        sys.exit(1)


@cli.command()
@click.option('--no-system-info', is_flag=True,
              help='Do not discover system information.')
@click.option('--no-install', is_flag=True,
              help='Assume package already in PYTHONPATH.')
@click.option('--discovery-report-path', default="./discovery.json",
              help='Path where to save the report from the discovery.',
              show_default=True)
@click.argument('package')
def discover(package: str, discovery_report_path: str = "./discovery.json",
             no_system_info: bool = False,
             no_install: bool = False) -> Discovery:
    """Discover capabilities and experiments."""
    discovery = disco(
        package_name=package, discover_system=not no_system_info,
        download_and_install=not no_install)
    with open(discovery_report_path, "w") as d:
        d.write(json.dumps(discovery, indent=2))
    logger.info("Discovery report saved in {p}".format(
        p=discovery_report_path))


# keep this after the cli group declaration for plugins to override defaults
with_plugins(iter_entry_points('chaostoolkit.cli_plugins'))(cli)
