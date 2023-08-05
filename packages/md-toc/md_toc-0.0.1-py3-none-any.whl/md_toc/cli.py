#
# cli.py
#
# Copyright (C) 2017 frnmst (Franco Masotti) <franco.masotti@live.com>
#                                            <franco.masotti@student.unife.it>
#
# This file is part of md-toc.
#
# md-toc is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# md-toc is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with md-toc.  If not, see <http://www.gnu.org/licenses/>.
#
"""Command line interface file."""

import argparse
import pkg_resources
from .api import (write_toc_on_md_file, build_toc)


class CliToApi():
    """An interface between the CLI and API functions."""

    def write_toc_on_md_file(self, args):
        """Write the table of contents on the markown file."""
        if args.toc_marker is None:
            args.toc_marker = '[](TOC)'
        result = write_toc_on_md_file(
            args.filename,
            toc=build_toc(args.filename, args.ordered),
            in_place=args.in_place,
            toc_marker=args.toc_marker)
        if result is not None:
            print(result, end='')


class CliInterface():
    """The interface exposed to the final user."""

    def __init__(self):
        """Set the parser variable that will be used instead of using create_parser."""
        self.parser = self.create_parser()

    def create_parser(self):
        """Create the CLI parser."""
        parser = argparse.ArgumentParser(
            description='Markdown Table Of Contents',
            epilog="Return values: 0 OK, 1 \
                                         Error, 2 Invalid command")
        subparsers = parser.add_subparsers(dest='command')
        subparsers.required = True
        write_toc_prs = subparsers.add_parser(
            'wtoc', help='write the table of contents')
        write_toc_prs.add_argument(
            'filename', metavar='FILE_NAME', help='the i/o file name')
        write_toc_prs.add_argument(
            '-i',
            '--in-place',
            help='overwrite the input file',
            action='store_true')
        write_toc_prs.add_argument(
            '-o',
            '--ordered',
            help='write as an ordered list',
            action='store_true')
        write_toc_prs.add_argument(
            '-t',
            '--toc-marker',
            help='set the string to be used as the marker \
                  for positioning the table of contents')
        parser.add_argument(
            '-v',
            '--version',
            action='version',
            version=pkg_resources.get_distribution('md_toc').version)
        write_toc_prs.set_defaults(func=CliToApi().write_toc_on_md_file)

        return parser
