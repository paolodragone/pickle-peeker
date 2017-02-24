
import dbm
import pickle
import shelve
import os.path


class Peeker(object):
    def __init__(self, filename, content='shelf'):
        self.filename = filename
        self.content = content
        self._exists = os.path.exists(filename)
        self._is_shelf = content == 'shelf' or dbm.whichdb(filename) == 'dbm.gnu'
        self.db = None
        self._modified = False

    def open(self):
        if not self._exists:
            if self.content == 'shelf':
                self.db = shelve.open(self.filename, flag='n')
            elif self.content == 'dict':
                self.db = {}
            elif self.content == 'list':
                self.db = []
            else:
                raise ValueError('content {} not supported'.format(self.content))
        elif self._is_shelf:
            self.db = shelve.open(self.filename)
        else:
            with open(self.filename, 'rb') as f:
                self.db = pickle.load(f)

    def close(self):
        if self._is_shelf:
            self.db.close()
        elif self._modified:
            with open(self.filename, 'wb') as f:
                pickle.dump(self.db, f)

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def peek(self, key):
        if self._is_shelf or isinstance(self.db, dict):
            return self.db[key]
        if isinstance(self.db, list):
            key = int(key)
            return self.db[key]
        raise ValueError('Not a shelf, dictionary, or list')

    def peek_keys(self):
        if self._is_shelf or isinstance(self.db, dict):
            return sorted(self.db.keys())
        elif isinstance(self.db, list):
            return len(self.db)
        raise ValueError('Not a shelf, dictionary, or list')

    def update(self, key, value):
        if self._is_shelf or isinstance(self.db, dict):
            self.db[key] = value
            self._modified = True
            return key, value
        elif isinstance(self.db, list):
            key = int(key)
            if key == -1:
                self.db.append(value)
            else:
                self.db[key] = value
            self._modified = True
            return key, value
        raise ValueError('Not a shelf, dictionary, or list')


def peek(filename, key='args'):
    with Peeker(filename) as peeker:
        return peeker.peek(key)


def peek_keys(filename):
    with Peeker(filename) as peeker:
        return peeker.peek_keys()


def update(filename, key, value, content='shelf'):
    with Peeker(filename, content) as peeker:
        return peeker.update(key, value)

