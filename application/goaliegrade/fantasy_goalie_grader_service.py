from application.goaliestats.model.goalie_stat import GoalieStat

class FantasyGoalieGraderService:

    def __init__(self):
        pass

    def grade_goalie(self, g: GoalieStat) -> float:
        """
        Compute a simple goalie grade using key performance stats.
        Returns a score typically between 0 and 100.
        """

        save_pct = g.savePct or 0
        gaa = g.goalsAgainstAverage or 0
        wins = g.wins or 0
        shutouts = g.shutouts or 0
        shots_against = g.shotsAgainst or 0
        losses = g.losses or 0
        ot_losses = g.otLosses or 0

        score = (
                (save_pct * 50)
                - (gaa * 5)
                + (wins * 2)
                + (shutouts * 3)
                + (shots_against * 0.01)
                - (losses * 1)
                - (ot_losses * 0.5)
        )

        return round(score, 2)
