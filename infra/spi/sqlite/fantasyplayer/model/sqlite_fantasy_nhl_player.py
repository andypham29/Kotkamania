from dataclasses import dataclass, field
from typing import Optional
from server.commons.fantasybadge.model.fantasy_player_badge import FantasyPlayerBadge


@dataclass
class SqliteDisplayStat:
    assists: int = 0
    goals: int = 0
    points: int = 0
    games: int = 0
    shots: int = 0
    hits: int = 0
    blocked: int = 0
    plusMinus: int = 0
    powerPlayGoals: int = 0
    powerPlayPoints: int = 0


@dataclass
class SqliteFantasyNhlPlayer:
    id: str = ""
    skaterFullName: str = ""
    positionCode: str = ""
    teamId: str = ""
    fantasyGrade: Optional[object] = None
    yahooEligibility: Optional[object] = None
    avgPick: Optional[object] = None
    avgRound: Optional[object] = None
    percentDrafted: Optional[object] = None
    teamName: str = "" # will store team abreviation instead
    nhlRank: Optional[object] = None
    badge: Optional[FantasyPlayerBadge] = field(default=None, init=True)
    stat: Optional[SqliteDisplayStat] = field(default=None, init=True)

    def __post_init__(self):
        if self.badge is None:
            self.badge = FantasyPlayerBadge()
        if self.stat is None:
            self.stat = SqliteDisplayStat()
        self.playerId = self.id
