from dataclasses import fields
from typing import List, Optional

from infra.spi.sqlite.playerstatpercentile.model.nhl_player_stat_percentile import PlayerStatPercentile
from infra.spi.sqlite.models import InternalPlayerStatPercentileORM, Session as DBSession

# ORM columns that exist on `internal_player_stat_percentile` and overlap with PlayerStatPercentile.
# We pre-compute the intersection so we can copy fields generically.
_ORM_COLUMNS = {c.name for c in InternalPlayerStatPercentileORM.__table__.columns}
_STAT_FIELDS = {f.name for f in fields(PlayerStatPercentile)}
_SHARED_FIELDS = _ORM_COLUMNS & _STAT_FIELDS


class NhlPlayerStatPercentileRepository:
    """SQLite repository for PlayerStatPercentile using the shared `internal.db` schema."""

    def _session(self):
        return DBSession()

    # ---- reads ----
    def find_all(self, season_id: int) -> list[PlayerStatPercentile | None]:
        session = self._session()
        try:
            rows = session.query(InternalPlayerStatPercentileORM).filter_by(seasonId=season_id).all()
            return [self._to_domain(row) for row in rows]
        finally:
            session.close()

    def find_by_player_id(self, player_id: int, season_id: int) -> Optional[PlayerStatPercentile]:
        session = self._session()
        try:
            row = session.query(InternalPlayerStatPercentileORM).filter_by(
                playerId=player_id,
                seasonId=season_id,
            ).first()
            return self._to_domain(row)
        finally:
            session.close()

    # ---- writes ----
    def save(self, stat: PlayerStatPercentile) -> None:
        if stat is None or stat.playerId is None or stat.seasonId is None:
            return
        session = self._session()
        try:
            self._upsert(session, stat)
            session.commit()
        finally:
            session.close()

    def save_all(self, stats: List[PlayerStatPercentile]) -> int:
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
    def _upsert(self, session, stat: PlayerStatPercentile) -> None:
        existing = session.query(InternalPlayerStatPercentileORM).filter_by(
            playerId=stat.playerId,
            seasonId=stat.seasonId,
        ).first()

        values = {name: getattr(stat, name) for name in _SHARED_FIELDS}

        if existing:
            for name, value in values.items():
                setattr(existing, name, value)
        else:
            session.add(InternalPlayerStatPercentileORM(**values))

    @staticmethod
    def _to_domain(row) -> Optional[PlayerStatPercentile]:
        if row is None:
            return None
        SKIP_FIELDS = {"id", "playerId", "seasonId"}

        return PlayerStatPercentile(**{
            name: getattr(row, name)
            for name in _SHARED_FIELDS
            if name not in SKIP_FIELDS
        })
