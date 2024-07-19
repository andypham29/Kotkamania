from helper.http_helper import HttpHelper
from server.commons.helper.nhl_team_converter import NhlTeamConverter
from server.nhlapi.model.nhl_team import Team, TeamStat


class NhlTeamService:

    def __init__(self):
        pass

    def getAllTeams(self):
        json = HttpHelper.get('https://api-web.nhle.com/v1/standings/now').get("standings", None)
        return [self.__get_team_stat(i) for i in json]

    def __get_team_stat(self, team):
        teamId = NhlTeamConverter.get_teamId_by_abr(team.get("teamAbbrev").get("default"))
        teamStats = TeamStat(
            gamesPlayed=team.get("gamesPlayed"),
            wins=team.get("wins"),
            losses=team.get("losses"),
            ot=team.get("otLosses"),
            pts=team.get("points"),
            ptPctg=team.get("pointPctg"),
            goalsPerGame=team.get("goalFor"),
            goalsAgainstPerGame=team.get("goalsForPctg"),
            evGGARatio=team.get("points"),
            powerPlayPercentage=team.get("points"),
            powerPlayGoals=team.get("points"),
            powerPlayGoalsAgainst=team.get("points"),
            powerPlayOpportunities=team.get("points"),
            penaltyKillPercentage=team.get("points"),
            shotsPerGame=team.get("points"),
            shotsAllowed=team.get("points"),
            winScoreFirst=team.get("points"),
            winOppScoreFirst=team.get("points"),
            winLeadFirstPer=team.get("points"),
            winLeadSecondPer=team.get("points"),
            winOutshootOpp=team.get("points"),
            winOutshotByOpp=team.get("points"),
            faceOffsTaken=team.get("points"),
            faceOffsWon=team.get("points"),
            faceOffsLost=team.get("points"),
            faceOffWinPercentage=team.get("points"),
            shootingPctg=team.get("points"),
            savePctg=team.get("points"),
        )
        return Team(
            id=teamId,
            abbreviation=team.get("teamAbbrev").get("default"),
            name=team.get("teamName").get("default"),
            points=team.get("points"),
            leagueRank=team.get("points"),
            teamStats=teamStats
        )

    def getAllTeamsForDraft(self):
        pass


if __name__ == '__main__':
    teams = NhlTeamService().getAllTeams()
    print([t.__dict__ for t in teams])
