# bytefmt - Convert a byte count into a human readable string
# Copyright (C) 2018 Ingo Ruhnke <grumbel@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import argparse
import sys

import bytefmt


def parse_args(argv):
    parser = argparse.ArgumentParser(description="Format bytes human-readable")

    parser.add_argument("BYTES", nargs=1)

    group = parser.add_argument_group("Formating Style")

    xgroup = group.add_mutually_exclusive_group()
    xgroup.add_argument("-d", "--decimal", action='store_true', default=False,
                        help="Use base 1000 SI units (kB, MB, GB, ...)")
    xgroup.add_argument("-b", "--binary", action='store_true', default=False,
                        help="Use base 1024 units (KiB, MiB, GiB, ...)")
    xgroup.add_argument("-g", "--gnu", action='store_true', default=False,
                        help="Use base 1024 GNU-ls style (K, M, G, ...)")

    group.add_argument("-c", "--compact", action='store_true', default=False,
                       help="Don't put a space between the unit and the value")
    group.add_argument("-u", "--unit", metavar="UNIT", type=str, default=None,
                       help="Display the value in UNIT, don't auto detect")
    group.add_argument("-p", "--precision", metavar="NUM", type=int, default=2,
                       help="Display the value with NUM digits")

    return parser.parse_args(argv)


def main(argv):
    args = parse_args(argv[1:])

    byte_count = bytefmt.dehumanize(args.BYTES[0])

    if args.binary:
        style = "binary"
    elif args.gnu:
        style = "gnu"
    else:  # args.decimal
        style = "decimal"

    print(bytefmt.humanize(byte_count, style=style,
                           compact=args.compact,
                           unit=args.unit,
                           precision=args.precision))


def main_entrypoint():
    main(sys.argv)


# EOF #
