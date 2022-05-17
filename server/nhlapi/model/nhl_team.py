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
