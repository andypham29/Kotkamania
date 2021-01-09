import datetime


class FantasyForwardGradeHelper:

    def __init__(self):
        pass

    def getForwardGrade(self, skaterFullName, player_stat):
        grade = 0

        grade_g = self.__calculate_grade_goals(player_stat)
        grade_a = self.__calculate_grade_assists(player_stat)
        grade_p = self.__calculate_grade_points(player_stat)
        grade_atp = self.__calculate_grade_actual_total_points(player_stat)
        grade_ppg = self.__calculate_grade_ppgoals(player_stat)
        grade_ppa = self.__calculate_grade_ppassists(player_stat)
        grade_ppp = self.__calculate_grade_points(player_stat)
        grade_shotPct = self.__calculate_grade_shotPct(player_stat)
        grade_toi = self.__calculate_grade_toi(player_stat)
        grade_pptoi = self.__calculate_grade_pptoi(player_stat)
        grade_evtoi = self.__calculate_grade_evtoi(player_stat)

        index = self.shotPctIndex(player_stat)
        scale = self.__scale_by_games_played(player_stat)

        # general = ((grade_ppg * index + grade_ppa + grade_ppp + grade_shotPct) + (
        #         (grade_toi + grade_pptoi + grade_evtoi) * index / 3))
        grade += grade_g * index * 0.225 + grade_g + grade_a * 1.75 + grade_p * 4 + grade_atp * scale + grade_ppg + grade_ppp * 0.725 * grade_pptoi
        grade = grade * scale
        print(skaterFullName, grade_g, grade_a, grade_p, grade_atp, grade_ppg, grade_ppp, grade)
        # print(
        #     f"{skaterFullName}[{round(index, 2)}]: \t\tGEN:{round(general, 2)}\tPP:{round(grade_toi, 2)}\tEV:{round(grade_evtoi, 2)} {player_stat.assists / player_stat.games * 82}\t{grade_p} {player_stat.points / player_stat.games * 82}")
        # grade += (grade_g * index + grade_a + grade_p + general * grade_evtoi * grade_pptoi * scale) / 50 * 100

        return round(grade, 2)

    def shotPctIndex(self, player_stat):
        index = round(-0.055 * (player_stat.shotPct / 12) ** 3 + 1.05, 2)
        return index if index > 0 else 0.95

    def __scale_by_games_played(self, player_stat):
        gp = player_stat.games
        if gp < 10:
            return 0.5
        elif 10 <= gp < 20:
            return 0.88
        elif 20 <= gp < 30:
            return 0.93
        elif 30 <= gp < 40:
            return 0.97
        else:
            return 1

    def __calculate_grade_goals(self, player_stat):
        # return -0.003 * (player_stat.goals / player_stat.games * 82 - 70) ** 2 + 10
        goal = player_stat.goals / player_stat.games * 82
        if goal < 10:
            return 7
        elif 10 <= goal < 15:
            return 8
        elif 15 <= goal < 20:
            return 8.5
        elif 20 <= goal < 25:
            return 9
        elif 25 <= goal < 30:
            return 9.1
        elif 30 <= goal < 35:
            return 9.3
        elif 35 <= goal < 40:
            return 9.5
        elif 40 <= goal < 45:
            return 9.8
        else:
            return 10

    def __calculate_grade_assists(self, player_stat):
        # return -0.0015 * (player_stat.assists / player_stat.games * 82 - 100) ** 2 + 10
        assists = player_stat.assists / player_stat.games * 82
        if assists < 15:
            return 7
        elif 15 <= assists < 25:
            return 7.5
        elif 25 <= assists < 35:
            return 8.8
        elif 35 <= assists < 40:
            return 9.5
        elif 40 <= assists < 45:
            return 9.8
        else:
            return 10

    def __calculate_grade_points(self, player_stat):
        # return -0.0007 * (player_stat.points / player_stat.games * 82 - 150) ** 2 + 10
        points = player_stat.points / player_stat.games * 82
        if points < 20:
            return 6
        elif 20 <= points < 30:
            return 7
        elif 30 <= points < 40:
            return 7.5
        elif 40 <= points < 50:
            return 8
        elif 50 <= points < 60:
            return 8.5
        elif 60 <= points < 70:
            return 8.8
        elif 70 <= points < 80:
            return 9
        elif 80 <= points < 90:
            return 9.5
        elif 90 <= points < 95:
            return 9.8
        else:
            return 10

    def __calculate_grade_actual_total_points(self, player_stat):
        # return -0.0007 * (player_stat.points / player_stat.games * 82 - 100) ** 2 + 10
        points = player_stat.points
        if points < 10:
            return 5
        elif 10 <= points < 20:
            return 7
        elif 20 <= points < 30:
            return 7.5
        elif 30 <= points < 40:
            return 8
        elif 40 <= points < 50:
            return 8.5
        elif 50 <= points < 55:
            return 9
        elif 55 <= points < 60:
            return 9.3
        elif 60 <= points < 65:
            return 9.5
        elif 65 <= points < 70:
            return 9.8
        else:
            return 10

    def __calculate_grade_ppgoals(self, player_stat):
        # return player_stat.powerPlayGoals / player_stat.games * 8
        ppgoals = player_stat.powerPlayGoals / player_stat.games * 82
        if ppgoals < 4:
            return 7
        elif 4 <= ppgoals < 7:
            return 8
        elif 7 <= ppgoals < 10:
            return 8.5
        elif 10 <= ppgoals < 12:
            return 8.8
        elif 12 <= ppgoals < 15:
            return 9
        elif 15 <= ppgoals < 18:
            return 9.3
        elif 18 <= ppgoals < 20:
            return 9.5
        else:
            return 10

    def __calculate_grade_ppassists(self, player_stat):
        return (player_stat.powerPlayPoints - player_stat.powerPlayGoals) / player_stat.games * 6

    def __calculate_grade_pppoints(self, player_stat):
        # return player_stat.powerPlayPoints / player_stat.games * 10
        pppoints = player_stat.powerPlayPoints / player_stat.games * 82

        if pppoints < 5:
            return 7
        elif 5 <= pppoints < 10:
            return 8
        elif 10 <= pppoints < 15:
            return 8.5
        elif 15 <= pppoints < 20:
            return 9
        elif 20 <= pppoints < 25:
            return 9.3
        elif 25 <= pppoints < 30:
            return 9.5
        elif 30 <= pppoints < 35:
            return 9.8
        elif 35 <= pppoints < 40:
            return 9.9
        else:
            return 10

    def __calculate_grade_shotPct(self, player_stat):
        shotPct = player_stat.shotPct
        try:
            grade = (shotPct / 100) ** -1 * 0.1 if shotPct > 0 or not None else 0.85
        except:
            grade = 0
        finally:
            return grade

    def __calculate_grade_toi(self, player_stat):
        toi = datetime.datetime.strptime(player_stat.timeOnIcePerGame, '%M:%S')
        grade = (toi.minute * 60 + toi.second) / (15 * 60)
        return grade if (grade > 0.5) else 0.5

    def __calculate_grade_pptoi(self, player_stat):
        pptoi = datetime.datetime.strptime(player_stat.powerPlayTimeOnIcePerGame, '%M:%S')
        grade = (pptoi.minute * 60 + pptoi.second) / (2.5 * 60)
        return grade if (grade > 0.5) else 0.5

    def __calculate_grade_evtoi(self, player_stat):
        evtoi = datetime.datetime.strptime(player_stat.evenTimeOnIcePerGame, '%M:%S')
        grade = (evtoi.minute * 60 + evtoi.second) / (13 * 60)
        return grade if (grade > 0.5) else 0.5
