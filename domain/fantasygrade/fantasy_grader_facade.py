class FantasyGraderFacade:
    def __init__(self, fantasy_grader):
        self.fantasy_grader = fantasy_grader

    def grade_player(self, player_stats):
        return self.fantasy_grader.grade(player_stats)