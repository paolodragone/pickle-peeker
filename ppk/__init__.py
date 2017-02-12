
import ast
import pickle
import os.path
import contextlib
from pprint import pprint


__version__ = '0.1.2'


def peek(args):
    with open(args.file, 'rb') as f:
        pf = pickle.load(f)

    key = args.key
    if isinstance(pf, dict) and key in pf:
        pprint(pf[key])
        return pf[key]
    if isinstance(pf, list):
        with contextlib.suppressi(ValueError):
            key = int(key)
            pprint(pf[key])
            return pf[key]
    pprint(pf)
    return pf


def modify(args):
    if os.path.exists(args.file):
        pf = pickle.load(f)
    else:
        pf = None

    if args.header:
        header = ast.literal_eval(args.header)
    elif pf and isinstance(pf, dict) and 'header' in pf:
        header = pf['header']
    else:
        header = None

    if args.content:
        content = ast.literal_eval(args.content)
    elif pf:
        if isinstance(pf, dict) and 'content' in pf:
            content = pf['content']
        else:
            content = pf
    else:
        content = None

    pf = {'header': header, 'content': content}
    with open(args.file, 'wb') as f:
        pickle.dump(pf, f)

    return pf


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
    parser.add_argument('-H', '--header', type=str,
                        help='add or replace the header of the file')
    parser.add_argument('-C', '--content', type=str,
                        help='replace the content of the file')
    args = parser.parse_args()

    if args.header or args.content:
        modify(args)
    else:
        peek(args)

