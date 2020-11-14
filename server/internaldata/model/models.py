import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()
engine = sa.create_engine('sqlite:///../../server/internaldata/db/internal.db', echo=True)
base.metadata.bind = engine
session = orm.scoped_session(orm.sessionmaker())(bind=engine)


def row2dict(row):
    return {c.name: str(getattr(row, c.name)) for c in row.__table__.columns}


class InternalPlayer(base):
    __tablename__ = 'internalplayer'

    id = sa.Column(sa.Integer, primary_key=True)
    assists = sa.Column(sa.Integer, nullable=True)
    evGoals = sa.Column(sa.Integer, nullable=True)
    evPoints = sa.Column(sa.Integer, nullable=True)
    faceoffWinPct = sa.Column(sa.Float, nullable=True)
    gameWinningGoals = sa.Column(sa.Integer, nullable=True)
    gamesPlayed = sa.Column(sa.Integer, nullable=True)
    goals = sa.Column(sa.Integer, nullable=True)
    lastName = sa.Column(sa.Text, nullable=True)
    otGoals = sa.Column(sa.Integer, nullable=True)
    penaltyMinutes = sa.Column(sa.Text, nullable=True)
    playerId = sa.Column(sa.Integer, nullable=True)
    plusMinus = sa.Column(sa.Integer, nullable=True)
    points = sa.Column(sa.Integer, nullable=True)
    pointsPerGame = sa.Column(sa.Integer, nullable=True)
    positionCode = sa.Column(sa.Text, nullable=True)
    ppGoals = sa.Column(sa.Integer, nullable=True)
    ppPoints = sa.Column(sa.Integer, nullable=True)
    seasonId = sa.Column(sa.Text, nullable=True)
    shGoals = sa.Column(sa.Integer, nullable=True)
    shPoints = sa.Column(sa.Integer, nullable=True)
    shootingPct = sa.Column(sa.Float, nullable=True)
    shootsCatches = sa.Column(sa.Text, nullable=True)
    shots = sa.Column(sa.Integer, nullable=True)
    skaterFullName = sa.Column(sa.Text, nullable=True)
    teamAbbrevs = sa.Column(sa.Text, nullable=True)
    timeOnIcePerGame = sa.Column(sa.Integer, nullable=True)

    def __repr__(self):
        return "<Player {}: {}>".format(self.id, self.name)


class InternalPlayerStat(base):
    __tablename__ = 'internal_player_stat'

    id = sa.Column(sa.Integer, primary_key=True)
    playerId = sa.Column(sa.Integer, nullable=False)
    seasonId = sa.Column(sa.Integer, nullable=False)
    timeOnIce = sa.Column(sa.Integer, nullable=False),
    assists = sa.Column(sa.Integer, nullable=True)
    goals = sa.Column(sa.Integer, nullable=True)
    pim = sa.Column(sa.Integer, nullable=True)
    shots = sa.Column(sa.Integer, nullable=True)
    games = sa.Column(sa.Integer, nullable=True)
    hits = sa.Column(sa.Integer, nullable=True)
    powerPlayGoals = sa.Column(sa.Integer, nullable=True)
    powerPlayPoints = sa.Column(sa.Integer, nullable=True)
    powerPlayTimeOnIce = sa.Column(sa.Text, nullable=True)
    evenTimeOnIce = sa.Column(sa.Text, nullable=True)
    penaltyMinutes = sa.Column(sa.Text, nullable=True)
    faceOffPct = sa.Column(sa.Float, nullable=True)
    shotPct = sa.Column(sa.Float, nullable=True)
    gameWinningGoals = sa.Column(sa.Integer, nullable=True)
    overTimeGoals = sa.Column(sa.Integer, nullable=True)
    shortHandedGoals = sa.Column(sa.Integer, nullable=True)
    shortHandedPoints = sa.Column(sa.Integer, nullable=True)
    shortHandedTimeOnIce = sa.Column(sa.Integer, nullable=True)
    blocked = sa.Column(sa.Integer, nullable=True)
    plusMinus = sa.Column(sa.Integer, nullable=True)
    points = sa.Column(sa.Integer, nullable=True)
    shifts = sa.Column(sa.Integer, nullable=True)
    timeOnIcePerGame = sa.Column(sa.Text, nullable=True)
    evenTimeOnIcePerGame = sa.Column(sa.Text, nullable=True)
    shortHandedTimeOnIcePerGame = sa.Column(sa.Text, nullable=True)
    powerPlayTimeOnIcePerGame = sa.Column(sa.Text, nullable=True)

    _table_args__ = (
        sa.UniqueConstraint(playerId, seasonId),
    )


#
#
# class FantasyPlayer(base):
#     __tablename__ = 'fantasyplayer'
#
#     id = sa.Column(sa.Integer, primary_key=True)
#     name = sa.Column(sa.Text, nullable=True)
#     team_id = sa.Column(sa.Integer, sa.ForeignKey('team.id'), nullable=True)
#
#     def __repr__(self):
#         return "<Player {}: {}>".format(self.id, self.name)

base.metadata.create_all(engine)
