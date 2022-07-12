from server.commons.fantasygrade.model.fantasy_forward_grade import FantasyForwardGrade


class FantasyForwardGradeHelper:

    def __init__(self):
        pass

    def getForwardGrade(self, skaterFullName, player_stat):
        grade = 0

        forward_player = FantasyForwardGrade(player_stat)

        grade += forward_player.grade_g * forward_player.shotPctIndex
        grade += forward_player.grade_g * forward_player.game_played_scale * 3
        grade += forward_player.grade_a * forward_player.game_played_scale * 4
        grade += forward_player.grade_p * 8.3
        grade += forward_player.grade_p * forward_player.game_played_scale
        grade += forward_player.grade_ppg
        grade += forward_player.grade_ppp * 0.525 * forward_player.grade_pptoi
        grade += forward_player.grade_toi
        grade = grade / 2

        print(skaterFullName, forward_player.grade_g, forward_player.grade_a, forward_player.grade_p,
              forward_player.grade_ppg, forward_player.grade_ppp, grade)

        return round(grade, 2)

