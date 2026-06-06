"""
SQLAlchemy ORM models for the internal database
"""
import os
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from server.commons.db import DatabaseManager

# Create base for ORM models
Base = declarative_base()
DatabaseManager.create_tables(Base)

# Database setup
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../server/internaldata/db/internal.db"))
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

class InternalPlayerStatPercentileORM(Base):
    """ORM model for internal_player_stat table"""
    __tablename__ = 'internal_player_stat_percentile'

    id = Column(Integer, primary_key=True)
    playerId = Column(Integer, nullable=False)
    seasonId = Column(Integer, nullable=False)
    timeOnIce = Column(Integer)
    assists = Column(Integer)
    goals = Column(Integer)
    pim = Column(Integer)
    shots = Column(Integer)
    games = Column(Integer)
    hits = Column(Integer)
    powerPlayGoals = Column(Integer)
    powerPlayPoints = Column(Integer)
    powerPlayTimeOnIce = Column(Integer)
    evenTimeOnIce = Column(Integer)
    penaltyMinutes = Column(Integer)
    faceOffPct = Column(Integer)
    shotPct = Column(Integer)
    gameWinningGoals = Column(Integer)
    overTimeGoals = Column(Integer)
    shortHandedGoals = Column(Integer)
    shortHandedPoints = Column(Integer)
    shortHandedTimeOnIce = Column(Integer)
    blocked = Column(Integer)
    plusMinus = Column(Integer)
    points = Column(Integer)
    shifts = Column(Integer)
    timeOnIcePerGame = Column(Integer)
    evenTimeOnIcePerGame = Column(Integer)
    shortHandedTimeOnIcePerGame = Column(Integer)
    powerPlayTimeOnIcePerGame = Column(Integer)


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


class DomainDraftboardORM(Base):
    """ORM model for internal_draftboard table."""
    __tablename__ = 'internal_draftboard'

    id = Column(String, primary_key=True)
    favorites = Column(JSON, nullable=False, default=list)
    watchlist = Column(JSON, nullable=False, default=list)
    draftboard = Column(JSON, nullable=False, default=list)
    drafted = Column(JSON, nullable=False, default=list)
    createdAt = Column(DateTime, nullable=False, default=datetime.utcnow)


class GoalieStatTable(Base):
    __tablename__ = "internal_goalie_stat"

    id = Column(Integer, primary_key=True)
    playerId = Column(Integer, nullable=False)
    seasonId = Column(Integer, nullable=False)
    assists = Column(Integer)
    gamesPlayed = Column(Integer)
    gamesStarted = Column(Integer)
    goalieFullName = Column(String)
    goals = Column(Integer)
    goalsAgainst = Column(Integer)
    goalsAgainstAverage = Column(Float)
    lastName = Column(String)
    losses = Column(Integer)
    otLosses = Column(Integer)
    penaltyMinutes = Column(Integer)
    points = Column(Integer)
    savePct = Column(Float)
    saves = Column(Integer)
    shootsCatches = Column(String)
    shotsAgainst = Column(Integer)
    shutouts = Column(Integer)
    teamAbbrevs = Column(String)
    ties = Column(Integer)
    timeOnIce = Column(Integer)
    wins = Column(Integer)

# Create all tables if they don't exist (after all ORM classes are defined)
Base.metadata.create_all(engine)


def _migrate_internal_draftboard() -> None:
    with engine.begin() as conn:
        rows = conn.execute(sa.text("PRAGMA table_info(internal_draftboard)")).fetchall()
        if not rows:
            return
        columns = {row[1] for row in rows}
        if "drafted" not in columns:
            conn.execute(sa.text(
                "ALTER TABLE internal_draftboard ADD COLUMN drafted JSON NOT NULL DEFAULT '[]'"
            ))


_migrate_internal_draftboard()


