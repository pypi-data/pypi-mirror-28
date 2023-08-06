#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os
import re
import sys

import click

import bones


@click.command()
@click.option('--check-url/--no-check-url', is_flag=True, help='Check URL for availability')
@click.option('-i', '--interactive', is_flag=True, help='Run interactively')
@click.option('-f', '--force', is_flag=True, help='Remove existing project if found')
@click.option('-q', '--quiet', help="Reduce spam")
@click.option('-d', '--debug', help="Increase spam")
@click.option('-p', '--python', help="Version of python to use")
@click.option('-v', '--venv', is_flag=True, help="Create a virtual environment")
@click.option('--version', is_flag=True, help='Show version and exit')
@click.argument('project_name', required=False)
def bone(python, version, quiet, debug, **kwds):
    if quiet:
        logging.basicConfig(level=logging.WARNING, format='%(message)s')
    elif debug:
        logging.basicConfig(level=logging.DEBUG, format='%(message)s')
    else:
        logging.basicConfig(level=logging.INFO, format='%(message)s')
    try:
        python_version_pattern = r'(?P<major>[0-9])(.(?P<minor>[0-9]+))?(.(?P<revision>[0-9]+))?'
        python = python or sys.version.split(' ')[0]
        match = re.match(python_version_pattern, python)
        if not match:
            raise bones.errors.PythonVersionMismatch(version=python)

        if version:
            print('bones {version}'.format(version=bones.__version__))
            sys.exit(0)

        kwds.setdefault('package_path', os.getcwd())
        bones.create(**kwds)

    except bones.errors.BaseError as e:
        msg = click.style(e.__msg__, fg='red', bold=True)
        click.echo(msg)


if __name__ == '__main__':
    bone()
