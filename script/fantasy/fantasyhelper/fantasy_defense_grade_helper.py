import datetime
import json

from script.fantasy.model.fantasy_skater_grade import FantasySkaterGrade


class FantasyDefenseGradeHelper:

    def __init__(self):
        pass

    def getDefenseGrade(self, skaterFullName, player_stat):
        grade = 0

        grade_g = self.__calculate_grade_goals(player_stat)
        grade_a = self.__calculate_grade_assists(player_stat)
        grade_p = self.__calculate_grade_points(player_stat)
        grade_ppg = self.__calculate_grade_ppgoals(player_stat)
        grade_ppa = self.__calculate_grade_ppassists(player_stat)
        grade_ppp = self.__calculate_grade_points(player_stat)
        grade_shotPct = self.__calculate_grade_shotPct(player_stat)
        grade_toi = self.__calculate_grade_toi(player_stat)
        grade_pptoi = self.__calculate_grade_pptoi(player_stat)
        grade_evtoi = self.__calculate_grade_evtoi(player_stat)
        grade_shotAttempt = self.__calculate_grade_shotAttempt(player_stat)

        grade_obj = FantasySkaterGrade(grade_g, grade_a, grade_p, grade_ppg, grade_ppa,
                                       grade_ppp, grade_shotPct, grade_toi, grade_pptoi,
                                       grade_evtoi, grade_shotAttempt)

        index = self.shotPctIndex(player_stat=player_stat)
        general = ((grade_ppg * index + grade_ppa + grade_ppp * grade_shotPct) / 3 * (
                (grade_toi + grade_pptoi * 5 + grade_evtoi * 3 + grade_shotAttempt) / 10) * 1.125)

        print(f"[{skaterFullName}|{round(general, 2)}|{index}]{json.dumps(grade_obj.__dict__)}")

        grade += (grade_g + grade_a + grade_p + general * 1.5 * index) / 50 * 100

        return round(grade, 2)

    def shotPctIndex(self, player_stat=None):
        grade_toi = self.__calculate_grade_toi(player_stat)
        grade_pptoi = self.__calculate_grade_pptoi(player_stat)
        grade_evtoi = self.__calculate_grade_evtoi(player_stat)
        grade_shotAttempt = self.__calculate_grade_shotAttempt(player_stat)

        return round(-0.1875 * ((grade_toi + grade_pptoi + grade_evtoi + grade_shotAttempt) / 5) ** 3 + 1.2, 2)

    def __calculate_grade_shotAttempt(self, player_stat):
        shotPctIndex = round(-0.055 * (player_stat.shotPct / 12) ** 3 + 1.05, 2)
        return ((player_stat.shots / player_stat.games) ** shotPctIndex) / 2

    def __calculate_grade_goals(self, player_stat):
        return -0.003 * (player_stat.goals / player_stat.games * 82 - 30) ** 2 + 10

    def __calculate_grade_assists(self, player_stat):
        return -0.0015 * (player_stat.assists / player_stat.games * 82 - 50) ** 2 + 10

    def __calculate_grade_points(self, player_stat):
        return -0.0007 * (player_stat.points / player_stat.games * 82 - 90) ** 2 + 10

    def __calculate_grade_ppgoals(self, player_stat):
        return -0.003 * (player_stat.powerPlayGoals / player_stat.games * 82 - 30) ** 2 + 10

    def __calculate_grade_ppassists(self, player_stat):
        ppa = (player_stat.powerPlayPoints - player_stat.powerPlayGoals)
        return -0.0015 * (ppa / player_stat.games * 82 - 50) ** 2 + 10

    def __calculate_grade_pppoints(self, player_stat):
        return -0.0007 * (player_stat.points / player_stat.games * 82 - 80) ** 2 + 10

    def __calculate_grade_shotPct(self, player_stat):
        shotPct = player_stat.shotPct
        return 0.85 if shotPct <= 0.0 or not None else (shotPct / 100) ** -1 * 0.1

    def __calculate_grade_toi(self, player_stat):
        toi = datetime.datetime.strptime(player_stat.timeOnIcePerGame, '%M:%S')
        return (toi.minute * 60 + toi.second) / (20 * 60)

    def __calculate_grade_pptoi(self, player_stat):
        pptoi = datetime.datetime.strptime(player_stat.powerPlayTimeOnIcePerGame, '%M:%S')
        return (pptoi.minute * 60 + pptoi.second) / (2.5 * 60)

    def __calculate_grade_evtoi(self, player_stat):
        evtoi = datetime.datetime.strptime(player_stat.evenTimeOnIcePerGame, '%M:%S')
        return (evtoi.minute * 60 + evtoi.second) / (15 * 60)
