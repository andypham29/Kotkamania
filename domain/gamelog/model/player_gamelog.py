from dataclasses import dataclass
from typing import Optional


@dataclass
class PlayerGameLog:
    date: Optional[str] = None
    opponent: Optional[str] = None
    goals: Optional[int] = None
    assists: Optional[int] = None
    points: Optional[int] = None
    pim: Optional[int] = None
    plusMinus: Optional[int] = None
    powerPlayGoals: Optional[int] = None
    powerPlayPoints: Optional[int] = None
    timeOnIce: Optional[str] = None
    evenTimeOnIce: Optional[str] = None
    shortHandedTimeOnIce: Optional[str] = None
    powerPlayTimeOnIce: Optional[str] = None
    shots: Optional[int] = None
    hits: Optional[int] = None
    blocked: Optional[int] = None
