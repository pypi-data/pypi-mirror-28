import collections
import io
import sqlite3
import numpy as np

__all__ = ['sql_table_drop', 'sql_table_info', 'sql_table_nrows', 'sql_tables', 'sql2ndarray',
           'ndarray2sql', 'SQLLeftJoin']

sqlite3_types = {
    np.int64: 'INTEGER',
    np.float64: 'REAL',
    np.str_: 'TEXT'}


class asconnection():
    """
    if the argument is a string, return a Connection to the database on
    entering and close it on exiting.

    """
    def __init__(self, database):
        if not isinstance(database, (str, sqlite3.Connection)):
            raise TypeError('Invalid database name or connection.')
        self.arg = database

    def __enter__(self):
        if isinstance(self.arg, str):
            self.connection = sqlite3.connect(
                self.arg, detect_types=sqlite3.PARSE_DECLTYPES)
        else:
            self.connection = self.arg
        return self.connection

    def __exit__(self, *exc):
        if isinstance(self.arg, str):
            self.connection.close()
        return False


def sql_table_drop(database, name):
    """
    Drop table.

    """
    with asconnection(database) as connection:
        request = 'DROP TABLE {}'.format(sql_escape(name))
        with connection:
            connection.execute(request)


def sql_table_info(database, name):
    """
    Return information about columns in a table.

    """
    with asconnection(database) as connection:
        request = 'PRAGMA table_info({});'.format(sql_escape(name))
        with connection:
            return connection.execute(request).fetchall()


def sql_table_nrows(database, name):
    """
    Return the number of rows in a table.

    """
    with asconnection(database) as connection:
        request = 'SELECT Count(*) FROM {}'.format(sql_escape(name))
        with connection:
            return connection.execute(request).fetchone()[0]


def sql_tables(database):
    """
    Return the names of the tables in a database.

    """
    with asconnection(database) as connection:
        request = 'SELECT name FROM sqlite_master WHERE type="table"'
        with connection:
            out = connection.execute(request).fetchall()
    return [_[0] for _ in out]


def _get_unicode_name(name):
    try:
        uname = name.encode('utf-8', 'strict').decode('utf-8')
    except UnicodeError:
        raise ValueError("Cannot convert identifier to UTF-8: '%s'" % name)
    return uname


def sql_escape(name):
    # See http://stackoverflow.com/questions/6514274/how-do-you-escape-strings\
    # -for-sqlite-table-column-names-in-python
    # Ensure the string can be encoded as UTF-8.
    # Ensure the string does not include any NUL characters.
    # Replace all " with "".
    # Wrap the entire thing in double quotes.
    uname = _get_unicode_name(name)
    if not len(uname):
        raise ValueError('Empty table or column name specified.')
    if uname.find('\x00') != -1:
        raise ValueError('SQLite identifier cannot contain NULLs.')
    return '"' + uname.replace('"', '""') + '"'


def _has_table(connection, name):
    request = 'SELECT name FROM sqlite_master WHERE type="table" AND name=?'
    return len(connection.execute(request, [name]).fetchall()) > 0


def _create_table(connection, table, valid_names, dtypes):
    columns = ['"id" INTEGER PRIMARY KEY']
    for v, d in zip(valid_names, dtypes):
        columns.append('{} {}'.format(v, d))
    request = 'CREATE TABLE IF NOT EXISTS {} ({})'.format(
        table, ', '.join(columns))
    connection.execute(request)


sqlite3.register_adapter(np.int64, lambda val: int(val))


types = {
    np.int64: 'INTEGER',
    np.float64: 'FLOAT',
    np.str_: 'TEXT'}
rev_types = {v: k for k, v in types.items()}


