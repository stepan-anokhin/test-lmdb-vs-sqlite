import logging
import sys

import perftest.lmdb
import perftest.sqlite


def test_lmdb(count):
    database, records = perftest.lmdb.setup(count)

    perftest.lmdb.test_write(database, records.items())
    perftest.lmdb.test_read(database, records.items())


def test_sqlite(count):
    database, records = perftest.sqlite.setup(count)

    perftest.sqlite.test_write(database, records.items())
    perftest.sqlite.test_read(database, records.items())


if __name__ == '__main__':
    logging.getLogger("perftest").setLevel(logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

    trials = 10 ** 3
    test_lmdb(trials)
    test_sqlite(trials)
