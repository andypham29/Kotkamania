from server.commons.fantasygrade.model.fantasy_defense_grade import FantasyDefenseGrade


class FantasyDefenseGradeHelper:

    def __init__(self, percentile_stats_object):
        self.percentile_stats_object = percentile_stats_object

    def getDefenseGrade(self, skaterFullName, player_stat):
        grade = 0

        defense_player = FantasyDefenseGrade(player_stat, self.percentile_stats_object)

        grade += defense_player.grade_g * defense_player.game_played_scale * 10
        grade += defense_player.grade_a * defense_player.game_played_scale * 10
        grade += defense_player.grade_p * 22
        grade += defense_player.grade_ppg
        grade += defense_player.grade_ppp * 5
        grade += defense_player.grade_pptoi
        grade += defense_player.grade_ppp * 2
        grade += defense_player.grade_toi * 3
        grade += defense_player.grade_sog * 3
        grade += defense_player.grade_hits * 5
        grade += defense_player.grade_blk * 7
        print(skaterFullName, defense_player.grade_g, defense_player.grade_a, defense_player.grade_p,
              defense_player.grade_ppg, defense_player.grade_ppp, defense_player.grade_pptoi)

        grade = grade / 6.9
        return round(grade, 2)
