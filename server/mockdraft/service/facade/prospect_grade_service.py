class ProspectGradeService:

    def __init__(self, prospect):
        self.prospect = prospect

    def get_skater_grade(self):
        return None

    def calculate_skater_goal_grade(self):
        goal = self.prospect.g / self.prospect.gp
        return goal

    def calculate_skater_assist_grade(self):
        assist = self.prospect.a / self.prospect.gp
        return assist
