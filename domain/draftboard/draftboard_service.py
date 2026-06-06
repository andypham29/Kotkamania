from typing import Optional

from domain.draftboard.model.domain_draftboard import DomainDraftboard
from infra.spi.sqlite.draftboard.draftboard_repository import DraftboardRepository


class DraftboardService:
    """Persists and retrieves draftboard state through the SQLite repository."""

    def __init__(self):
        self.repository = DraftboardRepository()

    def save(self, draftboard: DomainDraftboard) -> DomainDraftboard:
        if not draftboard.id:
            draftboard.id = generate_id()
        self.repository.save(draftboard)
        return draftboard

    def get_by_id(self, draftboard_id: str) -> Optional[DomainDraftboard]:
        return self.repository.find_by_id(draftboard_id)

    def delete_all(self) -> int:
        return self.repository.delete_all()

import secrets

def generate_id() -> str:
    return secrets.token_urlsafe(6)[:8]   # ~48 bits of entropy
