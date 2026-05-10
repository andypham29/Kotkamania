"""
SQLAlchemy ORM models for the internal database
"""
import os
import sqlalchemy as sa
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import datetime

# Create base for ORM models
Base = declarative_base()

# Database setup
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "internal.db"))
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


class FantasyNhlPlayerORM(Base):
    """ORM model for fantasy_nhl_player table"""
    __tablename__ = 'fantasy_nhl_player'

    playerId = Column(Integer, primary_key=True)
    skaterFullName = Column(String, nullable=False)
    positionCode = Column(String, nullable=False)
    teamId = Column(Integer, nullable=False)
    fantasyGrade = Column(Float)
    yahooEligibility = Column(String)
    avgPick = Column(Float)
    avgRound = Column(Float)
    percentDrafted = Column(String)
    teamName = Column(String, nullable=False)
    nhlRank = Column(Integer)
    scoring = Column(Float)
    playmaking = Column(Float)
    defense = Column(Float)
    powerplay = Column(Float)
    intangibles = Column(Float)


class InternalPlayerStatORM(Base):
    """ORM model for internal_player_stat table"""
    __tablename__ = 'internal_player_stat'

    id = Column(Integer, primary_key=True)
    playerId = Column(Integer, nullable=False)
    seasonId = Column(Integer, nullable=False)
    timeOnIce = Column(String)
    assists = Column(Integer)
    goals = Column(Integer)
    pim = Column(Integer)
    shots = Column(Integer)
    games = Column(Integer)
    hits = Column(Integer)
    powerPlayGoals = Column(Integer)
    powerPlayPoints = Column(Integer)
    powerPlayTimeOnIce = Column(String)
    evenTimeOnIce = Column(String)
    penaltyMinutes = Column(Integer)
    faceOffPct = Column(Float)
    shotPct = Column(Float)
    gameWinningGoals = Column(Integer)
    overTimeGoals = Column(Integer)
    shortHandedGoals = Column(Integer)
    shortHandedPoints = Column(Integer)
    shortHandedTimeOnIce = Column(String)
    blocked = Column(Integer)
    plusMinus = Column(Integer)
    points = Column(Integer)
    shifts = Column(Integer)
    timeOnIcePerGame = Column(String)
    evenTimeOnIcePerGame = Column(String)
    shortHandedTimeOnIcePerGame = Column(String)
    powerPlayTimeOnIcePerGame = Column(String)


class FantasyPlayerStreakIndexORM(Base):
    """ORM model for fantasy_streak table"""
    __tablename__ = 'fantasy_streak'

    playerId = Column(Integer, primary_key=True)
    skaterFullName = Column(String, nullable=False)
    positionCode = Column(String, nullable=False)
    pts = Column(Integer, nullable=False)
    toi = Column(Float, nullable=False)
    pptoi = Column(Float, nullable=False)
    streakIndex = Column(Float, nullable=False)
    lastUpdated = Column(String)

