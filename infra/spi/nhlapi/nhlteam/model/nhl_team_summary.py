from dataclasses import dataclass
from typing import Optional


@dataclass
class TeamSummary:
    faceoffWinPct: Optional[float] = None
    gamesPlayed: Optional[int] = None
    goalsAgainst: Optional[int] = None
    goalsAgainstPerGame: Optional[float] = None
    goalsFor: Optional[int] = None
    goalsForPerGame: Optional[float] = None
    losses: Optional[int] = None
    otLosses: Optional[int] = None
    penaltyKillNetPct: Optional[float] = None
    penaltyKillPct: Optional[float] = None
    pointPct: Optional[float] = None
    points: Optional[int] = None
    powerPlayNetPct: Optional[float] = None
    powerPlayPct: Optional[float] = None
    regulationAndOtWins: Optional[int] = None
    seasonId: Optional[int] = None
    shotsAgainstPerGame: Optional[float] = None
    shotsForPerGame: Optional[float] = None
    teamFullName: Optional[str] = None
    teamId: Optional[int] = None
    teamShutouts: Optional[int] = None
    ties: Optional[int] = None
    wins: Optional[int] = None
    winsInRegulation: Optional[int] = None
    winsInShootout: Optional[int] = None
