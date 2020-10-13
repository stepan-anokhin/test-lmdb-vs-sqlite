# LMDB vs SQLite simple performance test

This is a super-simple performance test of [LMDB](https://en.wikipedia.org/wiki/Lightning_Memory-Mapped_Database)
vs [SQLite](https://www.sqlite.org/index.html) + [SQLAlchemy](https://www.sqlalchemy.org/) Key-Value storage.


## Usage

Tested on python version: `3.8.4`

Install dependencies:
```bash
pip install -r requirements.txt
```

Run tests:
```bash
python3 main.py --count=1000
```

## Results 

For 1000 trials:
```
LMDB: Preparing fixture for 1000 entries.
LMDB: Fixture setup is done.
LMDB: test_write(...) took 0:00:20.886244
LMDB: test_read(...) took 0:00:00.001448
SQLite: Preparing fixture for 1000 entries.
SQLite: Fixture setup is done.
SQLite: test_write(...) took 0:00:45.955580
SQLite: test_read(...) took 0:00:00.803349
```
