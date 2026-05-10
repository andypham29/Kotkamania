import os
import sqlalchemy as sa
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

# Create base for ORM models
Base = declarative_base()


class NhlPlayerStatLogORM(Base):
    """ORM model for NHL player stat log"""
    __tablename__ = 'nhl_player_stat_log'

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False, unique=True)
    description = Column(String)
    timeExecuted = Column(Integer)


# Database setup
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "log.db"))
os.makedirs(os.path.dirname(db_path), exist_ok=True)

# Create engine
engine = sa.create_engine(
    f'sqlite:///{db_path}',
    connect_args={'check_same_thread': False, 'timeout': 20},
    echo=False
)

# Bind metadata to engine
Base.metadata.bind = engine

# Create scoped session
Session = scoped_session(sessionmaker(bind=engine, expire_on_commit=False))
