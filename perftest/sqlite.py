import logging
from contextlib import contextmanager
from uuid import uuid4 as uuid

from sqlalchemy import Column, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .benchmark import benchmark

Base = declarative_base()

LOGGER = logging.getLogger(__name__)
PREFIX = "SQLite: "


class Database:
    """Database class provides session factory and convenience methods to access database."""

    @staticmethod
    def in_memory(**options):
        """Create in-memory database."""
        return Database('sqlite:///:memory:', **options)

    def __init__(self, uri, base=Base, **options):
        """Create a new database instance.

        Each database instance will allocate it's own resources (connections, etc.).

        Args:
            uri (str): Database connection uri.
        """
        self.engine = create_engine(uri, **options)
        self.session = sessionmaker(bind=self.engine)
        self.base = base

    def create_tables(self):
        """Creates all tables specified on our internal schema."""
        self.base.metadata.create_all(bind=self.engine)

    def drop_tables(self):
        """Drop database."""
        self.base.metadata.drop_all(bind=self.engine)

    @contextmanager
    def session_scope(self):
        """Provide a transactional scope."""
        session = self.session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


class Entry(Base):
    __tablename__ = 'entry'
    key = Column(String, primary_key=True)
    value = Column(String)


def setup(count):
    LOGGER.info(f"SQLite: Preparing fixture for {count} entries.")
    database = Database(uri="sqlite:///store.sqlite", base=Base)
    database.create_tables()
    records = {str(uuid()) * 4: str(uuid()) for _ in range(count)}
    LOGGER.info("SQLite: Fixture setup is done.")
    return database, records


@benchmark(prefix=PREFIX)
def test_write(database: Database, records):
    for key, value in records:
        with database.session_scope() as session:
            session.add(Entry(key=key, value=value))


@benchmark(prefix=PREFIX)
def test_read(database, records):
    for key, value in records:
        with database.session_scope() as session:
            entry = session.query(Entry).filter(Entry.key == key).one_or_none()
            assert entry.value == value
