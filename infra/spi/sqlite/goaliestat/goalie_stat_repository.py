from dataclasses import fields
from typing import List, Optional

from application.goaliestats.model.goalie_stat import GoalieStat
from infra.spi.sqlite.goaliestat.model.goalie_stat_orm import GoalieStatORM
from infra.spi.sqlite.models import GoalieStatTable, Session

_TABLE_COLUMNS = {c.name for c in GoalieStatTable.__table__.columns}
_ORM_FIELDS = {f.name for f in fields(GoalieStatORM)}
_SHARED_FIELDS = _TABLE_COLUMNS & _ORM_FIELDS - {"id"}


class GoalieStatRepository:
    """SQLite repository for GoalieStat backed by internal_goalie_stat."""

    def _session(self):
        return Session()

    def find_all(self) -> List[GoalieStat]:
        session = self._session()
        try:
            rows = session.query(GoalieStatTable).all()
            return [self._to_application(row) for row in rows]
        finally:
            session.close()

    def find_all_by_season_id(self, season_id: int) -> List[GoalieStat]:
        session = self._session()
        try:
            rows = session.query(GoalieStatTable).filter_by(seasonId=season_id).all()
            return [self._to_application(row) for row in rows]
        finally:
            session.close()

    def find_by_player_id(self, player_id: int) -> Optional[GoalieStat]:
        session = self._session()
        try:
            row = (
                session.query(GoalieStatTable)
                .filter_by(playerId=player_id)
                .order_by(GoalieStatTable.seasonId.desc())
                .first()
            )
            return self._to_application(row)
        finally:
            session.close()

    def save(self, stat: GoalieStat) -> None:
        if stat is None or stat.playerId is None or stat.seasonId is None:
            return
        session = self._session()
        try:
            self._upsert(session, GoalieStatORM.from_application(stat))
            session.commit()
        finally:
            session.close()

    def _upsert(self, session, orm: GoalieStatORM) -> None:
        existing = session.query(GoalieStatTable).filter_by(
            playerId=orm.playerId,
            seasonId=orm.seasonId,
        ).first()

        values = {name: getattr(orm, name) for name in _SHARED_FIELDS}

        if existing:
            for name, value in values.items():
                setattr(existing, name, value)
        else:
            session.add(GoalieStatTable(**values))

    @staticmethod
    def _to_application(row) -> Optional[GoalieStat]:
        if row is None:
            return None
        orm = GoalieStatORM(**{name: getattr(row, name) for name in _SHARED_FIELDS})
        return orm.to_application()
