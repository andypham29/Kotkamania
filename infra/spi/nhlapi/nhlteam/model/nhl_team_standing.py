from dataclasses import dataclass


@dataclass
class TeamStanding:
    abbreviation: str
    fullName: str | None = None
    leagueRank: int | None = None
    conference: str | None = None
    division: str | None = None
    streak: str | None = None
    logoUrl: str | None = None
