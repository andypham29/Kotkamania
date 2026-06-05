from dataclasses import dataclass, fields
from typing import Optional

from application.goaliestats.model.goalie_stat import GoalieStat


@dataclass
class GoalieStatORM:
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

    @classmethod
    def from_application(cls, stat: GoalieStat) -> "GoalieStatORM":
        return cls(**{f.name: getattr(stat, f.name) for f in fields(cls)})

    def to_application(self) -> GoalieStat:
        return GoalieStat(**{f.name: getattr(self, f.name) for f in fields(GoalieStat)})
