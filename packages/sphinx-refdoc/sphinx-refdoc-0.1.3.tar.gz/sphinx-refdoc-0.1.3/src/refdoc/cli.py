# -*- coding: utf-8 -*-
"""
cli interface. Very simple for now.
"""
from __future__ import absolute_import
import click

from .logic import generate_docs


@click.command()
@click.option('-i', '--input-pkg', metavar='<package_path>', multiple=True)
@click.option('-o',  '--out', metavar='<dst_dir>')
@click.option('--no-index', is_flag=True)
def docs(input_pkg, out, no_index):
    """ Generate reference documentation for all packages found in src_dir. """
    generate_docs(input_pkg, out, no_index)
