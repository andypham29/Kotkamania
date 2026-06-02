from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from server.commons.fantasybadge.model.fantasy_player_badge import FantasyPlayerBadge


@dataclass
class StatValue:
    """Container for a single stat value and its percentile."""
    value: int = 0
    percentile: Optional[float] = None


@dataclass
class DisplayStat:
    assists: StatValue = field(default_factory=StatValue)
    goals: StatValue = field(default_factory=StatValue)
    points: StatValue = field(default_factory=StatValue)
    games: StatValue = field(default_factory=StatValue)
    shots: StatValue = field(default_factory=StatValue)
    hits: StatValue = field(default_factory=StatValue)
    blocked: StatValue = field(default_factory=StatValue)
    plusMinus: StatValue = field(default_factory=StatValue)
    powerPlayGoals: StatValue = field(default_factory=StatValue)
    powerPlayPoints: StatValue = field(default_factory=StatValue)

    def to_dict(self) -> Dict[str, Any]:
        """Return plain dict with nested {value, percentile} objects for JSON serialization."""
        return {
            'assists': {'value': self.assists.value, 'percentile': self.assists.percentile},
            'goals': {'value': self.goals.value, 'percentile': self.goals.percentile},
            'points': {'value': self.points.value, 'percentile': self.points.percentile},
            'games': {'value': self.games.value, 'percentile': self.games.percentile},
            'shots': {'value': self.shots.value, 'percentile': self.shots.percentile},
            'hits': {'value': self.hits.value, 'percentile': self.hits.percentile},
            'blocked': {'value': self.blocked.value, 'percentile': self.blocked.percentile},
            'plusMinus': {'value': self.plusMinus.value, 'percentile': self.plusMinus.percentile},
            'powerPlayGoals': {'value': self.powerPlayGoals.value, 'percentile': self.powerPlayGoals.percentile},
            'powerPlayPoints': {'value': self.powerPlayPoints.value, 'percentile': self.powerPlayPoints.percentile}
        }

    def __post_init__(self):
        # Coerce plain int/None fields to StatValue objects for backward compatibility
        for field_name in ('assists', 'goals', 'points', 'games', 'shots', 'hits', 'blocked', 'plusMinus',
                           'powerPlayGoals', 'powerPlayPoints'):
            val = getattr(self, field_name)
            if isinstance(val, StatValue):
                continue
            if val is None:
                setattr(self, field_name, StatValue(0, None))
            elif isinstance(val, (int, float)):
                setattr(self, field_name, StatValue(int(val), None))
            elif isinstance(val, dict):
                # dict with possible keys 'value' and 'percentile'
                v = val.get('value', 0)
                p = val.get('percentile', None)
                setattr(self, field_name, StatValue(int(v) if v is not None else 0, p))
            else:
                # fallback: wrap into StatValue if possible
                try:
                    setattr(self, field_name, StatValue(int(val), None))
                except Exception:
                    setattr(self, field_name, StatValue(0, None))


@dataclass
class FantasyNhlPlayer:
    id: str = ""
    skaterFullName: str = ""
    positionCode: str = ""
    teamId: str = ""
    fantasyGrade: Optional[object] = None
    yahooEligibility: Optional[object] = None
    avgPick: Optional[object] = None
    avgRound: Optional[object] = None
    percentDrafted: Optional[object] = None
    teamName: str = ""
    nhlRank: Optional[object] = None
    badge: Optional[FantasyPlayerBadge] = field(default=None, init=True)
    stat: Optional[DisplayStat] = field(default=None, init=True)

    def __post_init__(self):
        if self.badge is None:
            self.badge = FantasyPlayerBadge()
        if self.stat is None:
            self.stat = DisplayStat()
        self.playerId = self.id

@dataclass
class FantasyPlayerUpdateQuery:
    player_id: int
    score: float