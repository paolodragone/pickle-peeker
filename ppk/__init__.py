
from . import _ppk
from ._ppk import *

import ast
from pprint import pprint, pformat

__version__ = '0.2.0'


def _pprint(obj):
    if isinstance(obj, str):
        print(obj)
    elif isinstance(obj, dict):
        print(' '.join([': '.join([k, pformat(v)]) for k, v in obj.items()]))
    else:
        pprint(obj)


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
    parser.add_argument('-C', '--content', choices={'shelf', 'dict', 'list'},
                        default='shelf', help='the content of a new file')
    parser.add_argument('-k', '--key', type=str, default='args',
                        help='the content key to peek or update')
    parser.add_argument('-K', '--keys', action='store_true',
                        help='show the list of keys in the file')
    parser.add_argument('-V', '--value', type=str,
                        help='update the value for the given key')
    args = parser.parse_args()

    if args.keys:
        keys = _ppk.peek_keys(args.file)
        if isinstance(keys, list):
            print('\n'.join(keys))
        else:
            pprint(keys)
    elif args.value:
        value = ast.literal_eval(args.value)
        _ppk.update(args.file, args.key, value)
        _pprint(value)
    else:
        _pprint(_ppk.peek(args.file, args.key))


if __name__ == '__main__':
    main()


