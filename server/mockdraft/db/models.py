"""
SQLAlchemy ORM models for the mockdraft database
"""
import os
import sqlalchemy as sa
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

# Create base for ORM models
Base = declarative_base()


class ProspectEliteORM(Base):
    """ORM model for elite prospects"""
    __tablename__ = 'eliteprospect'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    position = Column(String)
    avg_rank = Column(String)
    hp = Column(String)
    fc = Column(String)
    iss = Column(String)
    mh = Column(String)
    elite = Column(String)
    league = Column(String)
    team = Column(String)
    gp = Column(String)
    g = Column(String)
    a = Column(String)
    p = Column(String)
    pim = Column(String)


class ProspectORM(Base):
    """ORM model for prospects"""
    __tablename__ = 'prospects'

    id = Column(Integer, primary_key=True)
    rank = Column(String, nullable=False)
    player_name = Column(String, nullable=False)
    height = Column(String, nullable=False)
    weight = Column(String, nullable=False)
    position = Column(String, nullable=False)
    team = Column(String, nullable=False)
    league = Column(String, nullable=False)


# Database setup
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "eliteprospect.db"))
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

