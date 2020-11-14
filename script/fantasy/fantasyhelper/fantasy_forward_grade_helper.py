import datetime


class FantasyForwardGradeHelper:

    def __init__(self):
        pass

    def getForwardGrade(self, player):
        grade = 0

        for player_stat in player.stats:
            toi = datetime.datetime.strptime(player_stat.stat.timeOnIcePerGame, '%M:%S')
            pptoi = datetime.datetime.strptime(player_stat.stat.powerPlayTimeOnIcePerGame, '%M:%S')
            evtoi = datetime.datetime.strptime(player_stat.stat.evenTimeOnIcePerGame, '%M:%S')

            grade_g = self.__calculate_grade_goals(player_stat)
            grade_a = (-0.0015 * (player_stat.stat.assists / player_stat.stat.games * 82 - 80) ** 2 + 10)
            grade_p = (-0.0007 * (player_stat.stat.points / player_stat.stat.games * 82 - 120) ** 2 + 10)
            grade_ppg = player_stat.stat.powerPlayGoals / player_stat.stat.games * 8
            grade_ppa = (
                                    player_stat.stat.powerPlayPoints - player_stat.stat.powerPlayGoals) / player_stat.stat.games * 6
            grade_ppp = player_stat.stat.powerPlayPoints / player_stat.stat.games * 10
            grade_shotPct = self.__calculate_grade_shotPct(player_stat)
            grade_toi = (toi.minute * 60 + toi.second) / (20 * 60)
            grade_pptoi = (pptoi.minute * 60 + pptoi.second) / (3 * 60)
            grade_evtoi = (evtoi.minute * 60 + evtoi.second) / (15 * 60)

            shoot = self.shotPctIndex(player_stat.stat.shotPct)
            general = ((grade_ppg * shoot + grade_ppa + grade_ppp + grade_shotPct) + (
                    (grade_toi + grade_pptoi + grade_evtoi) * shoot / 3) * 0.8)

            print(
                f"{player.fullName}[{round(shoot, 2)}]: \t\tGEN:{round(general, 2)}\tPP:{round(grade_toi, 2)}\tEV:{round(grade_evtoi, 2)} {player_stat.stat.assists / player_stat.stat.games * 82}\t{grade_p} {player_stat.stat.points / player_stat.stat.games * 82}")
            grade += (grade_g * shoot + grade_a + grade_p + general) / 42 * 100

        return round(grade, 2)

    def shotPctIndex(self, shotPct):
        return round(-0.055 * (shotPct / 12) ** 3 + 1.05, 2)

    def __calculate_grade_goals(self, player_stat):
        return -0.003 * (player_stat.stat.goals / player_stat.stat.games * 82 - 60) ** 2 + 10

    def __calculate_grade_assists(self, player_stat):
        return None

    def __calculate_grade_points(self, player_stat):
        return None

    def __calculate_grade_ppgoals(self, player_stat):
        return None

    def __calculate_grade_ppassists(self, player_stat):
        return None

    def __calculate_grade_pppoints(self, player_stat):
        return None

    def __calculate_grade_shotPct(self, player_stat):
        shotPct = player_stat.stat.shotPct
        return 1 if (shotPct <= 0.0 or None) else (shotPct / 100) ** -1 * 0.1

    def __calculate_grade_toi(self, player_stat):
        return None

    def __calculate_grade_pptoi(self, player_stat):
        return None

    def __calculate_grade(self, player_stat):
        return None

    def __calculate_grade(self, player_stat):
        return None
