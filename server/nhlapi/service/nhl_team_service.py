from helper.http_helper import HttpHelper
from server.nhlapi.model.nhl_team import Team, TeamStat


class NhlTeamService:

    def __init__(self):
        pass

    def getAllTeams(self):
        # json = HttpHelper.get('https://statsapi.web.nhl.com/api/v1/teams')
        json = HttpHelper.get('https://statsapi.web.nhl.com/api/v1/teams?expand=team.stats')
        teams = []
        for item in json.get('teams'):
            teams.append(Team(
                id=item.get('id'),
                name=item.get('name'),
                abbreviation=item.get('abbreviation'),
                teamStats=TeamStat(
                    gamesPlayed=item.get('teamStats')[0].get('splits')[0].get('stat').get('gamesPlayed'),
                    wins=item.get('teamStats')[0].get('splits')[0].get('stat').get('wins'),
                    losses=item.get('teamStats')[0].get('splits')[0].get('stat').get('losses'),
                    ot=item.get('teamStats')[0].get('splits')[0].get('stat').get('ot'),
                    pts=item.get('teamStats')[0].get('splits')[0].get('stat').get('pts'),
                    ptPctg=item.get('teamStats')[0].get('splits')[0].get('stat').get('ptPctg'),
                    goalsPerGame=item.get('teamStats')[0].get('splits')[0].get('stat').get('goalsPerGame'),
                    goalsAgainstPerGame=item.get('teamStats')[0].get('splits')[0].get('stat').get(
                        'goalsAgainstPerGame'),
                    evGGARatio=item.get('teamStats')[0].get('splits')[0].get('stat').get('evGGARatio'),
                    powerPlayPercentage=item.get('teamStats')[0].get('splits')[0].get('stat').get(
                        'powerPlayPercentage'),
                    powerPlayGoals=item.get('teamStats')[0].get('splits')[0].get('stat').get('powerPlayGoals'),
                    powerPlayGoalsAgainst=item.get('teamStats')[0].get('splits')[0].get('stat').get(
                        'powerPlayGoalsAgainst'),
                    powerPlayOpportunities=item.get('teamStats')[0].get('splits')[0].get('stat').get(
                        'powerPlayOpportunities'),
                    penaltyKillPercentage=item.get('teamStats')[0].get('splits')[0].get('stat').get(
                        'penaltyKillPercentage'),
                    shotsPerGame=item.get('teamStats')[0].get('splits')[0].get('stat').get('shotsPerGame'),
                    shotsAllowed=item.get('teamStats')[0].get('splits')[0].get('stat').get('shotsAllowed'),
                    winScoreFirst=item.get('teamStats')[0].get('splits')[0].get('stat').get('winScoreFirst'),
                    winOppScoreFirst=item.get('teamStats')[0].get('splits')[0].get('stat').get('winOppScoreFirst'),
                    winLeadFirstPer=item.get('teamStats')[0].get('splits')[0].get('stat').get('winLeadFirstPer'),
                    winLeadSecondPer=item.get('teamStats')[0].get('splits')[0].get('stat').get('winLeadSecondPer'),
                    winOutshootOpp=item.get('teamStats')[0].get('splits')[0].get('stat').get('winOutshootOpp'),
                    winOutshotByOpp=item.get('teamStats')[0].get('splits')[0].get('stat').get('winOutshotByOpp'),
                    faceOffsTaken=item.get('teamStats')[0].get('splits')[0].get('stat').get('faceOffsTaken'),
                    faceOffsWon=item.get('teamStats')[0].get('splits')[0].get('stat').get('faceOffsWon'),
                    faceOffsLost=item.get('teamStats')[0].get('splits')[0].get('stat').get('faceOffsLost'),
                    faceOffWinPercentage=item.get('teamStats')[0].get('splits')[0].get('stat').get(
                        'faceOffWinPercentage'),
                    shootingPctg=item.get('teamStats')[0].get('splits')[0].get('stat').get('shootingPctg'),
                    savePctg=item.get('teamStats')[0].get('splits')[0].get('stat').get('savePctg')
                )
            ))
        return sorted(teams, key=lambda x: x.teamStats.pts, reverse=True)

    def getAllTeamsForDraft(self):
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
            id = item['team']['id']
            name = item['team']['name']
            record = item['points']
            leagueRank = item['leagueRank']

            teams.append(Team(id=id, name=name, points=record, leagueRank=int(leagueRank)))
        return teams


if __name__ == '__main__':
    teams = NhlTeamService().getAllTeams()
    print(teams[0].teamStats.__dict__)
