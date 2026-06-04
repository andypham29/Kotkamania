from dataclasses import dataclass
from typing import Optional


@dataclass
class SkaterMiscellaneous:
    blockedShots: Optional[int] = None
    blockedShotsPer60: Optional[float] = None
    emptyNetAssists: Optional[int] = None
    emptyNetGoals: Optional[int] = None
    emptyNetPoints: Optional[int] = None
    firstGoals: Optional[int] = None
    gamesPlayed: Optional[int] = None
    giveaways: Optional[int] = None
    giveawaysPer60: Optional[float] = None
    hits: Optional[int] = None
    hitsPer60: Optional[float] = None
    lastName: Optional[str] = None
    missedShotCrossbar: Optional[int] = None
    missedShotFailedBankAttempt: Optional[int] = None
    missedShotGoalpost: Optional[int] = None
    missedShotOverNet: Optional[int] = None
    missedShotShort: Optional[int] = None
    missedShotWideOfNet: Optional[int] = None
    missedShots: Optional[int] = None
    otGoals: Optional[int] = None
    playerId: Optional[int] = None
    positionCode: Optional[str] = None
    seasonId: Optional[int] = None
    shootsCatches: Optional[str] = None
    shotAttemptsBlocked: Optional[int] = None
    skaterFullName: Optional[str] = None
    takeaways: Optional[int] = None
    takeawaysPer60: Optional[float] = None
    teamAbbrevs: Optional[str] = None
    timeOnIcePerGame: Optional[float] = None
    totalShotAttempts: Optional[int] = None
