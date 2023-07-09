from server.commons.fantasygrade.model.fantasy_defense_grade import FantasyDefenseGrade


class FantasyDefenseGradeHelper:

    def __init__(self, percentile_stats_object):
        self.percentile_stats_object = percentile_stats_object

    def getDefenseGrade(self, skaterFullName, player_stat):
        grade = 0

        defense_player = FantasyDefenseGrade(player_stat, self.percentile_stats_object)

        grade += defense_player.grade_g * defense_player.game_played_scale * 1.025 * 100
        grade += defense_player.grade_a * defense_player.game_played_scale * 1.025 * 400
        grade += defense_player.grade_p * 1.025 * 755
        grade += defense_player.grade_ppg * 1.025 * 50
        grade += defense_player.grade_pptoi * 1.025 * 3
        grade += defense_player.grade_ppp * 1.025 * 630
        grade += defense_player.grade_toi * 2
        grade += defense_player.grade_sog * 1.025 * 50
        grade += defense_player.grade_hits * 5
        grade += defense_player.grade_blk * 5

        grade = grade / 2000
        self.__print_player_stats(skaterFullName, defense_player, grade)
        return round(grade, 2)

    def __print_player_stats(self, skaterFullName, player, grade):
        print(skaterFullName,
              "\tgrade_g:", player.grade_g,
              "\tgrade_a:", player.grade_a,
              "\tgrade_p:", player.grade_p,
              "\tgrade_ppg:", player.grade_ppg,
              "\tgrade_ppp:", player.grade_ppp,
              "\tgrade_pptoi:", player.grade_pptoi,
              "\tgrade_sog:", player.grade_sog,
              "\tgrade_hit:", player.grade_hits,
              "\tgrade_blk:", player.grade_blk,
              "\tgrade: ", grade)