from dataclasses import dataclass

@dataclass
class DomainDraftboard:
    id: str
    favorites: list[str]
    watchlist: list[str]
    draftboard: list[str]