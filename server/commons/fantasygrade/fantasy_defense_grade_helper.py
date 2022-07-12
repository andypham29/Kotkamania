from server.commons.fantasygrade.model.fantasy_defense_grade import FantasyDefenseGrade


class FantasyDefenseGradeHelper:

    def __init__(self):
        pass

    def getDefenseGrade(self, skaterFullName, player_stat):
        grade = 0

        defense_player = FantasyDefenseGrade(player_stat)

        grade += defense_player.grade_g * defense_player.game_played_scale
        grade += defense_player.grade_a * defense_player.game_played_scale
        grade += defense_player.grade_p * 2
        grade += defense_player.grade_ppg
        grade += defense_player.grade_ppp
        grade += defense_player.grade_pptoi
        grade += defense_player.grade_ppp * 2
        grade += defense_player.grade_toi * 3
        print(skaterFullName, defense_player.grade_g, defense_player.grade_a, defense_player.grade_p,
              defense_player.grade_ppg, defense_player.grade_ppp, defense_player.grade_pptoi)

        grade = grade / 12 * 10
        return round(grade, 2)
