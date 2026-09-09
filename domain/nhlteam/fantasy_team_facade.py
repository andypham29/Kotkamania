from __future__ import annotations

from collections import defaultdict

from domain.fantasyplayer.model.fantasy_nhl_player import FantasyNhlPlayer
from domain.nhlteam.model.fantasy_team import FantasyTeam, FantasyTeamNhlStat
from infra.spi.nhlapi.nhlteam.model.nhl_team_standing import TeamStanding
from infra.spi.nhlapi.nhlteam.model.nhl_team_summary import TeamSummary
from server.commons.helper.nhl_team_converter import NhlTeamConverter


def _resolve_team_id(player: FantasyNhlPlayer) -> int | None:
    try:
        return int(player.teamId)
    except (TypeError, ValueError):
        return None


def _abbrev(value: str | None) -> str:
    return (value or "").strip().upper()


class FantasyTeamFacade:
    def __init__(
        self,
        fantasy_player_facade=None,
        nhl_team_summary_service=None,
        nhl_team_standings_service=None,
    ):
        if fantasy_player_facade is None:
            from domain.fantasyplayer.fantasy_player_facade import DomainFantasyPlayerFacade
            fantasy_player_facade = DomainFantasyPlayerFacade()
        if nhl_team_summary_service is None:
            from infra.spi.nhlapi.nhlteam.nhl_team_summary_service import NhlTeamSummaryService
            nhl_team_summary_service = NhlTeamSummaryService()
        if nhl_team_standings_service is None:
            from infra.spi.nhlapi.nhlteam.nhl_team_standings_service import NhlTeamStandingsService
            nhl_team_standings_service = NhlTeamStandingsService()
        self.fantasy_player_facade = fantasy_player_facade
        self.nhl_team_summary_service = nhl_team_summary_service
        self.nhl_team_standings_service = nhl_team_standings_service

    def getAllFantasyTeams(self) -> list[FantasyTeam]:
        players = self.fantasy_player_facade.getAllFantasySkaters()
        summaries = self.nhl_team_summary_service.getAllTeams()
        standings = self.nhl_team_standings_service.getAll()
        teams = self._assemble(players, summaries, standings)
        teams.sort(key=self._sort_key)
        return teams

    def getFantasyTeam(self, team_id: int) -> FantasyTeam | None:
        wanted = int(team_id)
        for team in self.getAllFantasyTeams():
            if team.teamId == wanted:
                return team
        return None

    def _assemble(
        self,
        players: list[FantasyNhlPlayer],
        summaries: list[TeamSummary],
        standings: list[TeamStanding],
    ) -> list[FantasyTeam]:
        players_by_id, players_by_abbrev = self._group_players(players)
        standings_by_abbrev = {_abbrev(row.abbreviation): row for row in standings if row.abbreviation}
        standings_by_name = {
            (row.fullName or "").strip().lower(): row
            for row in standings
            if row.fullName
        }

        teams: list[FantasyTeam] = []
        emitted_ids: set[int] = set()

        for summary in summaries:
            if summary.teamId is None:
                continue
            summary_id = int(summary.teamId)
            abbrev = self._abbrev_for_summary(summary, standings_by_name)
            standing = standings_by_abbrev.get(abbrev) if abbrev else None
            roster = list(players_by_id.get(summary_id, []))
            if not roster and abbrev:
                roster = list(players_by_abbrev.get(abbrev, []))
            team_id = self._team_id_for(summary_id, roster)
            if team_id in emitted_ids:
                continue
            teams.append(FantasyTeam.from_players(
                team_id,
                roster,
                abbreviation=abbrev or "",
                nhl=FantasyTeamNhlStat.from_nhl_sources(summary, standing),
            ))
            emitted_ids.add(team_id)

        for team_id, roster in players_by_id.items():
            if team_id in emitted_ids:
                continue
            abbrev = _abbrev(roster[0].teamName) or _abbrev(NhlTeamConverter.options.get(team_id))
            standing = standings_by_abbrev.get(abbrev) if abbrev else None
            teams.append(FantasyTeam.from_players(
                team_id,
                roster,
                abbreviation=abbrev,
                nhl=FantasyTeamNhlStat.from_nhl_sources(None, standing),
            ))
            emitted_ids.add(team_id)

        return teams

    @staticmethod
    def _group_players(
        players: list[FantasyNhlPlayer],
    ) -> tuple[dict[int, list[FantasyNhlPlayer]], dict[str, list[FantasyNhlPlayer]]]:
        by_id: dict[int, list[FantasyNhlPlayer]] = defaultdict(list)
        by_abbrev: dict[str, list[FantasyNhlPlayer]] = defaultdict(list)
        for player in players:
            team_id = _resolve_team_id(player)
            if team_id is not None:
                by_id[team_id].append(player)
            abbrev = _abbrev(player.teamName)
            if abbrev:
                by_abbrev[abbrev].append(player)
        return by_id, by_abbrev

    @staticmethod
    def _abbrev_for_summary(
        summary: TeamSummary,
        standings_by_name: dict[str, TeamStanding],
    ) -> str:
        try:
            mapped = NhlTeamConverter.options.get(int(summary.teamId))
        except (TypeError, ValueError):
            mapped = None
        if mapped:
            return _abbrev(mapped)
        full_name = (summary.teamFullName or "").strip().lower()
        standing = standings_by_name.get(full_name)
        if standing:
            return _abbrev(standing.abbreviation)
        return ""

    @staticmethod
    def _team_id_for(summary_id: int, players: list[FantasyNhlPlayer]) -> int:
        if players:
            player_team_id = _resolve_team_id(players[0])
            if player_team_id is not None:
                return player_team_id
        return summary_id

    @staticmethod
    def _sort_key(team: FantasyTeam):
        points = team.nhl.points if team.nhl and team.nhl.points is not None else -1
        grade = team.maxFantasyGrade if team.maxFantasyGrade is not None else -1
        return (-points, -grade, team.abbreviation or "")
