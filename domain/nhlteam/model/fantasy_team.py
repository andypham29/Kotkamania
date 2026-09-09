from dataclasses import dataclass, replace
from typing import Iterable

from domain.fantasyplayer.model.fantasy_nhl_player import FantasyNhlPlayer, StatValue
from infra.spi.nhlapi.nhlteam.model.nhl_team_standing import TeamStanding
from infra.spi.nhlapi.nhlteam.model.nhl_team_summary import TeamSummary

_FORWARD_CODES = frozenset({"C", "L", "R"})
_SKATER_STAT_FIELDS = (
    "games",
    "goals",
    "assists",
    "points",
    "plusMinus",
    "powerPlayGoals",
    "powerPlayPoints",
    "shots",
    "hits",
    "blocked",
)
_GOALIE_STAT_FIELDS = (
    "gamesPlayed",
    "wins",
    "losses",
    "otLosses",
    "saves",
    "goalsAgainst",
    "shutouts",
)


def _stat_number(container, field_name: str) -> float:
    if container is None:
        return 0
    raw = getattr(container, field_name, None)
    if raw is None:
        return 0
    if isinstance(raw, StatValue):
        raw = raw.value
    try:
        return float(raw or 0)
    except (TypeError, ValueError):
        return 0


def _grade(player: FantasyNhlPlayer) -> float | None:
    try:
        if player.fantasyGrade is None:
            return None
        return float(player.fantasyGrade)
    except (TypeError, ValueError):
        return None


def _best_player(players: Iterable[FantasyNhlPlayer]) -> FantasyNhlPlayer | None:
    ranked = [(player, grade) for player in players if (grade := _grade(player)) is not None]
    if not ranked:
        return None
    return max(ranked, key=lambda item: item[1])[0]


def _position(player: FantasyNhlPlayer) -> str:
    return (player.positionCode or "").upper()


def _is_goalie(player: FantasyNhlPlayer) -> bool:
    return _position(player) == "G"


def _is_defense(player: FantasyNhlPlayer) -> bool:
    return _position(player) == "D"


def _is_forward(player: FantasyNhlPlayer) -> bool:
    return _position(player) in _FORWARD_CODES


@dataclass
class FantasyTeamNhlStat:
    fullName: str | None = None
    gamesPlayed: int | None = None
    wins: int | None = None
    losses: int | None = None
    otLosses: int | None = None
    points: int | None = None
    pointPct: float | None = None
    goalsFor: int | None = None
    goalsAgainst: int | None = None
    goalsForPerGame: float | None = None
    goalsAgainstPerGame: float | None = None
    powerPlayPct: float | None = None
    penaltyKillPct: float | None = None
    faceoffWinPct: float | None = None
    shotsForPerGame: float | None = None
    shotsAgainstPerGame: float | None = None
    teamShutouts: int | None = None
    leagueRank: int | None = None
    conference: str | None = None
    division: str | None = None
    streak: str | None = None
    logoUrl: str | None = None

    @classmethod
    def from_summary(cls, summary: TeamSummary) -> "FantasyTeamNhlStat":
        return cls(
            fullName=summary.teamFullName,
            gamesPlayed=summary.gamesPlayed,
            wins=summary.wins,
            losses=summary.losses,
            otLosses=summary.otLosses,
            points=summary.points,
            pointPct=summary.pointPct,
            goalsFor=summary.goalsFor,
            goalsAgainst=summary.goalsAgainst,
            goalsForPerGame=summary.goalsForPerGame,
            goalsAgainstPerGame=summary.goalsAgainstPerGame,
            powerPlayPct=summary.powerPlayPct,
            penaltyKillPct=summary.penaltyKillPct,
            faceoffWinPct=summary.faceoffWinPct,
            shotsForPerGame=summary.shotsForPerGame,
            shotsAgainstPerGame=summary.shotsAgainstPerGame,
            teamShutouts=summary.teamShutouts,
        )

    def with_standing(self, standing: TeamStanding) -> "FantasyTeamNhlStat":
        return replace(
            self,
            fullName=self.fullName or standing.fullName,
            leagueRank=standing.leagueRank,
            conference=standing.conference,
            division=standing.division,
            streak=standing.streak,
            logoUrl=standing.logoUrl,
        )

    @classmethod
    def from_nhl_sources(
        cls,
        summary: TeamSummary | None = None,
        standing: TeamStanding | None = None,
    ) -> "FantasyTeamNhlStat | None":
        if summary is None and standing is None:
            return None
        nhl = cls.from_summary(summary) if summary is not None else cls()
        if standing is not None:
            nhl = nhl.with_standing(standing)
        return nhl


