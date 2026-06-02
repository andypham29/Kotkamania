from dataclasses import dataclass
from typing import Optional


@dataclass
class PlayerStatPercentile:
    # Identifiers
    playerId: Optional[int] = None
    seasonId: Optional[int] = None

    timeOnIce: Optional[int] = None
    assists: Optional[int] = None
    goals: Optional[int] = None
    pim: Optional[int] = None
    shots: Optional[int] = None
    games: Optional[int] = None
    hits: Optional[int] = None
    powerPlayGoals: Optional[int] = None
    powerPlayPoints: Optional[int] = None
    powerPlayTimeOnIce: Optional[int] = None
    evenTimeOnIce: Optional[int] = None
    penaltyMinutes: Optional[int] = None
    faceOffPct: Optional[int] = None
    shotPct: Optional[int] = None
    gameWinningGoals: Optional[int] = None
    overTimeGoals: Optional[int] = None
    shortHandedGoals: Optional[int] = None
    shortHandedPoints: Optional[int] = None
    shortHandedTimeOnIce: Optional[int] = None
    blocked: Optional[int] = None
    plusMinus: Optional[int] = None
    points: Optional[int] = None
    shifts: Optional[int] = None
    timeOnIcePerGame: Optional[int] = None
    evenTimeOnIcePerGame: Optional[int] = None
    shortHandedTimeOnIcePerGame: Optional[int] = None
    powerPlayTimeOnIcePerGame: Optional[int] = None