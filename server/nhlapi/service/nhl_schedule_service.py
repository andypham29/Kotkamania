from datetime import datetime

from helper.http_helper import HttpHelper
from server.commons.helper.calendar_helper import CalendarHelper
from server.nhlapi.model.nhl_schedule import NhlGame, Schedule, TeamGameInfo
from server.nhlapi.service.nhl_team_service import NhlTeamService


class NHLScheduleService:

    def __init__(self):
        pass

    def get_current_week_schedule_by_teamId(self, id):
        monday = CalendarHelper.get_current_week_monday().strftime("%Y-%m-%d")
        sunday = CalendarHelper.get_current_week_sunday().strftime("%Y-%m-%d")

        info_json = HttpHelper.get(self.__get_schedule_url() + f"?teamId={id}&startDate={monday}&endDate={sunday}")
        days = info_json["dates"]
        games = []
        for day in days:
            date = day.get("date")
            games += [self.__get_schedule_game(game, date) for game in day.get("games")]
        return Schedule(monday, sunday, games)
        # player["shootsCatches"] if player.get("shootsCatches") is not None else None

    def __get_schedule_game(self, json, date):
        gamePk = json.get("gamePk")
        home_json = json.get("teams").get("home")
        away_json = json.get("teams").get("away")
        home = TeamGameInfo(teamId=home_json.get("team").get("id"),
                            abbreviation=None,
                            teamName=home_json.get("team").get("name"),
                            score=home_json.get("score"))
        away = TeamGameInfo(teamId=away_json.get("team").get("id"),
                            abbreviation=None,
                            teamName=away_json.get("team").get("name"),
                            score=away_json.get("score"))

        display_day = datetime.strptime(date, "%Y-%m-%d").day % 7 - 1
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
