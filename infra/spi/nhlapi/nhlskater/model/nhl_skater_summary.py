from dataclasses import dataclass
from typing import Optional


@dataclass
class SkaterSummary:
    assists: Optional[int] = None
    evGoals: Optional[int] = None
    evPoints: Optional[int] = None
    faceoffWinPct: Optional[float] = None
    gameWinningGoals: Optional[int] = None
    gamesPlayed: Optional[int] = None
    goals: Optional[int] = None
    lastName: Optional[str] = None
    otGoals: Optional[int] = None
    penaltyMinutes: Optional[int] = None
    playerId: Optional[int] = None
    plusMinus: Optional[int] = None
    points: Optional[int] = None
    pointsPerGame: Optional[float] = None
    positionCode: Optional[str] = None
    ppGoals: Optional[int] = None
    ppPoints: Optional[int] = None
    seasonId: Optional[int] = None
    shGoals: Optional[int] = None
    shPoints: Optional[int] = None
    shootingPct: Optional[float] = None
    shootsCatches: Optional[str] = None
    shots: Optional[int] = None
    skaterFullName: Optional[str] = None
    teamAbbrevs: Optional[str] = None
    timeOnIcePerGame: Optional[float] = None
