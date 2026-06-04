from dataclasses import dataclass
from typing import Optional


@dataclass
class SkaterScoringPerGame:
    assists: Optional[int] = None
    assistsPerGame: Optional[float] = None
    blockedShots: Optional[int] = None
    blocksPerGame: Optional[float] = None
    gamesPlayed: Optional[int] = None
    goals: Optional[int] = None
    goalsPerGame: Optional[float] = None
    hits: Optional[int] = None
    hitsPerGame: Optional[float] = None
    lastName: Optional[str] = None
    penaltyMinutes: Optional[int] = None
    penaltyMinutesPerGame: Optional[float] = None
    playerId: Optional[int] = None
    points: Optional[int] = None
    pointsPerGame: Optional[float] = None
    positionCode: Optional[str] = None
    primaryAssistsPerGame: Optional[float] = None
    seasonId: Optional[int] = None
    secondaryAssistsPerGame: Optional[float] = None
    shootsCatches: Optional[str] = None
    shots: Optional[int] = None
    shotsPerGame: Optional[float] = None
    skaterFullName: Optional[str] = None
    teamAbbrevs: Optional[str] = None
    timeOnIce: Optional[int] = None
    timeOnIcePerGame: Optional[float] = None
    totalPrimaryAssists: Optional[int] = None
    totalSecondaryAssists: Optional[int] = None
