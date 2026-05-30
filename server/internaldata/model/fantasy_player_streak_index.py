from dataclasses import dataclass
from typing import Optional


@dataclass
class FantasyPlayerStreakIndex:
    id: str = ""
    skaterFullName: str = ""
    positionCode: str = ""
    pts: Optional[float] = None
    toi: Optional[float] = None
    pptoi: Optional[float] = None
    index: Optional[float] = None
    lastUpdated: Optional[str] = None
    playerId: str = ""

    def __post_init__(self):
        self.playerId = self.id
