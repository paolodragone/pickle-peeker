
import pickle
import contextlib
from pprint import pprint

__version__ = '0.1.0'


def peek(args):
    with open(args['file'], 'rb') as f:
        pf = pickle.load(f)

    key = args['key']
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
    args = parser.parse_args()
    peek(vars(args))

