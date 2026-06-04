from dataclasses import dataclass
from typing import Optional


@dataclass
class SkaterPuckPossession:
    defensiveZoneStartPct: Optional[float] = None
    faceoffPct5v5: Optional[float] = None
    gamesPlayed: Optional[int] = None
    goalsPct: Optional[float] = None
    individualSatForPer60: Optional[float] = None
    individualShotsForPer60: Optional[float] = None
    lastName: Optional[str] = None
    neutralZoneStartPct: Optional[float] = None
    offensiveZoneStartPct: Optional[float] = None
    offensiveZoneStartRatio: Optional[float] = None
    onIceShootingPct: Optional[float] = None
    playerId: Optional[int] = None
    positionCode: Optional[str] = None
    satPct: Optional[float] = None
    seasonId: Optional[int] = None
    shootsCatches: Optional[str] = None
    skaterFullName: Optional[str] = None
    teamAbbrevs: Optional[str] = None
    timeOnIcePerGame5v5: Optional[int] = None
    usatPct: Optional[float] = None
