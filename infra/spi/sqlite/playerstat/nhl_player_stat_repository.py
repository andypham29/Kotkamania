from dataclasses import fields
from typing import List, Optional

from domain.nhlplayerstat.model.nhl_player_stat import PlayerStat
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
        return PlayerStat(**{name: getattr(row, name) for name in _SHARED_FIELDS})
