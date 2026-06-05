from sqlalchemy.orm import Session

from server.commons.helper.time_converter import TimeConverter
from infra.spi.sqlite.models import InternalPlayerStatORM, Session as DBSession
from server.internaldata.model.internal_nhl_player_stat import InternalPlayerStat


class InternalPlayerStatDao:
    def __init__(self, uri=None):
        # Note: uri parameter is kept for backward compatibility but not used
        # The centralized database setup is used instead
        pass

    def _get_session(self) -> Session:
        """Get a new database session"""
        return DBSession()

    def get_internal_all_players_stats_by_seasonId(self, seasonId):
        """Get all player stats for a season"""
        session = self._get_session()
        try:
            rows = session.query(InternalPlayerStatORM).filter_by(
                seasonId=seasonId
            ).all()
            return [self.__row_to_object(row) for row in rows]
        finally:
            session.close()

    def get_internal_players_stats_by_playerId_and_seasonId(self, playerId, seasonId):
        """Get player stats by player ID and season"""
        session = self._get_session()
        try:
            row = session.query(InternalPlayerStatORM).filter_by(
                playerId=playerId,
                seasonId=seasonId
            ).first()
            return self.__row_to_object(row) if row else None
        finally:
            session.close()

    def get_internal_players_stats_at_percentile_values_and_seasonId(self, percentile_values, seasonId):
        """Get player stats filtered by percentile values"""
        session = self._get_session()
        try:
            query = session.query(InternalPlayerStatORM).filter_by(seasonId=seasonId)

            for attr, value in percentile_values.__dict__.items():
                if value.percentile is None:
                    continue

                if attr in ['timeOnIcePerGame', 'powerPlayTimeOnIcePerGame', 'evenTimeOnIcePerGame']:
                    print(f"{attr} > {TimeConverter.convert_total_seconds_to_string(value.value)}")
                    # For time-based comparisons, we'd need custom logic
                    continue
                else:
                    # Filter by calculated stat (value per game)
                    col = getattr(InternalPlayerStatORM, attr)
                    if col is not None:
                        query = query.filter(col > value.value)

            records = query.all()
            result = [self.__row_to_object(row) for row in records]
            print(f"[Percentile Filter] fetched number of rows: {len(result)}")
            return result
        finally:
            session.close()

    def insert_internal_players_stats(self, playerId, seasonId, stat):
        """Insert or update player stats"""
        session = self._get_session()
        try:
            existing = session.query(InternalPlayerStatORM).filter_by(
                playerId=playerId,
                seasonId=seasonId
            ).first()

            if existing:
                # Update existing record
                existing.timeOnIce = stat.timeOnIce
                existing.assists = stat.assists
                existing.goals = stat.goals
                existing.pim = stat.pim
                existing.shots = stat.shots
                existing.games = stat.games
                existing.hits = stat.hits
                existing.powerPlayGoals = stat.powerPlayGoals
                existing.powerPlayPoints = stat.powerPlayPoints
                existing.powerPlayTimeOnIce = stat.powerPlayTimeOnIce
                existing.evenTimeOnIce = stat.evenTimeOnIce
                existing.penaltyMinutes = stat.penaltyMinutes
                existing.faceOffPct = stat.faceOffPct
                existing.shotPct = stat.shotPct
                existing.gameWinningGoals = stat.gameWinningGoals
                existing.overTimeGoals = stat.overTimeGoals
                existing.shortHandedGoals = stat.shortHandedGoals
                existing.shortHandedPoints = stat.shortHandedPoints
                existing.shortHandedTimeOnIce = stat.shortHandedTimeOnIce
                existing.blocked = stat.blocked
                existing.plusMinus = stat.plusMinus
                existing.points = stat.points
                existing.shifts = stat.shifts
                existing.timeOnIcePerGame = stat.timeOnIcePerGame
                existing.evenTimeOnIcePerGame = stat.evenTimeOnIcePerGame
                existing.shortHandedTimeOnIcePerGame = stat.shortHandedTimeOnIcePerGame
                existing.powerPlayTimeOnIcePerGame = stat.powerPlayTimeOnIcePerGame
            else:
                # Create new record
                new_record = InternalPlayerStatORM(
                    playerId=playerId,
                    seasonId=seasonId,
                    timeOnIce=stat.timeOnIce,
                    assists=stat.assists,
                    goals=stat.goals,
                    pim=stat.pim,
                    shots=stat.shots,
                    games=stat.games,
                    hits=stat.hits,
                    powerPlayGoals=stat.powerPlayGoals,
                    powerPlayPoints=stat.powerPlayPoints,
                    powerPlayTimeOnIce=stat.powerPlayTimeOnIce,
                    evenTimeOnIce=stat.evenTimeOnIce,
                    penaltyMinutes=stat.penaltyMinutes,
                    faceOffPct=stat.faceOffPct,
                    shotPct=stat.shotPct,
                    gameWinningGoals=stat.gameWinningGoals,
                    overTimeGoals=stat.overTimeGoals,
                    shortHandedGoals=stat.shortHandedGoals,
                    shortHandedPoints=stat.shortHandedPoints,
                    shortHandedTimeOnIce=stat.shortHandedTimeOnIce,
                    blocked=stat.blocked,
                    plusMinus=stat.plusMinus,
                    points=stat.points,
                    shifts=stat.shifts,
                    timeOnIcePerGame=stat.timeOnIcePerGame,
                    evenTimeOnIcePerGame=stat.evenTimeOnIcePerGame,
                    shortHandedTimeOnIcePerGame=stat.shortHandedTimeOnIcePerGame,
                    powerPlayTimeOnIcePerGame=stat.powerPlayTimeOnIcePerGame
                )
                session.add(new_record)

            session.commit()
        finally:
            session.close()

    @staticmethod
    def __row_to_object(orm_row):
        """Convert ORM object to domain model"""
        if orm_row is None:
            return None
        return InternalPlayerStat(
            playerId=orm_row.playerId,
            seasonId=orm_row.seasonId,
            timeOnIce=None,
            assists=orm_row.assists,
            goals=orm_row.goals,
            pim=orm_row.pim,
            shots=orm_row.shots,
            games=orm_row.games,
            hits=orm_row.hits,
            powerPlayGoals=orm_row.powerPlayGoals,
            powerPlayPoints=orm_row.powerPlayPoints,
            powerPlayTimeOnIce=orm_row.powerPlayTimeOnIce,
            evenTimeOnIce=orm_row.evenTimeOnIce,
            penaltyMinutes=orm_row.penaltyMinutes,
            faceOffPct=orm_row.faceOffPct,
            shotPct=orm_row.shotPct,
            gameWinningGoals=orm_row.gameWinningGoals,
            overTimeGoals=orm_row.overTimeGoals,
            shortHandedGoals=orm_row.shortHandedGoals,
            shortHandedPoints=orm_row.shortHandedPoints,
            shortHandedTimeOnIce=orm_row.shortHandedTimeOnIce,
            blocked=orm_row.blocked,
            plusMinus=orm_row.plusMinus,
            points=orm_row.points,
            shifts=orm_row.shifts,
            timeOnIcePerGame=orm_row.timeOnIcePerGame,
            evenTimeOnIcePerGame=orm_row.evenTimeOnIcePerGame,
            shortHandedTimeOnIcePerGame=orm_row.shortHandedTimeOnIcePerGame,
            powerPlayTimeOnIcePerGame=orm_row.powerPlayTimeOnIcePerGame
        )
