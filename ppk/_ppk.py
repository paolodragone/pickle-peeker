
import ast
import pickle
import os.path
import contextlib
from pprint import pprint


def dict_view(d, sep=' '):
    s = []
    for item in d.items():
        s.append(': '.join(item))
    return sep.join(s)


def peek_keys(fname):
    with open(fname, 'rb') as f:
        pf = pickle.load(f)

    if isinstance(pf, dict):
        keys = sorted(pf.keys())
        print('\n'.join(keys))
        return keys
    else:
        pprint(pf)
        return pf


def peek(fname, key='header'):
    with open(fname, 'rb') as f:
        pf = pickle.load(f)

    if isinstance(pf, dict) and key in pf:
        if isinstance(pf[key], str):
            print(pf[key])
        if isinstance(pf[key], dict):
            dict_view(pf[key])
        else:
            pprint(pf[key])
        return pf[key]
    if isinstance(pf, list):
        with contextlib.suppress(ValueError):
            key = int(key)
            pprint(pf[key])
            return pf[key]
    pprint(pf)
    return pf


def dump(fname, header, content):
    if content and isinstance(content, dict):
        if 'header' in content:
            raise ValueError("Content contains a 'header' item")
        pf = {'header': header, **content}
    else:
        pf = {'header': header, 'content': content}
    with open(fname, 'wb') as f:
        pickle.dump(pf, f)
    return pf


def modify(fname, header=None, content=None):
    if os.path.exists(fname):
        with open(fname, 'rb') as f:
            pf = pickle.load(f)
    elif header and content:
        dump(fname, header, content)
    else:
        raise ValueError('The file does not exist.')

    if header:
        header = ast.literal_eval(header)
    elif pf and isinstance(pf, dict) and 'header' in pf:
        header = pf['header']
    else:
        header = None

    if content:
        content = ast.literal_eval(content)
    elif pf:
        if isinstance(pf, dict):
            content = {k: v for k, v in pf.items() if k != 'header'}
        else:
            content = pf
    else:
        content = None

    dump(fname, header, content)
    return pf

