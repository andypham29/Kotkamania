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
        info_json = HttpHelper.get(
            self.__get_schedule_url() + f"?startDate={self.monday}&endDate={self.sunday}")
        days = info_json["dates"]

        games = []
        for day in days:
            date = day.get("date")
            games += [self.__get_schedule_game(game, date, self.monday) for game in day.get("games")]

        teams = self.__get_games_of_all_teams(games)
        return Schedule(self.monday, self.sunday, teams)

    def get_current_week_schedule_by_teamId(self, id):
        info_json = HttpHelper.get(
            self.__get_schedule_url() + f"?teamId={id}&startDate={self.monday}&endDate={self.sunday}")
        days = info_json["dates"]
        games = []
        for day in days:
            date = day.get("date")
            games += [self.__get_schedule_game(game, date, self.monday) for game in day.get("games")]

        teams = [Team(id, games)]
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
        gamePk = json.get("gamePk")
        home_json = json.get("teams").get("home")
        away_json = json.get("teams").get("away")
        home = TeamGameInfo(teamId=home_json.get("team").get("id"),
                            teamName=home_json.get("team").get("name"),
                            score=home_json.get("score"))
        away = TeamGameInfo(teamId=away_json.get("team").get("id"),
                            teamName=away_json.get("team").get("name"),
                            score=away_json.get("score"))

        display_day = (datetime.strptime(date, "%Y-%m-%d").day - datetime.strptime(monday, "%Y-%m-%d").day)
        return NhlGame(day=display_day,
                       date=date,
                       gamePk=gamePk,
                       homeTeam=home,
                       awayTeam=away)

    @staticmethod
    def __get_schedule_url():
        return f"https://statsapi.web.nhl.com/api/v1/schedule"


if __name__ == '__main__':
    print([a.__dict__ for a in NhlTeamService().getAllTeams() if a.name == "Montréal Canadiens"])
    schedule = NHLScheduleService().get_current_week_schedule_by_teamId(8)

    print(schedule.__dict__)
    print([a.__dict__ for a in schedule.games])
