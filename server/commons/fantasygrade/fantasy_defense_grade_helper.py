from script.fantasy.model.fantasy_skater_grade import FantasySkaterGrade
from server.commons.helper.time_converter import TimeConverter


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

        scale = self.__scale_by_games_played(player_stat)
        print(skaterFullName, " evtoi: ", grade_evtoi, " scale: ", scale)

        grade += grade_g + grade_a + grade_p * 7 + grade_ppg + grade_ppp * grade_pptoi + grade_ppp * 3.25 + grade_toi * 4.5
        print(skaterFullName, grade_g, grade_a, grade_p, grade_ppg, grade_ppp, grade_pptoi)

        grade = grade * scale / 2
        return round(grade, 2)

    def shotPctIndex(self, player_stat=None):
        grade_toi = self.__calculate_grade_toi(player_stat)
        grade_pptoi = self.__calculate_grade_pptoi(player_stat)
        grade_evtoi = self.__calculate_grade_evtoi(player_stat)
        grade_shotAttempt = self.__calculate_grade_shotAttempt(player_stat)

        return round(-0.1875 * ((grade_toi + grade_pptoi + grade_evtoi + grade_shotAttempt) / 5) ** 3 + 1.2, 2)

    def __scale_by_games_played(self, player_stat):
        gp = player_stat.games
        if gp < 10:
            return 0.5
        elif 10 <= gp < 20:
            return 0.6
        elif 20 <= gp < 30:
            return 0.7
        elif 30 <= gp < 40:
            return 0.8
        else:
            return 1

    def __calculate_grade_shotAttempt(self, player_stat):
        if player_stat.games == 0:
            return 0
        shotPctIndex = round(-0.055 * (player_stat.shotPct / 12) ** 3 + 1.05, 2)
        return ((player_stat.shots / player_stat.games) ** shotPctIndex) / 2

    def __calculate_grade_goals(self, player_stat):
        if player_stat.games == 0:
            return 5
        # return -0.003 * (player_stat.goals / player_stat.games * 82 - 30) ** 2 + 10
        goal = player_stat.goals / player_stat.games * 82
        if goal < 3:
            return 6
        elif 3 <= goal < 5:
            return 7
        elif 5 <= goal < 10:
            return 8
        elif 10 <= goal < 15:
            return 8.5
        elif 15 <= goal < 20:
            return 9.3
        elif 20 <= goal < 22:
            return 9.5
        elif 22 <= goal < 25:
            return 9.7
        elif 25 <= goal < 30:
            return 9.8
        else:
            return 10

    def __calculate_grade_assists(self, player_stat):
        if player_stat.games == 0:
            return 5
        # return -0.0015 * (player_stat.assists / player_stat.games * 82 - 50) ** 2 + 10
        assists = player_stat.assists / player_stat.games * 82
        if assists < 5:
            return 6
        elif 5 <= assists < 10:
            return 6.5
        elif 10 <= assists < 20:
            return 7
        elif 20 <= assists < 25:
            return 8
        elif 25 <= assists < 30:
            return 8.8
        elif 30 <= assists < 40:
            return 9.3
        elif 40 <= assists < 50:
            return 9.5
        elif 50 <= assists < 60:
            return 9.8
        else:
            return 10

    def __calculate_grade_points(self, player_stat):
        if player_stat.games == 0:
            return 5
        # return -0.0007 * (player_stat.points / player_stat.games * 82 - 100) ** 2 + 10
        points = player_stat.points / player_stat.games * 82
        if points < 20:
            return 6
        elif 20 <= points < 30:
            return 7.5
        elif 30 <= points < 40:
            return 8
        elif 40 <= points < 50:
            return 8.5
        elif 50 <= points < 60:
            return 9
        elif 60 <= points < 65:
            return 9.3
        elif 65 <= points < 70:
            return 9.7
        elif 70 <= points < 75:
            return 9.8
        elif 75 <= points < 80:
            return 9.9
        else:
            return 10

    def __calculate_grade_ppgoals(self, player_stat):
        if player_stat.games == 0:
            return 6
        # return -0.003 * (player_stat.powerPlayGoals / player_stat.games * 82 - 40) ** 2 + 10
        ppgoals = player_stat.powerPlayGoals / player_stat.games * 82
        if ppgoals < 4:
            return 7
        elif 4 <= ppgoals < 6:
            return 8
        elif 6 <= ppgoals < 8:
            return 8.8
        elif 8 <= ppgoals < 10:
            return 9.3
        elif 10 <= ppgoals < 12:
            return 9.5
        elif 12 <= ppgoals < 15:
            return 9.8
        else:
            return 10

    def __calculate_grade_ppassists(self, player_stat):
        if player_stat.games == 0:
            return 0
        ppa = (player_stat.powerPlayPoints - player_stat.powerPlayGoals)
        return -0.0015 * (ppa / player_stat.games * 82 - 60) ** 2 + 10

    def __calculate_grade_pppoints(self, player_stat):
        if player_stat.games == 0:
            return 4
        # return -0.0007 * (player_stat.points / player_stat.games * 82 - 80) ** 2 + 10
        pppoints = player_stat.powerPlayPoints / player_stat.games * 82

        if pppoints < 5:
            return 5
        elif 5 <= pppoints < 10:
            return 7.5
        elif 10 <= pppoints < 15:
            return 8
        elif 15 <= pppoints < 20:
            return 8.5
        elif 20 <= pppoints < 25:
            return 9
        elif 25 <= pppoints < 30:
            return 9.5
        elif 30 <= pppoints < 35:
            return 9.7
        elif 35 <= pppoints < 40:
            return 9.9
        else:
            return 10

    def __calculate_grade_shotPct(self, player_stat):
        shotPct = player_stat.shotPct
        return 0.85 if shotPct <= 0.0 or not None else (shotPct / 100) ** -1 * 0.1

    def __calculate_grade_toi(self, player_stat):
        toi = TimeConverter.convert_string_to_total_seconds(player_stat.timeOnIcePerGame)
        if toi < 15 * 60:
            return 7
        elif 15 * 60 <= toi < 17 * 60:
            return 8
        elif 17 * 60 <= toi < 18 * 60:
            return 8.5
        elif 18 * 60 <= toi < 20 * 60:
            return 9
        elif 20 * 60 <= toi < 23 * 60:
            return 9.5
        elif 23 * 60 <= toi < 25 * 60:
            return 9.8
        else:
            return 10

    def __calculate_grade_pptoi(self, player_stat):
        pptoi = TimeConverter.convert_string_to_total_seconds(player_stat.powerPlayTimeOnIcePerGame)
        grade = pptoi / (2 * 60)
        return grade if (grade > 0.5) else 0.5

    def __calculate_grade_evtoi(self, player_stat):
        evtoi = TimeConverter.convert_string_to_total_seconds(player_stat.evenTimeOnIcePerGame)
        grade = evtoi / (20 * 60)
        return grade if (grade > 0.5) else 0.5
