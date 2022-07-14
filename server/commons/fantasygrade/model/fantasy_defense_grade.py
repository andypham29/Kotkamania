from server.commons.helper.time_converter import TimeConverter


class FantasyDefenseGrade:

    def __init__(self, player_stat):
        self.grade_g = self.__calculate_grade_goals(player_stat)
        self.grade_a = self.__calculate_grade_assists(player_stat)
        self.grade_p = self.__calculate_grade_points(player_stat)
        self.grade_ppg = self.__calculate_grade_ppgoals(player_stat)
        self.grade_ppa = self.__calculate_grade_ppassists(player_stat)
        self.grade_ppp = self.__calculate_grade_points(player_stat)
        self.grade_shotPct = self.__calculate_grade_shotPct(player_stat)
        self.grade_toi = self.__calculate_grade_toi(player_stat)
        self.grade_pptoi = self.__calculate_grade_pptoi(player_stat)
        self.grade_evtoi = self.__calculate_grade_evtoi(player_stat)
        self.grade_pktoi = self.__calculate_grade_pktoi(player_stat)
        self.grade_shotAttempt = self.__calculate_grade_shotAttempt(player_stat)
        self.shotPctIndex = self.shotPctIndex(player_stat)
        self.game_played_scale = self.__scale_by_games_played(player_stat)
        self.grade_sog = self.__calculate_grade_sog(player_stat)
        self.grade_hits = self.__calculate_grade_hits(player_stat)
        self.grade_blk = self.__calculate_grade_blk(player_stat)

    def shotPctIndex(self, player_stat=None):
        grade_toi = self.__calculate_grade_toi(player_stat)
        grade_pptoi = self.__calculate_grade_pptoi(player_stat)
        grade_evtoi = self.__calculate_grade_evtoi(player_stat)
        grade_shotAttempt = self.__calculate_grade_shotAttempt(player_stat)

        return round(-0.1875 * ((grade_toi + grade_pptoi + grade_evtoi + grade_shotAttempt) / 5) ** 3 + 1.2, 2)

    def __scale_by_games_played(self, player_stat):
        gp = player_stat.games
        if gp < 10:
            return 0.75
        elif 10 <= gp < 20:
            return 0.8
        elif 20 <= gp < 30:
            return 0.9
        elif 30 <= gp < 40:
            return 0.95
        else:
            return 1

    def __calculate_grade_shotAttempt(self, player_stat):
        if player_stat.games == 0:
            return 0
        shotPctIndex = round(-0.055 * (player_stat.shotPct / 12) ** 3 + 1.05, 2)
        return ((player_stat.shots / player_stat.games) ** shotPctIndex) / 2

    def __calculate_grade_goals(self, player_stat):
        if player_stat.games == 0:
            return 3
        # return -0.003 * (player_stat.goals / player_stat.games * 82 - 30) ** 2 + 10
        goal = player_stat.goals / player_stat.games * 82
        if goal < 3:
            return 3
        elif 3 <= goal < 5:
            return 4
        elif 5 <= goal < 8:
            return 5
        elif 8 <= goal < 10:
            return 6
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
            return 7
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
            return 8.8
        elif 20 * 60 <= toi < 23 * 60:
            return 9
        elif 23 * 60 <= toi < 25 * 60:
            return 9.5
        else:
            return 10

    def __calculate_grade_pptoi(self, player_stat):
        pptoi = TimeConverter.convert_string_to_total_seconds(player_stat.powerPlayTimeOnIcePerGame)
        if pptoi < 30:
            return 7.5
        elif 30 <= pptoi < 60:
            return 8
        elif 60 <= pptoi < 2 * 60:
            return 8.2
        elif 2 * 60 <= pptoi < 2 * 60 + 30:
            return 8.5
        elif 1 * 60 <= pptoi < 2 * 60 + 30:
            return 8.8
        elif 2 * 60 + 30 <= pptoi < 3 * 60:
            return 9
        elif 3 * 60 <= pptoi < 3 * 60 + 30:
            return 9.5
        else:
            return 10

    def __calculate_grade_evtoi(self, player_stat):
        evtoi = TimeConverter.convert_string_to_total_seconds(player_stat.evenTimeOnIcePerGame)
        if evtoi < 15 * 60:
            return 7.5
        elif 15 * 60 <= evtoi < 17 * 60:
            return 8
        elif 17 * 60 <= evtoi < 18 * 60:
            return 8.5
        elif 18 * 60 <= evtoi < 20 * 60:
            return 9
        else:
            return 10

    def __calculate_grade_sog(self, player_stat):
        if player_stat.games == 0:
            return 2
        sog = player_stat.shots / player_stat.games
        if sog < 1.06:
            return 3
        elif 1.06 <= sog < 1.18:
            return 4
        elif 1.18 <= sog < 1.32:
            return 5
        elif 1.32 <= sog < 1.48:
            return 6
        elif 1.48 <= sog < 1.73:
            return 7
        elif 1.73 <= sog < 1.99:
            return 8
        elif 1.99 <= sog < 2.35:
            return 9
        else:
            return 10

    def __calculate_grade_hits(self, player_stat):
        if player_stat.games == 0:
            return 2
        hits = player_stat.hits / player_stat.games
        if hits < 0.89:
            return 3
        elif 0.89 <= hits < 1.04:
            return 4
        elif 1.04 <= hits < 1.26:
            return 5
        elif 1.26 <= hits < 1.48:
            return 6
        elif 1.48 <= hits < 1.75:
            return 7
        elif 1.75 <= hits < 2.00:
            return 8
        elif 2.00 <= hits < 2.39:
            return 9
        else:
            return 10

    def __calculate_grade_blk(self, player_stat):
        if player_stat.games == 0:
            return 2
        blk = player_stat.blocked / player_stat.games
        if blk < 1.093:
            return 3
        elif 1.093 <= blk < 1.193:
            return 4
        elif 1.193 <= blk < 1.295:
            return 5
        elif 1.295 <= blk < 1.405:
            return 6
        elif 1.405 <= blk < 1.559:
            return 7
        elif 1.559 <= blk < 1.727:
            return 8
        elif 1.727 <= blk < 1.926:
            return 9
        else:
            return 10

    def __calculate_grade_pktoi(self, player_stat):
        toi = TimeConverter.convert_string_to_total_seconds(player_stat.shortHandedTimeOnIcePerGame)
        if toi < 30:
            return 1
        elif 30 <= toi < 45:
            return 5
        elif 45 <= toi < 1 * 60:
            return 6
        elif 1 * 60 <= toi < 1 * 60 + 30:
            return 7
        elif 1 * 60 + 15 <= toi < 2 * 60:
            return 8
        elif 2 * 60 <= toi < 2 * 60 + 30:
            return 9
        else:
            return 10