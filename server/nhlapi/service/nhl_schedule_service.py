from datetime import datetime

from helper.http_helper import HttpHelper
from server.commons.helper.calendar_helper import CalendarHelper
from server.commons.helper.nhl_team_converter import NhlTeamConverter
from server.nhlapi.model.nhl_schedule import NhlGame, Schedule, TeamGameInfo, Team
from server.nhlapi.service.nhl_team_service import NhlTeamService


class NHLScheduleService:

    def __init__(self):
        self.monday = CalendarHelper.get_current_week_monday().strftime("%Y-%m-%d")
        self.sunday = CalendarHelper.get_current_week_sunday().strftime("%Y-%m-%d")
        pass

    def get_current_week_games(self):
        info_json = HttpHelper.get(f"https://api-web.nhle.com/v1/schedule/{self.monday}")
        game_week = info_json["gameWeek"]

        games = []
        for day in game_week:
            date = day.get("date")
            games += [self.__get_schedule_game(game, date, self.monday) for game in day.get("games")]

        teams = self.__get_games_of_all_teams(games)
        return Schedule(self.monday, self.sunday, teams)

    def get_current_week_schedule_by_teamId(self, id):
        info_json = HttpHelper.get(f"https://api-web.nhle.com/v1/schedule/{self.monday}")
        game_week = info_json["gameWeek"]
        games = []
        for day in game_week:
            date = day.get("date")
            games += [self.__get_schedule_game(game, date, self.monday) for game in day.get("games")]

        # Filter games for the specific team
        team_games = [game for game in games if game.homeTeam.teamId == int(id) or game.awayTeam.teamId == int(id)]
        teams = [Team(int(id), team_games)]
        return Schedule(self.monday, self.sunday, teams)

    def __get_games_of_all_teams(self, games):
        teams = []
        for teamId in NhlTeamConverter.get_all_teamIds():
            team_games = self.__get_games_by_teamId(teamId, games)
            teams.append(Team(teamId, team_games))

        return teams

    def __get_games_by_teamId(self, teamId, games):
        team_games = []

        for game in games:
            if game.homeTeam.teamId == teamId or game.awayTeam.teamId == teamId:
                team_games.append(game)

        return team_games

    def __get_schedule_game(self, json, date, monday):
        gamePk = json.get("id")
        home_json = json.get("homeTeam")
        away_json = json.get("awayTeam")
        home = TeamGameInfo(teamId=home_json.get("id"),
                            teamName=home_json.get("commonName", {}).get("default", ""),
                            score=home_json.get("score", 0))
        away = TeamGameInfo(teamId=away_json.get("id"),
                            teamName=away_json.get("commonName", {}).get("default", ""),
                            score=away_json.get("score", 0))

        display_day = (datetime.strptime(date, "%Y-%m-%d") - datetime.strptime(monday, "%Y-%m-%d")).days
        return NhlGame(day=display_day,
                       date=date,
                       gamePk=gamePk,
                       homeTeam=home,
                       awayTeam=away)


if __name__ == '__main__':
    print([a.__dict__ for a in NhlTeamService().getAllTeams() if a.name == "Montréal Canadiens"])
    schedule = NHLScheduleService().get_current_week_schedule_by_teamId(8)

    print(schedule.__dict__)
    print([a.__dict__ for a in schedule.teams[0].games])
    print((datetime.strptime('2022-11-02', "%Y-%m-%d") - datetime.strptime('2022-10-31', "%Y-%m-%d")).days)
