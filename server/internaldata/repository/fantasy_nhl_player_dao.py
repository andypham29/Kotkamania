from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from server.commons.fantasybadge.model.fantasy_player_badge import FantasyPlayerBadge
from server.commons.helper.nhl_season_converter import NhlYearConverter
from server.commons.db.database import DatabaseManager
from server.internaldata.model.fantasy_nhl_player import FantasyNhlPlayer, DisplayStat
from server.internaldata.db.models import FantasyNhlPlayerORM, InternalPlayerStatORM


class FantasyNhlPlayerDao:

    def __init__(self, uri=None):
        self.uri = uri or 'server/internaldata/db/internal.db'
        self.year = NhlYearConverter.get_previous_season_by_year_removed(0)

    def _get_session(self) -> Session:
        """Get a new database session"""
        return DatabaseManager.get_session(self.uri)

    def initFantasySkaterTable(self):
        """Initialize fantasy_nhl_player table"""
        DatabaseManager.create_tables(
            __import__('server.internaldata.db.models', fromlist=['Base']).Base,
            self.uri
        )

    def saveFantasySkater(self, fantasy_skater):
        """Save or update fantasy skater"""
        session = self._get_session()
        try:
            orm_record = session.query(FantasyNhlPlayerORM).filter_by(
                playerId=fantasy_skater.playerId
            ).first()

            if orm_record:
                # Update existing record
                orm_record.skaterFullName = fantasy_skater.skaterFullName
                orm_record.positionCode = fantasy_skater.positionCode
                orm_record.teamId = fantasy_skater.teamId
                orm_record.teamName = fantasy_skater.teamName
                orm_record.fantasyGrade = fantasy_skater.fantasyGrade
                orm_record.yahooEligibility = fantasy_skater.yahooEligibility
                orm_record.avgPick = fantasy_skater.avgPick
                orm_record.avgRound = fantasy_skater.avgRound
                orm_record.percentDrafted = fantasy_skater.percentDrafted
                orm_record.nhlRank = fantasy_skater.nhlRank
            else:
                # Create new record
                orm_record = FantasyNhlPlayerORM(
                    playerId=fantasy_skater.playerId,
                    skaterFullName=fantasy_skater.skaterFullName,
                    positionCode=fantasy_skater.positionCode,
                    teamId=fantasy_skater.teamId,
                    teamName=fantasy_skater.teamName,
                    fantasyGrade=fantasy_skater.fantasyGrade,
                    yahooEligibility=fantasy_skater.yahooEligibility,
                    avgPick=fantasy_skater.avgPick,
                    avgRound=fantasy_skater.avgRound,
                    percentDrafted=fantasy_skater.percentDrafted,
                    nhlRank=fantasy_skater.nhlRank
                )
                session.add(orm_record)

            session.commit()
        finally:
            session.close()


    def getFantasySkaterById(self, playerId):
        """Get fantasy skater by player ID"""
        session = self._get_session()
        try:
            row = session.query(FantasyNhlPlayerORM).filter_by(
                playerId=playerId
            ).first()
            return self.__convert_to_model(row) if row else None
        finally:
            session.close()

    def getAllFantasySkatersWithStat(self):
        """Get all fantasy skaters with their stats"""
        session = self._get_session()
        try:
            from sqlalchemy import func

            rows = session.query(FantasyNhlPlayerORM).outerjoin(
                InternalPlayerStatORM,
                and_(
                    FantasyNhlPlayerORM.playerId == InternalPlayerStatORM.playerId,
                    InternalPlayerStatORM.seasonId == self.year
                )
            ).all()

            result = []
            for row in rows:
                # Get associated stat if it exists
                stat_row = session.query(InternalPlayerStatORM).filter(
                    InternalPlayerStatORM.playerId == row.playerId,
                    InternalPlayerStatORM.seasonId == self.year
                ).first()

                fantasy_skater = self.__convert_to_model_with_display_stat(row, stat_row)
                result.append(fantasy_skater)

            return result
        finally:
            session.close()

    def getAllFantasySkatersByPositionCodesWithStats(self, positionCodes, offset):
        """Get fantasy skaters by position codes with stats"""
        session = self._get_session()
        try:
            # Filter position codes
            valid_positions = [p for p in positionCodes if p in ['L', 'C', 'R', 'D', 'G']]

            query = session.query(FantasyNhlPlayerORM).outerjoin(
                InternalPlayerStatORM,
                and_(
                    FantasyNhlPlayerORM.playerId == InternalPlayerStatORM.playerId,
                    InternalPlayerStatORM.seasonId == self.year
                )
            )

            # Filter by position code or yahoo eligibility
            query = query.filter(
                or_(
                    FantasyNhlPlayerORM.positionCode.in_(valid_positions),
                    *[FantasyNhlPlayerORM.yahooEligibility.like(f'%{pos}%') for pos in valid_positions]
                )
            )

            if offset is not None:
                query = query.offset(125 * offset).limit(125)

            rows = query.all()

            result = []
            for row in rows:
                stat_row = session.query(InternalPlayerStatORM).filter(
                    InternalPlayerStatORM.playerId == row.playerId,
                    InternalPlayerStatORM.seasonId == self.year
                ).first()
                fantasy_skater = self.__convert_to_model_with_display_stat(row, stat_row)
                result.append(fantasy_skater)

            return result
        finally:
            session.close()


    def getAllFantasySkatersByPositionCodes(self, positionCodes, offset):
        """Get fantasy skaters by position codes"""
        session = self._get_session()
        try:
            valid_positions = [p for p in positionCodes if p in ['L', 'C', 'R', 'D', 'G']]

            query = session.query(FantasyNhlPlayerORM).filter(
                or_(
                    FantasyNhlPlayerORM.positionCode.in_(valid_positions),
                    *[FantasyNhlPlayerORM.yahooEligibility.like(f'%{pos}%') for pos in valid_positions]
                )
            )

            rows = query.all()
            return [self.__convert_to_model(row) for row in rows]
        finally:
            session.close()

    def getAllFantasySkaters(self):
        """Get all fantasy skaters with grade > 30"""
        session = self._get_session()
        try:
            rows = session.query(FantasyNhlPlayerORM).filter(
                FantasyNhlPlayerORM.fantasyGrade > 30
            ).all()
            return [self.__convert_to_model(row) for row in rows]
        finally:
            session.close()

    def getAllFantasySkatersInPlayerIdList(self, playerIdList):
        """Get fantasy skaters in player ID list"""
        session = self._get_session()
        try:
            rows = session.query(FantasyNhlPlayerORM).filter(
                FantasyNhlPlayerORM.playerId.in_(playerIdList)
            ).all()
            return [self.__convert_to_model(row) for row in rows]
        finally:
            session.close()

    def getAllFantasySkatersByTeamId(self, teamId):
        """Get all fantasy skaters by team ID"""
        session = self._get_session()
        try:
            rows = session.query(FantasyNhlPlayerORM).filter_by(
                teamId=teamId
            ).all()
            return [self.__convert_to_model(row) for row in rows]
        finally:
            session.close()

    def getAllFantasySkatersBySearchName(self, name):
        """Search fantasy skaters by name"""
        session = self._get_session()
        try:
            rows = session.query(FantasyNhlPlayerORM).filter(
                FantasyNhlPlayerORM.skaterFullName.like(f'%{name}%')
            ).all()
            return [self.__convert_to_model(row) for row in rows]
        finally:
            session.close()

    def deleteFantasySkaterById(self, playerId):
        """Delete fantasy skater by ID"""
        session = self._get_session()
        try:
            session.query(FantasyNhlPlayerORM).filter_by(
                playerId=playerId
            ).delete()
            session.commit()
        finally:
            session.close()

    def updateFantasyGradeForFantasySkaterWithId(self, playerId, grade):
        """Update fantasy grade for a skater"""
        session = self._get_session()
        try:
            session.query(FantasyNhlPlayerORM).filter_by(
                playerId=playerId
            ).update({'fantasyGrade': grade})
            session.commit()
        finally:
            session.close()

    def bulkUpdateFantasyGradeForFantasySkaterWithId(self, players):
        """Bulk update fantasy grades"""
        session = self._get_session()
        try:
            for player in players:
                session.query(FantasyNhlPlayerORM).filter_by(
                    playerId=player.id
                ).update({'fantasyGrade': player.score})
            session.commit()
        finally:
            session.close()

    def updateNhlRankForFantasySkaterWithName(self, playerName, nhlRank):
        """Update NHL rank by player name"""
        print(playerName, ": ", nhlRank)
        session = self._get_session()
        try:
            session.query(FantasyNhlPlayerORM).filter_by(
                skaterFullName=playerName
            ).update({'nhlRank': nhlRank})
            session.commit()
        finally:
            session.close()

    def updateYahooRankForFantasySkaterWithName(self, playerName, nhlRank):
        """Update Yahoo rank by player name"""
        print(playerName, ": ", nhlRank)
        session = self._get_session()
        try:
            session.query(FantasyNhlPlayerORM).filter_by(
                skaterFullName=playerName
            ).update({'avgPick': nhlRank})
            session.commit()
        finally:
            session.close()

    def updateFantasyYahooInfoForFantasySkater(self, yahoo_info):
        """Update Yahoo info for a skater"""
        session = self._get_session()
        try:
            session.query(FantasyNhlPlayerORM).filter_by(
                skaterFullName=yahoo_info[0]
            ).update({
                'yahooEligibility': yahoo_info[1],
                'avgPick': yahoo_info[2],
                'avgRound': yahoo_info[3],
                'percentDrafted': yahoo_info[4]
            })
            session.commit()
        finally:
            session.close()

    def updateFantasyBadgeForFantasySkaterByPlayerId(self, fantasy_badge, playerId):
        """Update fantasy badge for a skater"""
        session = self._get_session()
        try:
            session.query(FantasyNhlPlayerORM).filter_by(
                playerId=playerId
            ).update({
                'scoring': fantasy_badge.scoring,
                'playmaking': fantasy_badge.playmaking,
                'defense': fantasy_badge.defense,
                'powerplay': fantasy_badge.powerplay,
                'intangibles': fantasy_badge.intangibles
            })
            session.commit()
        finally:
            session.close()

    def removeTeamIdFromAllFantasySkates(self):
        """Remove team ID from all fantasy skaters"""
        session = self._get_session()
        try:
            session.query(FantasyNhlPlayerORM).update({'teamId': 0})
            session.commit()
        finally:
            session.close()

    def deleteAllFantasySkatersWithNoTeam(self):
        """Delete all fantasy skaters with no team"""
        session = self._get_session()
        try:
            session.query(FantasyNhlPlayerORM).filter_by(
                teamId=0
            ).delete()
            session.commit()
        finally:
            session.close()

    @staticmethod
    def __convert_to_model(orm_row):
        """Convert ORM object to domain model"""
        if orm_row is None:
            return None
        return FantasyNhlPlayer(
            id=orm_row.playerId,
            skaterFullName=orm_row.skaterFullName,
            positionCode=orm_row.positionCode,
            teamId=orm_row.teamId,
            fantasyGrade=orm_row.fantasyGrade,
            yahooEligibility=orm_row.yahooEligibility,
            avgPick=orm_row.avgPick,
            avgRound=orm_row.avgRound,
            percentDrafted=orm_row.percentDrafted,
            teamName=orm_row.teamName,
            nhlRank=orm_row.nhlRank,
            badge=FantasyPlayerBadge(
                orm_row.scoring or 0,
                orm_row.playmaking or 0,
                orm_row.defense or 0,
                orm_row.powerplay or 0,
                orm_row.intangibles or 0
            )
        )

    @staticmethod
    def __convert_to_model_with_display_stat(orm_row, stat_row):
        """Convert ORM objects to domain model with display stats"""
        if orm_row is None:
            return None

        display_stat = None
        if stat_row:
            display_stat = DisplayStat(
                assists=stat_row.assists or 0,
                goals=stat_row.goals or 0,
                points=stat_row.points or 0,
                games=stat_row.games or 0,
                shots=stat_row.shots or 0,
                hits=stat_row.hits or 0,
                blocked=stat_row.blocked or 0,
                plusMinus=stat_row.plusMinus or 0,
                powerPlayGoals=stat_row.powerPlayGoals or 0,
                powerPlayPoints=stat_row.powerPlayPoints or 0
            )

        return FantasyNhlPlayer(
            id=orm_row.playerId,
            skaterFullName=orm_row.skaterFullName,
            positionCode=orm_row.positionCode,
            teamId=orm_row.teamId,
            fantasyGrade=orm_row.fantasyGrade,
            yahooEligibility=orm_row.yahooEligibility,
            avgPick=orm_row.avgPick,
            avgRound=orm_row.avgRound,
            percentDrafted=orm_row.percentDrafted,
            teamName=orm_row.teamName,
            nhlRank=orm_row.nhlRank,
            badge=FantasyPlayerBadge(
                orm_row.scoring or 0,
                orm_row.playmaking or 0,
                orm_row.defense or 0,
                orm_row.powerplay or 0,
                orm_row.intangibles or 0
            ),
            stat=display_stat or DisplayStat()
        )
