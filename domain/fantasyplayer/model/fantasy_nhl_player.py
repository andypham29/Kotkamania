from dataclasses import dataclass, field, fields
from typing import Any, Dict, Iterable, Optional, TypeVar

from infra.spi.sqlite.fantasyplayer.model.sqlite_fantasy_nhl_player import SqliteFantasyNhlPlayer
from infra.spi.sqlite.playerstat.model.nhl_player_stat import PlayerStat
from infra.spi.sqlite.playerstatpercentile.model.nhl_player_stat_percentile import PlayerStatPercentile
from server.commons.fantasybadge.model.fantasy_player_badge import FantasyPlayerBadge

T = TypeVar("T")


@dataclass
class StatValue:
    """Container for a single stat value and its percentile."""
    value: int = 0
    percentile: Optional[float] = None


def _to_int(value: Any) -> int:
    if value is None:
        return 0
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _stat_value_from_spi(
    stat_source: Any | None,
    percentile_source: Any | None,
    field_name: str,
) -> StatValue:
    value = _to_int(getattr(stat_source, field_name, None) if stat_source else None)
    percentile = getattr(percentile_source, field_name, None) if percentile_source else None
    return StatValue(value, percentile)


def index_by_player_id(records: Iterable[T | None]) -> dict[int, T]:
    """Index SPI records by playerId for O(1) lookup when assembling players."""
    indexed: dict[int, T] = {}
    for record in records:
        if record is None:
            continue
        player_id = getattr(record, "playerId", None)
        if player_id is not None:
            indexed[int(player_id)] = record
    return indexed


@dataclass
class DisplayGoalieStat:
    assists: StatValue = field(default_factory=StatValue)
    gamesPlayed: StatValue = field(default_factory=StatValue)
    gamesStarted: StatValue = field(default_factory=StatValue)
    goalieFullName: StatValue = field(default_factory=StatValue)
    goals: StatValue = field(default_factory=StatValue)
    goalsAgainst: StatValue = field(default_factory=StatValue)
    goalsAgainstAverage: StatValue = field(default_factory=StatValue)
    lastName: StatValue = field(default_factory=StatValue)
    losses: StatValue = field(default_factory=StatValue)
    otLosses: StatValue = field(default_factory=StatValue)
    penaltyMinutes: StatValue = field(default_factory=StatValue)
    playerId: StatValue = field(default_factory=StatValue)
    points: StatValue = field(default_factory=StatValue)
    savePct: StatValue = field(default_factory=StatValue)
    saves: StatValue = field(default_factory=StatValue)
    seasonId: StatValue = field(default_factory=StatValue)
    shootsCatches: StatValue = field(default_factory=StatValue)
    shotsAgainst: StatValue = field(default_factory=StatValue)
    shutouts: StatValue = field(default_factory=StatValue)
    teamAbbrevs: StatValue = field(default_factory=StatValue)
    ties: StatValue = field(default_factory=StatValue)
    timeOnIce: StatValue = field(default_factory=StatValue)
    wins: StatValue = field(default_factory=StatValue)

    @classmethod
    def from_spi(cls, goalie_stat: Any | None = None, goalie_percentile: Any | None = None) -> "DisplayGoalieStat":
        return cls(**{
            name: _stat_value_from_spi(goalie_stat, goalie_percentile, name)
            for name in (f.name for f in fields(cls))
        })


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

    @classmethod
    def from_spi(
        cls,
        player_stat: PlayerStat | None = None,
        player_percentile: PlayerStatPercentile | None = None,
    ) -> "DisplayStat":
        return cls(**{
            name: _stat_value_from_spi(player_stat, player_percentile, name)
            for name in (f.name for f in fields(cls))
        })


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
    goalieStat: Optional[DisplayGoalieStat] = field(default=None, init=True)

    def __post_init__(self):
        if self.badge is None:
            self.badge = FantasyPlayerBadge()
        if self.positionCode == "G":
            self.stat = None
            if self.goalieStat is None:
                self.goalieStat = DisplayGoalieStat()
        else:
            self.goalieStat = None
            if self.stat is None:
                self.stat = DisplayStat()
        self.playerId = self.id

    @classmethod
    def from_spi(
        cls,
        player: SqliteFantasyNhlPlayer,
        player_stat: PlayerStat | None = None,
        player_percentile: PlayerStatPercentile | None = None,
        goalie_stat: Any | None = None,
        goalie_percentile: Any | None = None,
    ) -> "FantasyNhlPlayer":
        is_goalie = player.positionCode == "G"
        return cls(
            id=player.id,
            skaterFullName=player.skaterFullName,
            positionCode=player.positionCode,
            teamId=player.teamId,
            fantasyGrade=player.fantasyGrade,
            yahooEligibility=player.yahooEligibility,
            avgPick=player.avgPick,
            avgRound=player.avgRound,
            percentDrafted=player.percentDrafted,
            teamName=player.teamName,
            nhlRank=player.nhlRank,
            badge=player.badge,
            stat=None if is_goalie else DisplayStat.from_spi(player_stat, player_percentile),
            goalieStat=DisplayGoalieStat.from_spi(goalie_stat, goalie_percentile) if is_goalie else None,
        )

    @staticmethod
    def resolve_player_id(player: SqliteFantasyNhlPlayer) -> int | None:
        try:
            return int(player.id)
        except (TypeError, ValueError):
            return None


@dataclass
class FantasyPlayerUpdateQuery:
    player_id: int
    score: float