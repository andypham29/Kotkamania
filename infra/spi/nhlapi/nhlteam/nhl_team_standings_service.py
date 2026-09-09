from helper.http_helper import HttpHelper
from infra.spi.nhlapi.nhlteam.model.nhl_team_standing import TeamStanding

_STANDINGS_URL = "https://api-web.nhle.com/v1/standings/now"


def _default_text(value) -> str | None:
    if isinstance(value, dict):
        return value.get("default")
    return value


class NhlTeamStandingsService:
    def getAll(self) -> list[TeamStanding]:
        payload = HttpHelper.get(_STANDINGS_URL)
        if not payload:
            return []
        return [self._to_model(row) for row in payload.get("standings") or []]

    def _to_model(self, row: dict) -> TeamStanding:
        streak_code = row.get("streakCode")
        streak_count = row.get("streakCount")
        streak = f"{streak_code}{streak_count}" if streak_code and streak_count is not None else None
        return TeamStanding(
            abbreviation=_default_text(row.get("teamAbbrev")) or "",
            fullName=_default_text(row.get("teamName")),
            leagueRank=row.get("leagueSequence"),
            conference=row.get("conferenceAbbrev"),
            division=row.get("divisionAbbrev"),
            streak=streak,
            logoUrl=row.get("teamLogo"),
        )
