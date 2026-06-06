from typing import Optional

from domain.draftboard.model.domain_draftboard import DomainDraftboard
from infra.spi.sqlite.models import DomainDraftboardORM, Session as DBSession

_DOMAIN_FIELDS = ('id', 'favorites', 'watchlist', 'draftboard', 'drafted')


class DraftboardRepository:
    """SQLite repository for DomainDraftboard using the shared internal.db schema."""

    def _session(self):
        return DBSession()

    def find_by_id(self, draftboard_id: str) -> Optional[DomainDraftboard]:
        session = self._session()
        try:
            row = session.query(DomainDraftboardORM).filter_by(id=draftboard_id).first()
            return self._to_domain(row)
        finally:
            session.close()

    def save(self, draftboard: DomainDraftboard) -> None:
        if draftboard is None or not draftboard.id:
            return
        session = self._session()
        try:
            self._upsert(session, draftboard)
            session.commit()
        finally:
            session.close()

    def delete_all(self) -> int:
        session = self._session()
        try:
            deleted = session.query(DomainDraftboardORM).delete()
            session.commit()
            return deleted
        finally:
            session.close()

    def _upsert(self, session, draftboard: DomainDraftboard) -> None:
        existing = session.query(DomainDraftboardORM).filter_by(id=draftboard.id).first()
        values = {name: getattr(draftboard, name) for name in _DOMAIN_FIELDS}

        if existing:
            for name, value in values.items():
                if name != 'id':
                    setattr(existing, name, value)
        else:
            session.add(DomainDraftboardORM(**values))

    @staticmethod
    def _to_domain(row) -> Optional[DomainDraftboard]:
        if row is None:
            return None
        return DomainDraftboard(**{name: getattr(row, name) for name in _DOMAIN_FIELDS})
