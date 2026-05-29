from dataclasses import dataclass
from typing import Optional


@dataclass
class SkaterTimeOnIce:
    evTimeOnIce: Optional[int] = None
    evTimeOnIcePerGame: Optional[float] = None
    gamesPlayed: Optional[int] = None
    lastName: Optional[str] = None
    otTimeOnIce: Optional[int] = None
    otTimeOnIcePerOtGame: Optional[float] = None
    playerId: Optional[int] = None
    positionCode: Optional[str] = None
    ppTimeOnIce: Optional[int] = None
    ppTimeOnIcePerGame: Optional[float] = None
    seasonId: Optional[int] = None
    shTimeOnIce: Optional[int] = None
    shTimeOnIcePerGame: Optional[float] = None
    shifts: Optional[int] = None
    shiftsPerGame: Optional[float] = None
    shootsCatches: Optional[str] = None
    skaterFullName: Optional[str] = None
    teamAbbrevs: Optional[str] = None
    timeOnIce: Optional[int] = None
    timeOnIcePerGame: Optional[float] = None
    timeOnIcePerShift: Optional[float] = None
