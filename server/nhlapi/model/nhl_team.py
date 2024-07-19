class Team:

    def __init__(self, id="", name="", abbreviation="", points=None, leagueRank=None, teamStats=None):
        self.id = id
        self.name = name
        self.abbreviation = abbreviation
        self.points = points
        self.leagueRank = leagueRank
        self.teamStats = teamStats

    def toString(self):
        print("({0}) {1}: {2}".format(self.leagueRank, self.name, self.points))


class TeamStat:

    def __init__(self,
                 gamesPlayed,
                 wins,
                 losses,
                 ot,
                 pts,
                 ptPctg,
                 goalsPerGame,
                 goalsAgainstPerGame,
                 evGGARatio,
                 powerPlayPercentage,
                 powerPlayGoals,
                 powerPlayGoalsAgainst,
                 powerPlayOpportunities,
                 penaltyKillPercentage,
                 shotsPerGame,
                 shotsAllowed,
                 winScoreFirst,
                 winOppScoreFirst,
                 winLeadFirstPer,
                 winLeadSecondPer,
                 winOutshootOpp,
                 winOutshotByOpp,
                 faceOffsTaken,
                 faceOffsWon,
                 faceOffsLost,
                 faceOffWinPercentage,
                 shootingPctg,
                 savePctg):
        self.gamesPlayed = gamesPlayed
        self.wins = wins
        self.losses = losses
        self.ot = ot
        self.pts = pts
        self.ptPctg = ptPctg
        self.goalsPerGame = goalsPerGame
        self.goalsAgainstPerGame = goalsAgainstPerGame
        self.evGGARatio = evGGARatio
        self.powerPlayPercentage = powerPlayPercentage
        self.powerPlayGoals = powerPlayGoals
        self.powerPlayGoalsAgainst = powerPlayGoalsAgainst
        self.powerPlayOpportunities = powerPlayOpportunities
        self.penaltyKillPercentage = penaltyKillPercentage
        self.shotsPerGame = shotsPerGame
        self.shotsAllowed = shotsAllowed
        self.winScoreFirst = winScoreFirst
        self.winOppScoreFirst = winOppScoreFirst
        self.winLeadFirstPer = winLeadFirstPer
        self.winLeadSecondPer = winLeadSecondPer
        self.winOutshootOpp = winOutshootOpp
        self.winOutshotByOpp = winOutshotByOpp
        self.faceOffsTaken = faceOffsTaken
        self.faceOffsWon = faceOffsWon
        self.faceOffsLost = faceOffsLost
        self.faceOffWinPercentage = faceOffWinPercentage
        self.shootingPctg = shootingPctg
        self.savePctg = savePctg

    class NewTeamStat:

        def __init__(self, gamesPlayed, goalDifferential, goalDifferentialPctg, goalAgainst, goalFor, goalsForPctg,
                     homeGamesPlayed, homeGoalDifferential, homeGoalsAgainst, homeGoalsFor, homeLosses, homeOtLosses,
                     homePoints, homeRegulationPlusOtWins, homeRegulationWins, homeTies, homeWins, losses, otLosses,
                     pointPctg, points, regulationPlusOtWinPctg, regulationPlusOtWins, regulationWinPctg,
                     regulationWins, roadGamesPlayed, roadGoalDifferential, roadGoalsAgainst, roadGoalsFor, roadLosses,
                     roadOtLosses, roadPoints, roadRegulationPlusOtWins, roadRegulationWins, roadTies, roadWins,
                     shootoutLosses, shootoutWins, ties, waiversSequence, wildcardSequence, winPctg, wins,
                     ):
            self.gamesPlayed = gamesPlayed
            self.goalDifferential = goalDifferential
            self.goalDifferentialPctg = goalDifferentialPctg
            self.goalAgainst = goalAgainst
            self.goalFor = goalFor
            self.goalsForPctg = goalsForPctg
            self.homeGamesPlayed = homeGamesPlayed
            self.homeGoalDifferential = homeGoalDifferential
            self.homeGoalsAgainst = homeGoalsAgainst
            self.homeGoalsFor = homeGoalsFor
            self.homeLosses = homeLosses
            self.homeOtLosses = homeOtLosses
            self.homePoints = homePoints
            self.homeRegulationPlusOtWins = homeRegulationPlusOtWins
            self.homeRegulationWins = homeRegulationWins
            self.homeTies = homeTies
            self.homeWins = homeWins
            self.losses = losses
            self.otLosses = otLosses
            self.pointPctg = pointPctg
            self.points = points
            self.regulationPlusOtWinPctg = regulationPlusOtWinPctg
            self.regulationPlusOtWins = regulationPlusOtWins
            self.regulationWinPctg = regulationWinPctg
            self.regulationWins = regulationWins
            self.roadGamesPlayed = roadGamesPlayed
            self.roadGoalDifferential = roadGoalDifferential
            self.roadGoalsAgainst = roadGoalsAgainst
            self.roadGoalsFor = roadGoalsFor
            self.roadLosses = roadLosses
            self.roadOtLosses = roadOtLosses
            self.roadPoints = roadPoints
            self.roadRegulationPlusOtWins = roadRegulationPlusOtWins
            self.roadRegulationWins = roadRegulationWins
            self.roadTies = roadTies
            self.roadWins = roadWins
            self.shootoutLosses = shootoutLosses
            self.shootoutWins = shootoutWins
            self.ties = ties
            self.waiversSequence = waiversSequence
            self.wildcardSequence = wildcardSequence
            self.winPctg = winPctg
            self.wins = wins