def ndarray2sql(database, table, data, if_exists='fail'):
    """
    Write ndarray into sqlite database.

    """

    if isinstance(data, (list, tuple)) and \
       isinstance(data[0], (list, tuple)) and \
       isinstance(data[0][0], str):
        data = collections.OrderedDict(data)

    if not isinstance(data, (np.ndarray, collections.Mapping)):
        raise TypeError('The input is not a numpy array.')

    if isinstance(data, np.ndarray):
        dtype = data.dtype
        if dtype.fields is None:
            raise TypeError('The input array is not structured.')
        names = list(dtype.names)
        try:
            ids = data['id']
            names.remove('id')
        except ValueError:
            ids = np.arange(1, len(data) + 1)
        values = [data[_] for _ in names]
    else:
        if any(not isinstance(_, collections.Iterable) for _ in data.values()):
            raise TypeError('The input dict values are not iterable.')
        names = list(data.keys())
        try:
            ids = data['id']
            names.remove('id')
        except KeyError:
            ids = np.arange(1, len(data[names[0]]) + 1)
        values = [np.asarray(data[_]) for _ in names]
    dtypes = [_.dtype for _ in values]

    valid_table = sql_escape(table)
    valid_names = [sql_escape(_) for _ in names]
    sqltypes = [types[_.type] for _ in dtypes]

    with asconnection(database) as connection:
        if _has_table(connection, table) and if_exists == 'fail':
            raise sqlite3.OperationalError(
                'table {!r} already exists'.format(table))
        _create_table(connection, valid_table, valid_names, sqltypes)
        request = 'REPLACE INTO {} (id, {}) VALUES (?, {})'.format(
            valid_table, ', '.join(valid_names), ', '.join(len(names) * ['?']))
        with connection:
            connection.executemany(request, zip(ids, *values))


def sql2ndarray(database, table, restriction=None):
    """
    Extract sqlite database as ndarray.

    """
    with asconnection(database) as connection:

        if isinstance(restriction, slice):
            start = restriction.start or 0
            stop = restriction.stop or sql_table_nrows(connection, table)
            where = 'WHERE id >= {} AND id <= {}'.format(start + 1, stop)
        elif isinstance(restriction, str):
            where = restriction
        else:
            where = ''

        request = 'SELECT * FROM {} {} ORDER BY id'.format(
            sql_escape(table), where)
        with connection:
            data = connection.execute(request).fetchall()

        if len(data) == 0:
            # we grab any row to know the length of the TEXT columns
            request = 'SELECT * FROM {} LIMIT 1'.format(sql_escape(table))
            with connection:
                data_ = connection.execute(request).fetchall()
        else:
            data_ = data

        info = sql_table_info(connection, table)
        length = len(info) * [0]
        for icol, infocol in enumerate(info):
            if infocol[2] == 'TEXT':
                length[icol] = max((len(_[icol]) for _ in data_))

        dtype = []
        for info_, length_ in zip(info, length):
            if length_ > 0:
                dtype_ = '<U{}'.format(length_)
            else:
                dtype_ = rev_types[info_[2]]
            dtype.append((info_[1], dtype_))
        return np.array(data, dtype=dtype)


class SQLLeftJoin:
    """
    Perform a left join onto 2 sql databases read by sql2ndarray.

    """
    def __init__(self, table_left, field_left, table_right, field_right=None):
        if field_right is None:
            field_right = field_left
        hash = {v: i for i, v in enumerate(table_right[field_right])}
        self.index = np.array([hash.get(_, -1) for _ in table_left[field_left]], dtype=int)
        self.len_table_left = len(table_left)
        self.table_right = table_right

    def __call__(self, ids, field_right=None, assert_missing=False):
        input_is_bool = False
        if field_right is None:
            field_right = ids
            ids = slice(None)
            nrows = self.len_table_left
        else:
            if isinstance(ids, np.ndarray) and ids.dtype == bool:
                if ids.size != self.len_table_left:
                    raise ValueError('Invalid size for the selection mask.')
                ids = np.arange(self.len_table_left)[ids]
                input_is_bool = True
            else:
                ids = np.asarray(ids) - 1
            nrows = len(ids)
        if isinstance(field_right, str):
            field_right_ = (field_right,)
        else:
            field_right_ = field_right
        index = self.index[ids]
        isnotnone = index != -1
        out = tuple(np.empty(nrows, dtype=self.table_right[_].dtype) for _ in field_right_)
        for ifield, field in enumerate(field_right_):
            out[ifield][isnotnone] = self.table_right[field][index[isnotnone]]
        if isinstance(field_right, str):
            out = out[0]
        if assert_missing:
            assert np.all(isnotnone)
            return out
        if input_is_bool:
            # is the input is a boolean mask, return a boolean mask of the same
            # size
            isnone = np.zeros(self.len_table_left, bool)
            isnone[ids[~isnotnone]] = True
            return out, isnone
        return out, ~isnotnone
