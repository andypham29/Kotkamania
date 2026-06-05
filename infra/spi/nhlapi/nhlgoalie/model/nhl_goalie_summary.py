from dataclasses import dataclass
from typing import Optional


@dataclass
class GoalieSummary:
    assists: Optional[int] = None
    gamesPlayed: Optional[int] = None
    gamesStarted: Optional[int] = None
    goalieFullName: Optional[str] = None
    goals: Optional[int] = None
    goalsAgainst: Optional[int] = None
    goalsAgainstAverage: Optional[float] = None
    lastName: Optional[str] = None
    losses: Optional[int] = None
    otLosses: Optional[int] = None
    penaltyMinutes: Optional[int] = None
    playerId: Optional[int] = None
    points: Optional[int] = None
    savePct: Optional[float] = None
    saves: Optional[int] = None
    seasonId: Optional[int] = None
    shootsCatches: Optional[str] = None
    shotsAgainst: Optional[int] = None
    shutouts: Optional[int] = None
    teamAbbrevs: Optional[str] = None
    ties: Optional[int] = None
    timeOnIce: Optional[int] = None
    wins: Optional[int] = None
