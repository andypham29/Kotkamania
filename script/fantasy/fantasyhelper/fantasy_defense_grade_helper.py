import datetime


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

        shoot = self.shotPctIndex(player_stat.shotPct)
        general = ((grade_ppg * shoot + grade_ppa + grade_ppp + grade_shotPct) + (
                (grade_toi + grade_pptoi + grade_evtoi) * shoot / 3) * 0.8)

        print(
            f"{skaterFullName}[{round(shoot, 2)}]: \t\tGEN:{round(general, 2)}\tPP:{round(grade_toi, 2)}\tEV:{round(grade_evtoi, 2)} "
            f"{round(player_stat.assists / player_stat.games * 82, 2)}\t{grade_p} {round(player_stat.points / player_stat.games * 82, 2)}")
        grade += (grade_g * shoot + grade_a + grade_p + general) / 42 * 100

        return round(grade, 2)

    def shotPctIndex(self, shotPct):
        return round(-0.055 * (shotPct / 12) ** 3 + 1.05, 2)

    def __calculate_grade_goals(self, player_stat):
        return -0.003 * (player_stat.goals / player_stat.games * 82 - 60) ** 2 + 10

    def __calculate_grade_assists(self, player_stat):
        return -0.0015 * (player_stat.assists / player_stat.games * 82 - 80) ** 2 + 10

    def __calculate_grade_points(self, player_stat):
        return -0.0007 * (player_stat.points / player_stat.games * 82 - 120) ** 2 + 10

    def __calculate_grade_ppgoals(self, player_stat):
        return player_stat.powerPlayGoals / player_stat.games * 8

    def __calculate_grade_ppassists(self, player_stat):
        return (player_stat.powerPlayPoints - player_stat.powerPlayGoals) / player_stat.games * 6

    def __calculate_grade_pppoints(self, player_stat):
        return player_stat.powerPlayPoints / player_stat.games * 10

    def __calculate_grade_shotPct(self, player_stat):
        shotPct = player_stat.shotPct
        return (shotPct / 100) ** -1 * 0.1 if shotPct > 0 or not None else 0.85

    def __calculate_grade_toi(self, player_stat):
        toi = datetime.datetime.strptime(player_stat.timeOnIcePerGame, '%M:%S')
        return (toi.minute * 60 + toi.second) / (20 * 60)

    def __calculate_grade_pptoi(self, player_stat):
        pptoi = datetime.datetime.strptime(player_stat.powerPlayTimeOnIcePerGame, '%M:%S')
        return (pptoi.minute * 60 + pptoi.second) / (3 * 60)

    def __calculate_grade_evtoi(self, player_stat):
        evtoi = datetime.datetime.strptime(player_stat.evenTimeOnIcePerGame, '%M:%S')
        return (evtoi.minute * 60 + evtoi.second) / (15 * 60)
