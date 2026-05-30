from dataclasses import dataclass
from typing import Optional


@dataclass
class Team:
    id: str = ""
    name: str = ""
    abbreviation: str = ""
    points: Optional[int] = None
    leagueRank: Optional[int] = None
    teamStats: Optional['TeamStat'] = None

    def toString(self):
        print("({0}) {1}: {2}".format(self.leagueRank, self.name, self.points))


@dataclass
class TeamStat:
    gamesPlayed: int
    wins: int
    losses: int
    ot: int
    pts: int
    ptPctg: float
    goalsPerGame: float
    goalsAgainstPerGame: float
    evGGARatio: float
    powerPlayPercentage: float
    powerPlayGoals: int
    powerPlayGoalsAgainst: int
    powerPlayOpportunities: int
    penaltyKillPercentage: float
    shotsPerGame: float
    shotsAllowed: int
    winScoreFirst: int
    winOppScoreFirst: int
    winLeadFirstPer: int
    winLeadSecondPer: int
    winOutshootOpp: int
    winOutshotByOpp: int
    faceOffsTaken: int
    faceOffsWon: int
    faceOffsLost: int
    faceOffWinPercentage: float
    shootingPctg: float
    savePctg: float

    @dataclass
    class NewTeamStat:
        gamesPlayed: int
        goalDifferential: int
        goalDifferentialPctg: float
        goalAgainst: int
        goalFor: int
        goalsForPctg: float
        homeGamesPlayed: int
        homeGoalDifferential: int
        homeGoalsAgainst: int
        homeGoalsFor: int
        homeLosses: int
        homeOtLosses: int
        homePoints: int
        homeRegulationPlusOtWins: int
        homeRegulationWins: int
        homeTies: int
        homeWins: int
        losses: int
        otLosses: int
        pointPctg: float
        points: int
        regulationPlusOtWinPctg: float
        regulationPlusOtWins: int
        regulationWinPctg: float
        regulationWins: int
        roadGamesPlayed: int
        roadGoalDifferential: int
        roadGoalsAgainst: int
        roadGoalsFor: int
        roadLosses: int
        roadOtLosses: int
        roadPoints: int
        roadRegulationPlusOtWins: int
        roadRegulationWins: int
        roadTies: int
        roadWins: int
        shootoutLosses: int
        shootoutWins: int
        ties: int
        waiversSequence: int
        wildcardSequence: int
        winPctg: float
        wins: int
