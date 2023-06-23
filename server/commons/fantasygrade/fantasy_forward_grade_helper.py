from server.commons.fantasygrade.model.fantasy_forward_grade import FantasyForwardGrade


class FantasyForwardGradeHelper:

    def __init__(self, percentile_stats_object):
        self.percentile_stats_object = percentile_stats_object

    def getForwardGrade(self, skaterFullName, player_stat):
        grade = 0

        forward_player = FantasyForwardGrade(player_stat, self.percentile_stats_object)

        grade += forward_player.grade_g * forward_player.shotPctIndex
        grade += forward_player.grade_g * forward_player.game_played_scale * 9
        grade += forward_player.grade_a * forward_player.game_played_scale * 10
        grade += forward_player.grade_p * 20
        grade += forward_player.grade_p * forward_player.game_played_scale
        grade += forward_player.grade_ppg
        grade += forward_player.grade_ppp * 5
        grade += forward_player.grade_pptoi * 5
        grade += forward_player.grade_toi
        grade += forward_player.grade_sog * 5
        grade += forward_player.grade_hits * 2
        grade += forward_player.grade_blk
        grade = grade / 5.9

        print(skaterFullName, forward_player.grade_g, forward_player.grade_a, forward_player.grade_p,
              forward_player.grade_ppg, forward_player.grade_ppp, grade)

        return round(grade, 2)
