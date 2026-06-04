from dataclasses import dataclass
from typing import Optional


@dataclass
class SkaterPowerPlay:
    gamesPlayed: Optional[int] = None
    lastName: Optional[str] = None
    playerId: Optional[int] = None
    positionCode: Optional[str] = None
    ppAssists: Optional[int] = None
    ppGoals: Optional[int] = None
    ppGoalsForPer60: Optional[float] = None
    ppGoalsPer60: Optional[float] = None
    ppIndividualSatFor: Optional[int] = None
    ppIndividualSatForPer60: Optional[float] = None
    ppPoints: Optional[int] = None
    ppPointsPer60: Optional[float] = None
    ppPrimaryAssists: Optional[int] = None
    ppPrimaryAssistsPer60: Optional[float] = None
    ppSecondaryAssists: Optional[int] = None
    ppSecondaryAssistsPer60: Optional[float] = None
    ppShootingPct: Optional[float] = None
    ppShots: Optional[int] = None
    ppShotsPer60: Optional[float] = None
    ppTimeOnIce: Optional[int] = None
    ppTimeOnIcePctPerGame: Optional[float] = None
    ppTimeOnIcePerGame: Optional[float] = None
    seasonId: Optional[int] = None
    skaterFullName: Optional[str] = None
    teamAbbrevs: Optional[str] = None
