import logging
from uuid import uuid4 as uuid

import lmdb

from .benchmark import benchmark

LOGGER = logging.getLogger(__name__)
PREFIX = "LMDB: "


def setup(count):
    LOGGER.info(f"LMDB: Preparing fixture for {count} entries.")
    database = lmdb.open("./store.lmdb", readahead=False)
    records = {(str(uuid()) * 4).encode('utf-8'): str(uuid()).encode('utf-8') for _ in range(count)}
    LOGGER.info(f"LMDB: Fixture setup is done.")
    return database, records


@benchmark(prefix=PREFIX)
def test_write(database, records):
    for key, value in records:
        with database.begin(write=True) as txn:
            txn.put(key, value)


@benchmark(prefix=PREFIX)
def test_read(database, records):
    for key, value in records:
        with database.begin(write=False) as txn:
            assert txn.get(key) == value
