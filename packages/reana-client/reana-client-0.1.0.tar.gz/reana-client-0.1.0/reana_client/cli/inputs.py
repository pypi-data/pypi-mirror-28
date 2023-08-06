# -*- coding: utf-8 -*-
#
# This file is part of REANA.
# Copyright (C) 2017, 2018 CERN.
#
# REANA is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# REANA is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# REANA; if not, write to the Free Software Foundation, Inc., 59 Temple Place,
# Suite 330, Boston, MA 02111-1307, USA.
#
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization or
# submit itself to any jurisdiction.
"""REANA client inputs related commands."""

import logging
import os

import click
import tablib

from ..config import default_inputs_path, default_organization, default_user


@click.group(
    help='All interaction related to input files and parameters of workflows.')
@click.pass_context
def inputs(ctx):
    """Top level wrapper for input file and parameter related interaction."""
    logging.debug('inputs')


@click.command(
    'list',
    help='List input files of a workflow.')
@click.option(
    '-u',
    '--user',
    default=default_user,
    help='User who created the workflow.')
@click.option(
    '-o',
    '--organization',
    default=default_organization,
    help='Organization whose resources will be used.')
@click.option(
    '--workflow',
    default=os.environ.get('REANA_WORKON', None),
    help='Name of the workflow whose input files you want to list.')
@click.option(
    '--filter',
    multiple=True,
    help='Filter output according to column titles (case-sensitive).')
@click.option(
    '-of',
    '--output-format',
    type=click.Choice(['json', 'yaml']),
    help='Set output format.')
@click.pass_context
def inputs_list(ctx, user, organization, workflow, filter, output_format):
    """List input files of a workflow."""
    logging.debug('inputs.list')
    logging.debug('user: {}'.format(user))
    logging.debug('organization: {}'.format(organization))
    logging.debug('workflow: {}'.format(workflow))
    logging.debug('filter: {}'.format(filter))
    logging.debug('output_format: {}'.format(output_format))

    try:
        response = ctx.obj.client.get_analysis_inputs(user, organization,
                                                      workflow)

        data = tablib.Dataset()
        data.headers = ['Name', 'Size', 'Last-Modified']
        for file_ in response:
            data.append([file_['name'],
                         file_['size'],
                         file_['last-modified']])

        if filter:
            data = data.subset(rows=None, cols=list(filter))

        if output_format:
            click.echo(data.export(output_format))
        else:
            click.echo(data)
    except Exception as e:
        logging.debug(str(e))
        click.echo(
            click.style('Something went wrong while retrieving input file list'
                        ' for workflow {0}:\n{1}'.format(workflow, str(e)),
                        fg='red'),
            err=True)


@click.command(
    'upload',
    help='Upload one of more FILE to the analysis workspace.')
@click.argument('filenames', metavar='FILE', nargs=-1)
@click.option(
    '-u',
    '--user',
    default=default_user,
    help='User who created the workflow.')
@click.option(
    '-o',
    '--organization',
    default=default_organization,
    help='Organization whose resources will be used.')
@click.option(
    '--workflow',
    default=os.environ.get('REANA_WORKON', None),
    help='Name of the workflow you are uploading files for. '
         'Overrides value of $REANA_WORKON.')
@click.option(
    '--inputs-directory',
    default=default_inputs_path,
    help='Path to the inputs files directory.')
@click.pass_context
def inputs_upload(ctx, user, organization, workflow, filenames,
                  inputs_directory):
    """Upload file(s) to analysis workspace. Associate with a workflow."""
    logging.debug('inputs.upload')
    logging.debug('filenames: {}'.format(filenames))
    logging.debug('user: {}'.format(user))
    logging.debug('organization: {}'.format(organization))
    logging.debug('workflow: {}'.format(workflow))
    logging.debug('inputs_directory: {}'.format(inputs_directory))

    if workflow:
        logging.info('Workflow "{}" selected'.format(workflow))
        for filename in filenames:
            try:
                with open(os.path.join(inputs_directory, filename)) as f:
                    click.echo('Uploading {} ...'.format(f.name))
                    response = ctx.obj.client.seed_analysis_inputs(
                        user, organization, workflow, f, filename)
                    if response:
                        click.echo('File {} was successfully uploaded.'.
                                   format(f.name))

            except Exception as e:
                logging.debug(str(e))
                click.echo(
                    click.style(
                        'Something went wrong while uploading {0}'.
                        format(f.name),
                        fg='red'),
                    err=True)

    else:
        click.echo(
            click.style('Workflow name must be provided either with '
                        '`--workflow` option or with `$REANA_WORKON` '
                        'environment variable',
                        fg='red'),
            err=True)


inputs.add_command(inputs_list)
inputs.add_command(inputs_upload)
