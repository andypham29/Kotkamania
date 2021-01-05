class FantasySkaterGrade:

    def __init__(self, grade_g, grade_a, grade_p, grade_ppg, grade_ppa,
                 grade_ppp, grade_shotPct, grade_toi, grade_pptoi,
                 grade_evtoi, grade_shotAttempt):
        self.g = round(grade_g, 2)
        self.a = round(grade_a, 2)
        self.p = round(grade_p, 2)
        self.ppg = round(grade_ppg, 2)
        self.ppa = round(grade_ppa, 2)
        self.ppp = round(grade_ppp, 2)
        self.shotPct = round(grade_shotPct, 2)
        self.toi = round(grade_toi, 2)
        self.pptoi = round(grade_pptoi, 2)
        self.evtoi = round(grade_evtoi, 2)
        self.shotAttempt = round(grade_shotAttempt, 2)
