from dataclasses import dataclass, field
from typing import Any, Optional


def _as_str_list(value: Any) -> list[str]:
    if not value:
        return []
    return [str(item) for item in value]


@dataclass
class DomainDraftboard:
    id: Optional[str] = None
    favorites: list[str] = field(default_factory=list)
    watchlist: list[str] = field(default_factory=list)
    draftboard: list[str] = field(default_factory=list)
    drafted: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "favorites": self.favorites,
            "watchlist": self.watchlist,
            "draftboard": self.draftboard,
            "drafted": self.drafted,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "DomainDraftboard":
        return cls(
            id=data.get("id"),
            favorites=_as_str_list(data.get("favorites")),
            watchlist=_as_str_list(data.get("watchlist")),
            draftboard=_as_str_list(data.get("draftboard")),
            drafted=_as_str_list(data.get("drafted")),
        )