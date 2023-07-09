from server.commons.fantasygrade.model.fantasy_forward_grade import FantasyForwardGrade


class FantasyForwardGradeHelper:

    def __init__(self, percentile_stats_object):
        self.percentile_stats_object = percentile_stats_object

    def getForwardGrade(self, skaterFullName, player_stat):
        grade = 0

        forward_player = FantasyForwardGrade(player_stat, self.percentile_stats_object)

        # grade += forward_player.grade_g * forward_player.shotPctIndex
        grade += forward_player.grade_g * forward_player.game_played_scale * 300
        grade += forward_player.grade_a * forward_player.game_played_scale * 350
        grade += forward_player.grade_p * 630
        grade += forward_player.grade_p * forward_player.game_played_scale
        grade += forward_player.grade_ppg * 75
        grade += forward_player.grade_ppp * 575
        grade += forward_player.grade_pptoi * 2
        grade += forward_player.grade_toi
        grade += forward_player.grade_sog * 75
        grade += forward_player.grade_hits
        grade += forward_player.grade_blk
        grade = grade / 2000

        self.__print_player_stats(skaterFullName, forward_player, grade)
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