@dataclass
class FantasyTeamSkaterStat:
    games: int = 0
    goals: int = 0
    assists: int = 0
    points: int = 0
    plusMinus: int = 0
    powerPlayGoals: int = 0
    powerPlayPoints: int = 0
    shots: int = 0
    hits: int = 0
    blocked: int = 0

    @classmethod
    def from_players(cls, players: Iterable[FantasyNhlPlayer]) -> "FantasyTeamSkaterStat":
        totals = {name: 0 for name in _SKATER_STAT_FIELDS}
        for player in players:
            if _is_goalie(player):
                continue
            for name in _SKATER_STAT_FIELDS:
                totals[name] += int(_stat_number(player.stat, name))
        return cls(**totals)


@dataclass
class FantasyTeamGoalieStat:
    gamesPlayed: int = 0
    wins: int = 0
    losses: int = 0
    otLosses: int = 0
    saves: int = 0
    goalsAgainst: int = 0
    shutouts: int = 0
    savePct: float | None = None

    @classmethod
    def from_players(cls, players: Iterable[FantasyNhlPlayer]) -> "FantasyTeamGoalieStat":
        totals = {name: 0 for name in _GOALIE_STAT_FIELDS}
        for player in players:
            if not _is_goalie(player):
                continue
            for name in _GOALIE_STAT_FIELDS:
                totals[name] += int(_stat_number(player.goalieStat, name))
        shots_against = totals["saves"] + totals["goalsAgainst"]
        save_pct = round(totals["saves"] / shots_against, 3) if shots_against else None
        return cls(**totals, savePct=save_pct)


@dataclass
class FantasyTeamBestPlayers:
    overall: FantasyNhlPlayer | None = None
    forward: FantasyNhlPlayer | None = None
    defense: FantasyNhlPlayer | None = None
    goalie: FantasyNhlPlayer | None = None

    @classmethod
    def from_players(cls, players: list[FantasyNhlPlayer]) -> "FantasyTeamBestPlayers":
        return cls(
            overall=_best_player(players),
            forward=_best_player(p for p in players if _is_forward(p)),
            defense=_best_player(p for p in players if _is_defense(p)),
            goalie=_best_player(p for p in players if _is_goalie(p)),
        )


@dataclass
class FantasyTeam:
    teamId: int
    abbreviation: str
    playerCount: int
    skaterCount: int
    goalieCount: int
    avgFantasyGrade: float | None
    maxFantasyGrade: float | None
    nhl: FantasyTeamNhlStat | None
    stat: FantasyTeamSkaterStat
    goalieStat: FantasyTeamGoalieStat
    best: FantasyTeamBestPlayers

    @classmethod
    def from_players(
        cls,
        team_id: int,
        players: list[FantasyNhlPlayer],
        *,
        abbreviation: str | None = None,
        nhl: FantasyTeamNhlStat | None = None,
    ) -> "FantasyTeam":
        goalies = [player for player in players if _is_goalie(player)]
        skaters = [player for player in players if not _is_goalie(player)]
        grades = [grade for player in players if (grade := _grade(player)) is not None]
        abbrev = abbreviation or next((p.teamName for p in players if p.teamName), "")
        return cls(
            teamId=team_id,
            abbreviation=abbrev,
            playerCount=len(players),
            skaterCount=len(skaters),
            goalieCount=len(goalies),
            avgFantasyGrade=round(sum(grades) / len(grades), 2) if grades else None,
            maxFantasyGrade=round(max(grades), 2) if grades else None,
            nhl=nhl,
            stat=FantasyTeamSkaterStat.from_players(skaters),
            goalieStat=FantasyTeamGoalieStat.from_players(goalies),
            best=FantasyTeamBestPlayers.from_players(players),
        )
