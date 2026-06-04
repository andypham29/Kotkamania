from dataclasses import dataclass
from typing import Optional


@dataclass
class SkaterShotAttemptCount:
    gamesPlayed: Optional[int] = None
    lastName: Optional[str] = None
    playerId: Optional[int] = None
    positionCode: Optional[str] = None
    satAgainst: Optional[int] = None
    satAhead: Optional[int] = None
    satBehind: Optional[int] = None
    satClose: Optional[int] = None
    satFor: Optional[int] = None
    satRelative: Optional[float] = None
    satTied: Optional[int] = None
    satTotal: Optional[int] = None
    seasonId: Optional[int] = None
    shootsCatches: Optional[str] = None
    skaterFullName: Optional[str] = None
    teamAbbrevs: Optional[str] = None
    timeOnIcePerGame5v5: Optional[float] = None
    usatAgainst: Optional[int] = None
    usatAhead: Optional[int] = None
    usatBehind: Optional[int] = None
    usatClose: Optional[int] = None
    usatFor: Optional[int] = None
    usatRelative: Optional[float] = None
    usatTied: Optional[int] = None
    usatTotal: Optional[int] = None # unblocked shots attempts meaning shots for + missed shots for
