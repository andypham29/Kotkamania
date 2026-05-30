from dataclasses import dataclass
from typing import Optional


@dataclass
class RosterPlayerInfo:
    playerId: int
    fullName: str
    position: str
    jerseyNumber: Optional[int] = None
