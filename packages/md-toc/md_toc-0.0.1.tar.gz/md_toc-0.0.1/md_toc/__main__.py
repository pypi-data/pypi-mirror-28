#
# __main__.py
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
"""Call the CLI parser."""

import sys
from .cli import CliInterface


def main(args=None):
    """Call the CLI interface and wait for the result."""
    retcode = 0
    try:
        ci = CliInterface()
        args = ci.parser.parse_args()
        result = args.func(args)
        if result is not None:
            print(result)
        retcode = 0
    except Exception as e:
        retcode = 1
        print(e)
    sys.exit(retcode)


if __name__ == '__main__':
    main()
