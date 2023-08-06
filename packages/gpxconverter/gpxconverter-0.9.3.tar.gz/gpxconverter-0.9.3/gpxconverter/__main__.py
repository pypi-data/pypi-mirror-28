#!/usr/bin/env python3

import sys
import argparse
from converter import convert


def main():
    args = sys.argv[1:]
    parser = argparse.ArgumentParser(prog='gpxconvert')
    parser.add_argument(
        '-i',
        nargs=1,
        metavar='file path',
        help='input file',
    )
    parser.add_argument(
        '-o',
        required=False,
        metavar='output file name',
        help='out file name without csv extension',
    )
    args = parser.parse_args(args)
    try:
        convert(**vars(args))
    except Exception as exc:
        print(exc)


if __name__ == "__main__":
    sys.exit(main())
