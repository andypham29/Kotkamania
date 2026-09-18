import requests

from infra.spi.nhlapi.model.club_stats import ClubStatsResponse


class ClubStats:
    """Provider for the NHL club-statistics endpoint."""

    BASE_URL = 'https://api-web.nhle.com/v1/club-stats'

    def get_club_stats(self, team_abbreviation, season, game_type=2):
        team = team_abbreviation.upper()
        url = '{}/{}/{}/{}'.format(self.BASE_URL, team, season, game_type)

        response = requests.get(url, timeout=10)
        response.raise_for_status()

        return ClubStatsResponse.from_dict(response.json())
