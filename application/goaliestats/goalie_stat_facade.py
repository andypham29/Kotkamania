from application.goaliestats.goalie_stat_service import GoalieStatService
from infra.spi.nhlapi.nhlgoalie.nhl_goalie_summary_service import NHLGoalieSummaryService


class GoalieStatFacade:

    def __init__(self):
        self.goalie_stat_service = GoalieStatService()
        self.nhl_goalie_summary_service = NHLGoalieSummaryService()

    def save_all_goalie_stats(self):
        stats = self.nhl_goalie_summary_service.getAllGoalies()

        for stat in stats:
            self.goalie_stat_service.save(stat.to_application())


    def save_all_goalie_percentile_stats(self):
        stats = self.nhl_goalie_summary_service.getAllGoalies()

        for stat in stats:
            self.goalie_stat_service.save(stat.to_application())
