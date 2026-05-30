"""
Database module for SQLAlchemy setup and session management
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from contextlib import contextmanager
import os


class DatabaseManager:
    """Singleton class for database management with SQLAlchemy"""

    _instances = {}
    _session_factories = {}

    @classmethod
    def _normalize_uri(cls, uri: str = None) -> str:
        if uri is None:
            # database.py lives at server/commons/db/; the DB lives at server/internaldata/db/internal.db
            db_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'internaldata', 'db')
            os.makedirs(db_dir, exist_ok=True)
            uri = os.path.join(db_dir, 'internal.db')

        if uri.startswith('sqlite://'):
            return uri
        if not os.path.isabs(uri):
            uri = os.path.abspath(uri)
        return f'sqlite:///{uri.replace(os.sep, "/")}'

    @classmethod
    def get_engine(cls, uri: str = None):
        """Get or create SQLAlchemy engine for a database URI"""
        uri = cls._normalize_uri(uri)
        if uri not in cls._instances:
            cls._instances[uri] = create_engine(
                uri,
                connect_args={'check_same_thread': False, 'timeout': 20},
                poolclass=StaticPool,
                echo=False,
            )
        return cls._instances[uri]

    @classmethod
    def get_session_factory(cls, uri: str = None):
        """Get or create SQLAlchemy session factory"""
        uri = cls._normalize_uri(uri)
        engine = cls.get_engine(uri)
        if uri not in cls._session_factories:
            cls._session_factories[uri] = sessionmaker(bind=engine, expire_on_commit=False)
        return cls._session_factories[uri]

    @classmethod
    def get_session(cls, uri: str = None) -> Session:
        """Get a new SQLAlchemy session"""
        session_factory = cls.get_session_factory(uri)
        return session_factory()

    @classmethod
    @contextmanager
    def session_scope(cls, uri: str = None):
        """Provide a transactional scope for SQLAlchemy sessions"""
        session = cls.get_session(uri)
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @classmethod
    def create_tables(cls, base, uri: str = None):
        """Create all tables from Base metadata"""
        engine = cls.get_engine(uri)
        base.metadata.create_all(engine)

