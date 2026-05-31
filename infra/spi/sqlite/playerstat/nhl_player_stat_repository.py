from dataclasses import fields
from typing import List, Optional

from sqlalchemy import func, Integer, cast, Float

from domain.playerstat.model.nhl_player_stat import PlayerStat
from server.internaldata.db.models import InternalPlayerStatORM, Session as DBSession

# ORM columns that exist on `internal_player_stat` and overlap with PlayerStat.
# We pre-compute the intersection so we can copy fields generically.
_ORM_COLUMNS = {c.name for c in InternalPlayerStatORM.__table__.columns}
_STAT_FIELDS = {f.name for f in fields(PlayerStat)}
_SHARED_FIELDS = _ORM_COLUMNS & _STAT_FIELDS


class NhlPlayerStatRepository:
    """SQLite repository for PlayerStat using the shared `internal.db` schema."""

    def _session(self):
        return DBSession()

    # ---- reads ----
    def find_all(self, season_id: int) -> list[PlayerStat | None]:
        session = self._session()
        try:
            rows = session.query(InternalPlayerStatORM).filter_by(seasonId=season_id).all()
            return [self._to_domain(row) for row in rows]
        finally:
            session.close()

    def find_by_player_id(self, player_id: int, season_id: int) -> Optional[PlayerStat]:
        session = self._session()
        try:
            row = session.query(InternalPlayerStatORM).filter_by(
                playerId=player_id,
                seasonId=season_id,
            ).first()
            return self._to_domain(row)
        finally:
            session.close()

    # ---- writes ----
    def save(self, stat: PlayerStat) -> None:
        if stat is None or stat.playerId is None or stat.seasonId is None:
            return
        session = self._session()
        try:
            self._upsert(session, stat)
            session.commit()
        finally:
            session.close()

    def save_all(self, stats: List[PlayerStat]) -> int:
        if not stats:
            return 0
        session = self._session()
        try:
            written = 0
            for stat in stats:
                if stat is None or stat.playerId is None or stat.seasonId is None:
                    continue
                self._upsert(session, stat)
                written += 1
            session.commit()
            return written
        finally:
            session.close()

    def find_max_stat(self, season_id):
        session = self._session()
        try:
            row = session.query(
                func.max(cast(InternalPlayerStatORM.timeOnIce, Float)).label("timeOnIce"),
                func.max(InternalPlayerStatORM.assists).label("assists"),
                func.max(InternalPlayerStatORM.goals).label("goals"),
                func.max(InternalPlayerStatORM.pim).label("pim"),
                func.max(InternalPlayerStatORM.shots).label("shots"),
                func.max(InternalPlayerStatORM.games).label("games"),
                func.max(InternalPlayerStatORM.hits).label("hits"),
                func.max(InternalPlayerStatORM.powerPlayGoals).label("powerPlayGoals"),
                func.max(InternalPlayerStatORM.powerPlayPoints).label("powerPlayPoints"),
                func.max(cast(InternalPlayerStatORM.powerPlayTimeOnIce, Float)).label("powerPlayTimeOnIce"),
                func.max(cast(InternalPlayerStatORM.evenTimeOnIce, Float)).label("evenTimeOnIce"),
                func.max(InternalPlayerStatORM.penaltyMinutes).label("penaltyMinutes"),
                func.max(InternalPlayerStatORM.faceOffPct).label("faceOffPct"),
                func.max(InternalPlayerStatORM.shotPct).label("shotPct"),
                func.max(InternalPlayerStatORM.gameWinningGoals).label("gameWinningGoals"),
                func.max(InternalPlayerStatORM.overTimeGoals).label("overTimeGoals"),
                func.max(InternalPlayerStatORM.shortHandedGoals).label("shortHandedGoals"),
                func.max(InternalPlayerStatORM.shortHandedPoints).label("shortHandedPoints"),
                func.max(cast(InternalPlayerStatORM.shortHandedTimeOnIce, Float)).label("shortHandedTimeOnIce"),
                func.max(InternalPlayerStatORM.blocked).label("blocked"),
                func.max(InternalPlayerStatORM.plusMinus).label("plusMinus"),
                func.max(InternalPlayerStatORM.points).label("points"),
                func.max(InternalPlayerStatORM.shifts).label("shifts"),
                func.max(cast(InternalPlayerStatORM.timeOnIcePerGame, Float)).label("timeOnIcePerGame"),
                func.max(cast(InternalPlayerStatORM.evenTimeOnIcePerGame, Float)).label("evenTimeOnIcePerGame"),
                func.max(cast(InternalPlayerStatORM.shortHandedTimeOnIcePerGame, Float)).label("shortHandedTimeOnIcePerGame"),
                func.max(cast(InternalPlayerStatORM.powerPlayTimeOnIcePerGame, Float)).label("powerPlayTimeOnIcePerGame"),
            ).filter(InternalPlayerStatORM.seasonId == season_id).one()
            return self._to_domain(row)
        finally:
            session.close()

    def find_min_stat(self, season_id):
        session = self._session()
        try:
            row = session.query(
                func.min(cast(InternalPlayerStatORM.timeOnIce, Float)).label("timeOnIce"),
                func.min(InternalPlayerStatORM.assists).label("assists"),
                func.min(InternalPlayerStatORM.goals).label("goals"),
                func.min(InternalPlayerStatORM.pim).label("pim"),
                func.min(InternalPlayerStatORM.shots).label("shots"),
                func.min(InternalPlayerStatORM.games).label("games"),
                func.min(InternalPlayerStatORM.hits).label("hits"),
                func.min(InternalPlayerStatORM.powerPlayGoals).label("powerPlayGoals"),
                func.min(InternalPlayerStatORM.powerPlayPoints).label("powerPlayPoints"),
                func.min(cast(InternalPlayerStatORM.powerPlayTimeOnIce, Float)).label("powerPlayTimeOnIce"),
                func.min(cast(InternalPlayerStatORM.evenTimeOnIce, Float)).label("evenTimeOnIce"),
                func.min(cast(InternalPlayerStatORM.penaltyMinutes, Float)).label("penaltyMinutes"),
                func.min(InternalPlayerStatORM.faceOffPct).label("faceOffPct"),
                func.min(InternalPlayerStatORM.shotPct).label("shotPct"),
                func.min(InternalPlayerStatORM.gameWinningGoals).label("gameWinningGoals"),
                func.min(InternalPlayerStatORM.overTimeGoals).label("overTimeGoals"),
                func.min(InternalPlayerStatORM.shortHandedGoals).label("shortHandedGoals"),
                func.min(InternalPlayerStatORM.shortHandedPoints).label("shortHandedPoints"),
                func.min(cast(InternalPlayerStatORM.shortHandedTimeOnIce, Float)).label("shortHandedTimeOnIce"),
                func.min(InternalPlayerStatORM.blocked).label("blocked"),
                func.min(InternalPlayerStatORM.plusMinus).label("plusMinus"),
                func.min(InternalPlayerStatORM.points).label("points"),
                func.min(InternalPlayerStatORM.shifts).label("shifts"),
                func.min(cast(InternalPlayerStatORM.timeOnIcePerGame, Float)).label("timeOnIcePerGame"),
                func.min(cast(InternalPlayerStatORM.evenTimeOnIcePerGame, Float)).label("evenTimeOnIcePerGame"),
                func.min(cast(InternalPlayerStatORM.shortHandedTimeOnIcePerGame, Float)).label("shortHandedTimeOnIcePerGame"),
                func.min(cast(InternalPlayerStatORM.powerPlayTimeOnIcePerGame, Float)).label("powerPlayTimeOnIcePerGame"),
            ).filter(InternalPlayerStatORM.seasonId == season_id).one()
            return self._to_domain(row)
        finally:
            session.close()

    # ---- helpers ----
    def _upsert(self, session, stat: PlayerStat) -> None:
        existing = session.query(InternalPlayerStatORM).filter_by(
            playerId=stat.playerId,
            seasonId=stat.seasonId,
        ).first()

        values = {name: getattr(stat, name) for name in _SHARED_FIELDS}

        if existing:
            for name, value in values.items():
                setattr(existing, name, value)
        else:
            session.add(InternalPlayerStatORM(**values))

    @staticmethod
    def _to_domain(row) -> Optional[PlayerStat]:
        if row is None:
            return None
        SKIP_FIELDS = {"id", "playerId", "seasonId"}

        return PlayerStat(**{
            name: getattr(row, name)
            for name in _SHARED_FIELDS
            if name not in SKIP_FIELDS
        })
