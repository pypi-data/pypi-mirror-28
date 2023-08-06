import collections
import numpy as np
import os
import shutil
import tempfile
import uuid
from numpy.testing import assert_equal
from sqlite3ndarray import asconnection, ndarray2sql, sql2ndarray, sql_tables
from uuid import uuid1

dirname = os.path.join(tempfile.gettempdir(),
                       'test-sqlite3ndarray-' + uuid.uuid4().hex)
dbname = os.path.join(dirname, 'database.db')
dtype_array = [('field1', int),
               ('field2', float),
               ('field3', 'U10'),
              ]
#               ('field1arr', (int, 3)),
#               ('field2arr', (float, 5)),
#               ('field3arr', (np.float32, (2, 3)))]
array_size = 10
field_names = [_[0] for _ in dtype_array]
field_values = [
    np.arange(array_size),
    np.array([2.**_ for _ in range(array_size - 1)] + [np.nan]),
    np.array([uuid.uuid4().hex[:10] for _ in range(array_size)]),
    ]
#    np.random.random_integers(10, size=(array_size, 3)),
#    np.random.random_integers(10, size=(array_size, 5)).astype(float),
#    np.random.random_integers(9, size=(array_size, 2, 3)).astype(np.float32)]


def setup():
    os.mkdir(dirname)


def teardown():
    shutil.rmtree(dirname)


def test_ndarray():
    def func(col, restriction):
        actual = array[col]
        expected = orig[col]
        if restriction is not None:
            actual = actual
            expected = expected[restriction]
        assert_equal(actual.shape, expected.shape)
        check = actual == expected
        if expected.dtype == float:
            check |= np.isnan(actual) & np.isnan(expected)
        assert np.alltrue(check)

    slices = (None, slice(None, None), slice(1, None), slice(None, 4),
              slice(5, 8), slice(4, 4))

    for type_ in 'ndarray', 'dict':
        if type_ == 'ndarray':
            orig = np.empty(array_size, dtype_array)
        else:
            orig = collections.OrderedDict()
        for name, value in zip(field_names, field_values):
            orig[name] = value
        ndarray2sql(dbname, type_, orig)
        for restriction in slices:
            array = sql2ndarray(dbname, type_, restriction=restriction)
            assert_equal(array.dtype,[('id', int)] + dtype_array)
            for col in field_names:
                yield func, col, restriction


def test_sql_tables():
    dbname2 = dbname + '.2'
    with asconnection(dbname2) as connection:
        connection.execute('CREATE TABLE table1 (a INTEGER, b REAL)')
        connection.execute('CREATE TABLE table2 (c INTEGER, d REAL)')
        tables = sql_tables(connection)
    assert 'table1' in tables
    assert 'table2' in tables
