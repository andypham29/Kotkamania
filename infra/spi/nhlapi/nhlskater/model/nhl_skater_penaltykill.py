from dataclasses import dataclass
from typing import Optional


@dataclass
class SkaterPenaltyKill:
    gamesPlayed: Optional[int] = None
    lastName: Optional[str] = None
    playerId: Optional[int] = None
    positionCode: Optional[str] = None
    ppGoalsAgainstPer60: Optional[float] = None
    seasonId: Optional[int] = None
    shAssists: Optional[int] = None
    shGoals: Optional[int] = None
    shGoalsPer60: Optional[float] = None
    shIndividualSatFor: Optional[int] = None
    shIndividualSatForPer60: Optional[float] = None
    shPoints: Optional[int] = None
    shPointsPer60: Optional[float] = None
    shPrimaryAssists: Optional[int] = None
    shPrimaryAssistsPer60: Optional[float] = None
    shSecondaryAssists: Optional[int] = None
    shSecondaryAssistsPer60: Optional[float] = None
    shShootingPct: Optional[float] = None
    shShots: Optional[int] = None
    shShotsPer60: Optional[float] = None
    shTimeOnIce: Optional[int] = None
    shTimeOnIcePctPerGame: Optional[float] = None
    shTimeOnIcePerGame: Optional[float] = None
    skaterFullName: Optional[str] = None
    teamAbbrevs: Optional[str] = None
