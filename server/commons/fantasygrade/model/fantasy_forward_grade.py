from server.commons.helper.time_converter import TimeConverter


class FantasyForwardGrade:

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

    def shotPctIndex(self, player_stat):
        index = round(-0.055 * (player_stat.shotPct / 12) ** 3 + 1.05, 2)
        return index if index > 0 else 0.95

    def __scale_by_games_played(self, player_stat):
        gp = player_stat.games
        if gp < 10:
            return 0.88
        elif 10 <= gp < 20:
            return 0.9
        elif 20 <= gp < 30:
            return 0.93
        elif 30 <= gp < 40:
            return 0.97
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
        # return -0.003 * (player_stat.goals / player_stat.games * 82 - 70) ** 2 + 10
        goal = player_stat.goals / player_stat.games * 82
        if goal < 10:
            return 7
        elif 10 <= goal < 15:
            return 8
        elif 15 <= goal < 20:
            return 8.5
        elif 20 <= goal < 25:
            return 8.8
        elif 25 <= goal < 30:
            return 9
        elif 30 <= goal < 35:
            return 9.5
        elif 35 <= goal < 40:
            return 9.7
        elif 40 <= goal < 45:
            return 9.75
        elif 45 <= goal < 50:
            return 9.8
        elif 50 <= goal < 55:
            return 9.85
        elif 55 <= goal < 60:
            return 9.9
        else:
            return 10

    def __calculate_grade_assists(self, player_stat):
        if player_stat.games == 0:
            return 5
        # return -0.0015 * (player_stat.assists / player_stat.games * 82 - 100) ** 2 + 10
        assists = player_stat.assists / player_stat.games * 82
        if assists < 15:
            return 7
        elif 15 <= assists < 25:
            return 7.5
        elif 25 <= assists < 35:
            return 8
        elif 35 <= assists < 40:
            return 8.5
        elif 40 <= assists < 45:
            return 8.8
        elif 45 <= assists < 50:
            return 9.5
        elif 50 <= assists < 55:
            return 9.6
        elif 55 <= assists < 60:
            return 9.7
        elif 60 <= assists < 65:
            return 9.8
        elif 65 <= assists < 70:
            return 9.85
        elif 70 <= assists < 75:
            return 9.9
        else:
            return 10

    def __calculate_grade_points(self, player_stat):
        if player_stat.games == 0:
            return 5
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
            return 9
        elif 70 <= points < 80:
            return 9.3
        elif 80 <= points < 90:
            return 9.5
        elif 90 <= points < 95:
            return 9.8
        elif 95 <= points < 100:
            return 9.9
        else:
            return 10

    def __calculate_grade_ppgoals(self, player_stat):
        if player_stat.games == 0:
            return 6
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
        if player_stat.games == 0:
            return 0
        return (player_stat.powerPlayPoints - player_stat.powerPlayGoals) / player_stat.games * 6

    def __calculate_grade_pppoints(self, player_stat):
        if player_stat.games == 0:
            return 6
        # return player_stat.powerPlayPoints / player_stat.games * 10
        pppoints = player_stat.powerPlayPoints / player_stat.games * 82

        if pppoints < 5:
            return 7
        elif 5 <= pppoints < 10:
            return 8
        elif 10 <= pppoints < 15:
            return 8.5
        elif 15 <= pppoints < 20:
            return 8.8
        elif 20 <= pppoints < 25:
            return 9
        elif 25 <= pppoints < 30:
            return 9.3
        elif 30 <= pppoints < 35:
            return 9.6
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
        toi = TimeConverter.convert_string_to_total_seconds(player_stat.timeOnIcePerGame)
        if toi < 15 * 60:
            return 7
        elif 15 * 60 <= toi < 17 * 60:
            return 8
        elif 17 * 60 <= toi < 20 * 60:
            return 9
        elif 20 * 60 <= toi < 25 * 60:
            return 10
        else:
            return 10.5

    def __calculate_grade_pptoi(self, player_stat):
        pptoi = TimeConverter.convert_string_to_total_seconds(player_stat.powerPlayTimeOnIcePerGame)
        grade = pptoi / (2.5 * 60)
        return grade if (grade > 0.5) else 0.5

    def __calculate_grade_evtoi(self, player_stat):
        evtoi = TimeConverter.convert_string_to_total_seconds(player_stat.evenTimeOnIcePerGame)
        grade = evtoi / (13 * 60)
        return grade if (grade > 0.5) else 0.5

    def __calculate_grade_sog(self, player_stat):
        if player_stat.games == 0:
            return 2
        sog = player_stat.shots / player_stat.games
        if sog < 1.392:
            return 3
        elif 1.392 <= sog < 1.573:
            return 4
        elif 1.573 <= sog < 1.734:
            return 5
        elif 1.734 <= sog < 2.015:
            return 6
        elif 2.015 <= sog < 2.278:
            return 7
        elif 2.278 <= sog < 2.632:
            return 8
        elif 2.632 <= sog < 2.996:
            return 9
        else:
            return 10

    def __calculate_grade_hits(self, player_stat):
        if player_stat.games == 0:
            return 2
        hits = player_stat.hits / player_stat.games
        if hits < 0.716:
            return 3
        elif 0.716 <= hits < 0.890:
            return 4
        elif 0.890 <= hits < 1.059:
            return 5
        elif 1.059 <= hits < 1.239:
            return 6
        elif 1.239 <= hits < 1.424:
            return 7
        elif 1.424 <= hits < 1.859:
            return 8
        elif 1.859 <= hits < 2.324:
            return 9
        else:
            return 10

    def __calculate_grade_blk(self, player_stat):
        if player_stat.games == 0:
            return 2
        blk = player_stat.blk / player_stat.games
        if blk < 0.332:
            return 3
        elif 0.332 <= blk < 0.378:
            return 4
        elif 0.378 <= blk < 0.420:
            return 5
        elif 0.420 <= blk < 0.463:
            return 6
        elif 0.463 <= blk < 0.545:
            return 7
        elif 0.545 <= blk < 0.617:
            return 8
        elif 0.617 <= blk < 0.7014:
            return 9
        else:
            return 10

    def __calculate_grade_pktoi(self, player_stat):
        toi = TimeConverter.convert_string_to_total_seconds(player_stat.timeOnIcePerGame)
        if toi < 30:
            return 4
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