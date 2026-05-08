from sqlalchemy.orm import Session

from server.commons.db.database import DatabaseManager
from server.internaldata.model.fantasy_player_streak_index import FantasyPlayerStreakIndex
from server.internaldata.db.models import FantasyPlayerStreakIndexORM


class FantasyPlayerStreakIndexDao:

    def __init__(self, uri=None):
        self.uri = uri or 'server/internaldata/db/fantasy.db'

    def _get_session(self) -> Session:
        """Get a new database session"""
        return DatabaseManager.get_session(self.uri)

    def initFantasyPlayerStreakIndexTable(self):
        """Initialize fantasy streak index table"""
        DatabaseManager.create_tables(
            __import__('server.internaldata.db.models', fromlist=['Base']).Base,
            self.uri
        )

    def saveOrUpdateFantasyPlayerStreakIndex(self, fantasy_streak_info):
        """Save or update fantasy player streak index"""
        session = self._get_session()
        try:
            existing = session.query(FantasyPlayerStreakIndexORM).filter_by(
                playerId=fantasy_streak_info.playerId
            ).first()

            if existing:
                existing.skaterFullName = fantasy_streak_info.skaterFullName
                existing.positionCode = fantasy_streak_info.positionCode
                existing.pts = fantasy_streak_info.pts
                existing.toi = fantasy_streak_info.toi
                existing.pptoi = fantasy_streak_info.pptoi
                existing.streakIndex = fantasy_streak_info.index
                existing.lastUpdated = fantasy_streak_info.lastUpdated
            else:
                new_record = FantasyPlayerStreakIndexORM(
                    playerId=fantasy_streak_info.playerId,
                    skaterFullName=fantasy_streak_info.skaterFullName,
                    positionCode=fantasy_streak_info.positionCode,
                    pts=fantasy_streak_info.pts,
                    toi=fantasy_streak_info.toi,
                    pptoi=fantasy_streak_info.pptoi,
                    streakIndex=fantasy_streak_info.index,
                    lastUpdated=fantasy_streak_info.lastUpdated
                )
                session.add(new_record)

            session.commit()
        finally:
            session.close()

    def getFantasyPlayerStreakIndex(self, playerId):
        """Get fantasy player streak index by player ID"""
        session = self._get_session()
        try:
            row = session.query(FantasyPlayerStreakIndexORM).filter_by(
                playerId=playerId
            ).first()
            return self.__row_to_object(row) if row else None
        finally:
            session.close()

    def getAllFantasyPlayerStreakIndexes(self):
        """Get all fantasy player streak indexes ordered by streak index"""
        session = self._get_session()
        try:
            records = session.query(FantasyPlayerStreakIndexORM).order_by(
                FantasyPlayerStreakIndexORM.streakIndex.desc()
            ).all()
            return [self.__row_to_object(row) for row in records]
        finally:
            session.close()

    def getAllFantasyPlayerStreakIndexesByPositionCodes(self, positionCodes):
        """Get fantasy player streak indexes by position codes"""
        session = self._get_session()
        try:
            valid_positions = [p for p in positionCodes if p in ['L', 'C', 'R', 'D']]

            records = session.query(FantasyPlayerStreakIndexORM).filter(
                FantasyPlayerStreakIndexORM.positionCode.in_(valid_positions)
            ).order_by(FantasyPlayerStreakIndexORM.streakIndex.desc()).all()

            return [self.__row_to_object(row) for row in records]
        finally:
            session.close()

    def getAllFantasyPlayerStreakIndexInPlayerIdList(self, playerIdList):
        """Get fantasy player streak index for players in list"""
        session = self._get_session()
        try:
            records = session.query(FantasyPlayerStreakIndexORM).filter(
                FantasyPlayerStreakIndexORM.playerId.in_(playerIdList)
            ).all()
            return [self.__row_to_object(row) for row in records]
        finally:
            session.close()

    def getAllFantasySkatersBySearchName(self, name):
        """Search fantasy skaters by name"""
        session = self._get_session()
        try:
            records = session.query(FantasyPlayerStreakIndexORM).filter(
                FantasyPlayerStreakIndexORM.skaterFullName.like(f'%{name}%')
            ).all()
            return [self.__row_to_object(row) for row in records]
        finally:
            session.close()

    def deleteFantasySkaterById(self, playerId):
        """Delete fantasy skater by ID"""
        session = self._get_session()
        try:
            session.query(FantasyPlayerStreakIndexORM).filter_by(
                playerId=playerId
            ).delete()
            session.commit()
        finally:
            session.close()

    def deleteAllFantasySkaterStreak(self):
        """Delete all fantasy skater streaks"""
        session = self._get_session()
        try:
            session.query(FantasyPlayerStreakIndexORM).delete()
            session.commit()
        finally:
            session.close()

    @staticmethod
    def __row_to_object(orm_row):
        """Convert ORM object to domain model"""
        if orm_row is None:
            return None
        return FantasyPlayerStreakIndex(
            id=orm_row.playerId,
            skaterFullName=orm_row.skaterFullName,
            positionCode=orm_row.positionCode,
            pts=orm_row.pts,
            toi=orm_row.toi,
            pptoi=orm_row.pptoi,
            index=orm_row.streakIndex,
            lastUpdated=orm_row.lastUpdated
        )
