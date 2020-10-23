from helper.http_helper import HttpHelper
from server.nhlapi.model.team import Team


class NhlTeamService:

    def __init__(self):
        pass

    def getAllTeams(self):
        json = HttpHelper.get('https://statsapi.web.nhl.com/api/v1/standings')
        return self.__getTeamsFromAllDivision(json)

    def __sortTeamsBy(self, teams):
        return sorted(teams, key=lambda x: x.leagueRank, reverse=True)

    def __getTeamsFromAllDivision(self, json):
        teams = []
        for item in json['records']:
            teams += (self.__getAllTeamsPerDivision(item['teamRecords']))
        return teams

    def __getAllTeamsPerDivision(self, json):
        teams = []
        for item in json:
            name = item['team']['name']
            record = item['leagueRecord']
            leagueRank = item['leagueRank']

            # print("({0}) {1}: {2}".format(leagueRank, name, record))
            teams.append(Team(name, record, int(leagueRank)))
        return teams
