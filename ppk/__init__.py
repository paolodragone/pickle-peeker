
from . import _ppk
from ._ppk import *

__version__ = '0.1.3'


def main():
    import argparse
    from textwrap import dedent

    desc = dedent('''\
        Pickle peeker is a smart pickle reader.
    ''')

    fmt = argparse.ArgumentDefaultsHelpFormatter
    parser = argparse.ArgumentParser(description=desc, formatter_class=fmt)
    parser.add_argument('--version', action='version',
                        version='ppk version: {}'.format(__version__))
    parser.add_argument('file', type=str,
                        help='the pickle file to peek')
    parser.add_argument('-k', '--key', type=str, default='header',
                        help='the content key to peek')
    parser.add_argument('-K', '--keys', action='store_true',
                        help='show the list of keys in the file')
    parser.add_argument('-H', '--header', type=str,
                        help='add or replace the header of the file')
    parser.add_argument('-C', '--content', type=str,
                        help='replace the content of the file')
    args = parser.parse_args()

    if args.keys:
        peek_keys(args.file)
    elif args.header or args.content:
        modify(args.file, args.header, args.content)
    else:
        peek(args.file, args.key)

if __name__ == '__main__':
    main()


