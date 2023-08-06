#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 Malcolm Ramsay <malramsay64@gmail.com>
#
# Distributed under terms of the MIT license.

"""Run an experiment varying a number of variables."""

import logging
import os
import shutil
import subprocess
import sys
from collections import ChainMap
from itertools import product
from pathlib import Path
from typing import Any, Callable, Dict, Iterator, List, Union

import click
from ruamel.yaml import YAML

from .pbs import create_pbs_file

yaml = YAML()
PathLike = Union[str, Path]

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def combine_dictionaries(dicts: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Merge a list of dictionaries into a single dictionary.

    Where there are collisions the first value in the list will be set
    as this function is using ChainMap to combine the dicts.
    """
    return dict(ChainMap(*dicts))


def variable_matrix(variables: Dict[str, Any],
                    parent: str=None,
                    iterator='product') -> Iterator[Dict[str, Any]]:
    """Process the variables into a list of the appropriate combinations.

    This function performs recursive processing of the input variables, creating an iterator which
    has all the combinations of varaibles specified in the input.

    """
    _iters: Dict[str, Callable] = {'product': product, 'zip': zip}

    if isinstance(variables, dict):
        key_vars = []
        # Check for iterator variable and remove if nessecary
        # changing the value of the iterator for remaining levels.
        if variables.get('iterator'):
            iterator = variables.get('iterator')
            del variables['iterator']
        for key, value in variables.items():
            # The case where we have a dictionary representing a
            # variable's value, the value is stored in 'value'.
            if key == 'value':
                key = parent
            key_vars.append(list(variable_matrix(value, key, iterator)))
        # Iterate through all possible products generating a dictionary
        for i in _iters[iterator](*key_vars):
            yield combine_dictionaries(i)

    elif isinstance(variables, list):
        for item in variables:
            yield from variable_matrix(item, parent, iterator)

    # Stopping condition -> we have either a single value from a list
    # or a value had only one item
    else:
        yield {parent: variables}


# TODO update type inference for this when issues in mypy are closed
def uniqueify(my_list: Any) -> List[Any]:
    return list(dict.fromkeys(my_list))


def process_command(commands: Union[str, List[str]],
                    matrix: List[Dict[str, Any]]) -> Iterator[List[str]]:
    # Ensure commands is a list
    if isinstance(commands, str):
        commands = [commands]

    for command in commands:
        # substitute variables into command
        c_list = [command.format(**kwargs) for kwargs in matrix]
        yield uniqueify(c_list)


def read_file(filename: PathLike='experiment.yml') -> Dict['str', Any]:
    with open(filename, 'r') as stream:
        structure = yaml.load(stream)
    return structure


def process_file(filename: PathLike='experiment.yml') -> None:
    # Ensure filename is a Path
    filename = Path(filename)

    # Read input file
    logger.debug('Reading file %s', filename)
    structure = read_file(filename)

    # create variable matrix
    variables = list(variable_matrix(structure.get('variables')))
    assert variables

    command_groups = process_command(structure.get('command'), variables)

    # Check for pbs options
    if structure.get('pbs'):
        if structure.get('name'):
            # set the name attribute in pbs to global name if no name defined in pbs
            structure['pbs'].setdefault('name', structure.get('name'))
        run_pbs_commands(command_groups, structure.get('pbs'), filename.parent)
        return

    run_bash_commands(command_groups, filename.parent)
    return


def run_bash_commands(command_groups: Iterator[List[str]],
                      directory: PathLike=Path.cwd()) -> None:
    logger.debug('Running commands in bash shell')
    # iterate through command groups
    for command_group in command_groups:
        # Check command works
        if shutil.which(command_group[0].split()[0]) is None:
            raise ProcessLookupError('Command `{}` was not found, check your PATH.')

        for command in command_group:
            try:
                subprocess.run(command.split(), check=True, cwd=directory)
            except ProcessLookupError:
                print('Command failed: check PATH is correctly set\n', command)


def run_pbs_commands(command_groups: Iterator[List[str]],
                     pbs_options: Dict[str, Any],
                     directory: PathLike=Path.cwd(),
                     basename: str='experi') -> None:
    """Submit a series of commands to a batch scheduler.

    This takes a list of strings which are the contents of the pbs files, writes the files to disk
    and submits the job to the scheduler. Files which match the pattern of the resulting files
    <basename>_<index>.pbs are deleted before writing the new files.

    To ensure that commands run consecutively the aditional requirement to the run script `-W
    depend=afterok:<prev_jobid>` is added. This allows for all the components of the experiment to
    be conducted in a single script.

    Note: Running this function requires that the command `qsub` exists, implying that a job
    scheduler is installed.

    """
    submit_job = True
    logger.debug('Creating commands in pbs files.')
    # Check qsub exists
    if shutil.which('qsub') is None:
        logger.warning('The `qsub` command is not found.'
                       'Skipping job submission and just generating files')
        submit_job = False

    # Ensure directory is a Path
    directory = Path(directory)

    # remove existing files
    for fname in directory.glob(basename+'*.pbs'):
        print('Removing {}'.format(fname))
        os.remove(fname)

    # Write new files and generate commands
    prev_jobid = None
    for index, command_group in enumerate(command_groups):
        # Generate pbs file
        content = create_pbs_file(command_group, pbs_options)
        # Write file to disk
        fname = Path(directory / '{}_{:02d}.pbs'.format(basename, index))
        with open(fname, 'w') as dst:
            dst.write(content)

        if submit_job:
            # Construct command
            submit_cmd = 'qsub '
            if index > 0:
                submit_cmd += '-W depend=afterok:{} '.format(prev_jobid)
            submit_cmd += str(fname)
            # acutally run the command
            cmd_res = subprocess.run(submit_cmd.split(), cwd=directory)
            assert cmd_res.returncode == 0, 'Submitting a job to the queue failed.'
            prev_jobid = cmd_res.stdout


@click.command()
@click.option('-f', '--input-file',
              type=click.Path(exists=True, dir_okay=False),
              default='experiment.yml',
              )
def main(input_file) -> None:
    # Process and run commands
    process_file(input_file)
