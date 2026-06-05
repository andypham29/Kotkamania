from domain.goaliestat.model.domain_goalie_stat import DomainGoalieStat


class GoalieStatService:

    def __init__(self):
        self.goalie_stat_repository = None

    def get_all_stats(self):
        return self.goalie_stat_repository.find_all()

    def get_stat_by_playerid(self, player_id: int):
        return self.goalie_stat_repository.find_by_player_id(player_id)