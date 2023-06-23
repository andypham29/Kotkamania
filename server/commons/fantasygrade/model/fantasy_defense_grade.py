from server.commons.helper.time_converter import TimeConverter


class FantasyDefenseGrade:

    def __init__(self, player_stat, percentile_stats_object=None):
        self.percentile_stats_object = percentile_stats_object
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

    def get_percentile_by_stat(self, stat, stat_name):
        try:
            percentile_stat_list = self.percentile_stats_object.get(stat_name)
        except:
            return 0
        return min(range(len(percentile_stat_list)), key=lambda i: abs(percentile_stat_list[i] - stat))

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
            return 30
        # return -0.003 * (player_stat.goals / player_stat.games * 82 - 30) ** 2 + 10
        goal = player_stat.goals / player_stat.games
        return self.get_percentile_by_stat(goal, "goal")

    def __calculate_grade_assists(self, player_stat):
        if player_stat.games == 0:
            return 50
        # return -0.0015 * (player_stat.assists / player_stat.games * 82 - 50) ** 2 + 10
        assists = player_stat.assists / player_stat.games
        return self.get_percentile_by_stat(assists, "assist")

    def __calculate_grade_points(self, player_stat):
        if player_stat.games == 0:
            return 50
        # return -0.0007 * (player_stat.points / player_stat.games * 82 - 100) ** 2 + 10
        points = player_stat.points / player_stat.games
        return self.get_percentile_by_stat(points, "point")

    def __calculate_grade_ppgoals(self, player_stat):
        if player_stat.games == 0:
            return 60
        # return -0.003 * (player_stat.powerPlayGoals / player_stat.games * 82 - 40) ** 2 + 10
        ppgoals = player_stat.powerPlayGoals / player_stat.games * 82
        if ppgoals < 4:
            return 70
        elif 4 <= ppgoals < 6:
            return 80
        elif 6 <= ppgoals < 8:
            return 88
        elif 8 <= ppgoals < 10:
            return 93
        elif 10 <= ppgoals < 12:
            return 95
        elif 12 <= ppgoals < 15:
            return 98
        else:
            return 100

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
            return 70
        elif 5 <= pppoints < 10:
            return 75
        elif 10 <= pppoints < 15:
            return 80
        elif 15 <= pppoints < 20:
            return 85
        elif 20 <= pppoints < 25:
            return 9
        elif 25 <= pppoints < 30:
            return 95
        elif 30 <= pppoints < 35:
            return 97
        elif 35 <= pppoints < 40:
            return 99
        else:
            return 100

    def __calculate_grade_shotPct(self, player_stat):
        shotPct = player_stat.shotPct
        return 0.85 if shotPct <= 0.0 or not None else (shotPct / 100) ** -1 * 0.1

    def __calculate_grade_toi(self, player_stat):
        if player_stat.games == 0:
            return 0
        toi = TimeConverter.convert_string_to_total_seconds(player_stat.timeOnIcePerGame) / player_stat.games
        return self.get_percentile_by_stat(toi, "toi")

    def __calculate_grade_pptoi(self, player_stat):
        if player_stat.games == 0:
            return 0
        pptoi = TimeConverter.convert_string_to_total_seconds(player_stat.powerPlayTimeOnIcePerGame) / player_stat.games
        return self.get_percentile_by_stat(pptoi, "pptoi")

    def __calculate_grade_evtoi(self, player_stat):
        if player_stat.games == 0:
            return 0
        evtoi = TimeConverter.convert_string_to_total_seconds(player_stat.evenTimeOnIcePerGame) / player_stat.games
        return self.get_percentile_by_stat(evtoi, "evtoi")

    def __calculate_grade_sog(self, player_stat):
        if player_stat.games == 0:
            return 0
        sog = player_stat.shots / player_stat.games
        return self.get_percentile_by_stat(sog, "shot")

    def __calculate_grade_hits(self, player_stat):
        if player_stat.games == 0:
            return 0
        hits = player_stat.hits / player_stat.games
        return self.get_percentile_by_stat(hits, "hit")

    def __calculate_grade_blk(self, player_stat):
        if player_stat.games == 0:
            return 0
        blk = player_stat.blocked / player_stat.games
        return self.get_percentile_by_stat(blk, "block")

    def __calculate_grade_pktoi(self, player_stat):
        toi = TimeConverter.convert_string_to_total_seconds(player_stat.shortHandedTimeOnIcePerGame)
        if toi < 30:
            return 10
        elif 30 <= toi < 45:
            return 50
        elif 45 <= toi < 1 * 60:
            return 60
        elif 1 * 60 <= toi < 1 * 60 + 30:
            return 70
        elif 1 * 60 + 15 <= toi < 2 * 60:
            return 80
        elif 2 * 60 <= toi < 2 * 60 + 30:
            return 90
        else:
            return 100
