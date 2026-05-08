from dataclasses import dataclass


@dataclass
class FantasySkaterGrade:
    grade_g: float
    grade_a: float
    grade_p: float
    grade_ppg: float
    grade_ppa: float
    grade_ppp: float
    grade_shotPct: float
    grade_toi: float
    grade_pptoi: float
    grade_evtoi: float
    grade_shotAttempt: float

    def __post_init__(self):
        self.g = round(self.grade_g, 2)
        self.a = round(self.grade_a, 2)
        self.p = round(self.grade_p, 2)
        self.ppg = round(self.grade_ppg, 2)
        self.ppa = round(self.grade_ppa, 2)
        self.ppp = round(self.grade_ppp, 2)
        self.shotPct = round(self.grade_shotPct, 2)
        self.toi = round(self.grade_toi, 2)
        self.pptoi = round(self.grade_pptoi, 2)
        self.evtoi = round(self.grade_evtoi, 2)
        self.shotAttempt = round(self.grade_shotAttempt, 2)
