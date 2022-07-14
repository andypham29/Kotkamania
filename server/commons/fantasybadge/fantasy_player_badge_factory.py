from server.commons.fantasybadge.model.fantasy_player_badge import FantasyPlayerBadge
from server.commons.fantasygrade.model.fantasy_defense_grade import FantasyDefenseGrade
from server.commons.fantasygrade.model.fantasy_forward_grade import FantasyForwardGrade


class FantasyPlayerBadgeFactory:

    def get_badge_for_skater(self, player_stat, position):
        if position == "D":
            return self.get_badge_for_defense(player_stat)
        else:
            return self.get_badge_for_forward(player_stat)

    def get_badge_for_forward(self, player_stat):
        player = FantasyForwardGrade(player_stat)
        return FantasyPlayerBadge(scoring=self.__get_scoring_badge(player),
                                  playmaking=self.__get_playmaking_badge(player),
                                  defense=self.__get_defense_badge(player),
                                  powerplay=self.__get_powerplay_badge(player),
                                  intangibles=self.__get_intangibles_badge(player))

    def get_badge_for_defense(self, player_stat):
        player = FantasyDefenseGrade(player_stat)
        return FantasyPlayerBadge(scoring=self.__get_scoring_badge(player),
                                  playmaking=self.__get_playmaking_badge(player),
                                  defense=self.__get_defense_badge(player),
                                  powerplay=self.__get_powerplay_badge(player),
                                  intangibles=self.__get_intangibles_badge(player))

    def __get_scoring_badge(self, player):
        badge = player.grade_g * 5 + player.grade_sog * 3 + player.grade_ppp + player.grade_ppg * 2 + player.grade_pptoi * 2
        return round(badge / 12, 2)

    def __get_playmaking_badge(self, player):
        badge = player.grade_a * 5 + player.grade_ppp + player.grade_ppa * 2 + player.grade_pptoi * 2
        return round(badge / 10, 2)

    def __get_defense_badge(self, player):
        badge = player.grade_evtoi * 2 + player.grade_blk * 3 + player.grade_pktoi * 5
        return round(badge / 10, 2)

    def __get_powerplay_badge(self, player):
        badge = player.grade_ppp * 4 + player.grade_ppa + player.grade_ppg + player.grade_pptoi * 4
        return round(badge / 10, 2)

    def __get_intangibles_badge(self, player):
        badge = player.grade_sog * 3 + player.grade_hits * 5 + player.grade_blk * 4
        return round(badge / 12, 2)
