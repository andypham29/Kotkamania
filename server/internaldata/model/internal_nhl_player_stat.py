class InternalPlayerStat:

    def __init__(self, playerId, seasonId, timeOnIce=None, assists=None, goals=None, pim=None, shots=None, games=None,
                 hits=None,
                 powerPlayGoals=None, powerPlayPoints=None,
                 powerPlayTimeOnIce=None, evenTimeOnIce=None, penaltyMinutes=None, faceOffPct=None, shotPct=None,
                 gameWinningGoals=None,
                 overTimeGoals=None, shortHandedGoals=None, shortHandedPoints=None, shortHandedTimeOnIce=None,
                 blocked=None, plusMinus=None,
                 points=None, shifts=None, timeOnIcePerGame=None, evenTimeOnIcePerGame=None,
                 shortHandedTimeOnIcePerGame=None,
                 powerPlayTimeOnIcePerGame=None):
        self.playerId = playerId
        self.seasonId = seasonId
        self.timeOnIce = timeOnIce
        self.assists = assists
        self.goals = goals
        self.pim = pim
        self.shots = shots
        self.games = games
        self.hits = hits
        self.powerPlayGoals = powerPlayGoals
        self.powerPlayPoints = powerPlayPoints
        self.powerPlayTimeOnIce = powerPlayTimeOnIce
        self.evenTimeOnIce = evenTimeOnIce
        self.penaltyMinutes = penaltyMinutes
        self.faceOffPct = faceOffPct
        self.shotPct = shotPct
        self.gameWinningGoals = gameWinningGoals
        self.overTimeGoals = overTimeGoals
        self.shortHandedGoals = shortHandedGoals
        self.shortHandedPoints = shortHandedPoints
        self.shortHandedTimeOnIce = shortHandedTimeOnIce
        self.blocked = blocked
        self.plusMinus = plusMinus
        self.points = points
        self.shifts = shifts
        self.timeOnIcePerGame = timeOnIcePerGame
        self.evenTimeOnIcePerGame = evenTimeOnIcePerGame
        self.shortHandedTimeOnIcePerGame = shortHandedTimeOnIcePerGame
        self.powerPlayTimeOnIcePerGame = powerPlayTimeOnIcePerGame
