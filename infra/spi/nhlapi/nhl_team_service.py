from helper.http_helper import HttpHelper
from infra.spi.nhlapi.model.nhl_team import Team
from server.commons.helper.nhl_team_converter import NhlTeamConverter


class NhlTeamService:

    def __init__(self):
        pass

    def getAllTeams(self):
        json = HttpHelper.get('https://api.nhle.com/stats/rest/en/team').get("data", None)

        all_existing_teams = [self.__get_team_info(i) for i in json]
        return list(filter(lambda n: self.__exists_team(n), all_existing_teams))

    def __exists_team(self, team):
        teamId = NhlTeamConverter.get_teamId_by_abr(team.triCode)
        return teamId is not None

    def __get_team_info(self, data):
        return Team(
            data.get("id"),
            data.get("franchiseId"),
            data.get("fullName"),
            data.get("leagueId"),
            data.get("rawTricode"),
            data.get("triCode")
        )


if __name__ == '__main__':
    from dataclasses import asdict
    import json

    teams = NhlTeamService().getAllTeams()
    for s in teams:
        # 2: "NYI",
        print(f"{s.id}: \"{s.abbreviation}\",")
        # print(json.dumps(asdict(s), indent=2))
