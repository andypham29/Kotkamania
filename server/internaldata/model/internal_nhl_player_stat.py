from dataclasses import dataclass
from typing import Optional


@dataclass
class InternalPlayerStat:
    playerId: int
    seasonId: int
    timeOnIce: Optional[str] = None
    assists: Optional[int] = None
    goals: Optional[int] = None
    pim: Optional[int] = None
    shots: Optional[int] = None
    games: Optional[int] = None
    hits: Optional[int] = None
    powerPlayGoals: Optional[int] = None
    powerPlayPoints: Optional[int] = None
    powerPlayTimeOnIce: Optional[str] = None
    evenTimeOnIce: Optional[str] = None
    penaltyMinutes: Optional[int] = None
    faceOffPct: Optional[float] = None
    shotPct: Optional[float] = None
    gameWinningGoals: Optional[int] = None
    overTimeGoals: Optional[int] = None
    shortHandedGoals: Optional[int] = None
    shortHandedPoints: Optional[int] = None
    shortHandedTimeOnIce: Optional[str] = None
    blocked: Optional[int] = None
    plusMinus: Optional[int] = None
    points: Optional[int] = None
    shifts: Optional[int] = None
    timeOnIcePerGame: Optional[str] = None
    evenTimeOnIcePerGame: Optional[str] = None
    shortHandedTimeOnIcePerGame: Optional[str] = None
    powerPlayTimeOnIcePerGame: Optional[str] = None
