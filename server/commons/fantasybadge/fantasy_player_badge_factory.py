from server.commons.fantasybadge.model.fantasy_player_badge import FantasyPlayerBadge
from server.commons.fantasygrade.model.fantasy_defense_grade import FantasyDefenseGrade
from server.commons.fantasygrade.model.fantasy_forward_grade import FantasyForwardGrade


class FantasyPlayerBadgeFactory:

    def get_badge_for_forward(self, player_stat):
        player = FantasyForwardGrade(player_stat)
        return FantasyPlayerBadge(scoring=self.__get_scoring_badge(player),
                                  playmaking=self.__get_playmaking_badge(player),
                                  defense=self.__get_defense_badge(player),
                                  powerplay=self.__get_powerplay_badge(player),
                                  intangible=self.__get_intangible_badge(player))

    def get_badge_for_defense(self, player_stat):
        player = FantasyDefenseGrade(player_stat)
        return FantasyPlayerBadge(scoring=self.__get_scoring_badge(player),
                                  playmaking=self.__get_playmaking_badge(player),
                                  defense=self.__get_defense_badge(player),
                                  powerplay=self.__get_powerplay_badge(player),
                                  intangible=self.__get_intangible_badge(player))

    def __get_scoring_badge(self, player):
        badge = player.grade_g * 5 + player.grade_sog * 3 + player.grade_ppp + player.grade_ppg + player.grade_pptoi * 2
        return round(badge / 12, 2)

    def __get_playmaking_badge(self, player):
        badge = player.grade_a * 5 + player.grade_ppp + player.grade_ppa + player.grade_pptoi * 2
        return round(badge / 9, 2)

    def __get_defense_badge(self, player):
        badge = player.grade_evtoi * 3 + player.grade_blk + player.grade_pktoi * 6
        return round(badge / 10, 2)

    def __get_powerplay_badge(self, player):
        badge = player.grade_ppp * 4 + player.grade_ppa + player.grade_ppg + player.grade_pptoi * 4
        return round(badge / 10, 2)

    def __get_intangible_badge(self, player):
        badge = player.grade_sog * 2 + player.grade_hits * 4 + player.grade_blk * 4
        return round(badge / 10, 2)
