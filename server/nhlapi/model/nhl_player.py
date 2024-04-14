class Player:

    def __init__(self, playerId, fullName, position, teamId, team, primaryNumber, birthDate, currentAge, birthCity,
                 birthCountry, height, weight, shootCatches, stats=None, badge=None, playerDraftDetails=None):
        self.playerId = playerId
        self.fullName = fullName
        self.position = position
        self.teamId = teamId
        self.team = team
        self.primaryNumber = primaryNumber
        self.birthDate = birthDate
        self.currentAge = currentAge
        self.birthCity = birthCity
        self.birthCountry = birthCountry
        self.height = height
        self.weight = weight
        self.shootCatches = shootCatches
        self.stats = stats
        self.badge = badge
        self.playerDraftDetails = playerDraftDetails


class PlayerDraftDetails:

    def __init__(self, year, teamAbbrev, draftRound, pickInRound, overallPick):
        self.year = year
        self.teamAbbrev = teamAbbrev
        self.draftRound = draftRound
        self.pickInRound = pickInRound
        self.overallPick = overallPick


class SeasonStat:

    def __init__(self, season, stat):
        self.season = season
        self.stat = stat


class PlayerStat:

    def __init__(self, timeOnIce=None, assists=None, goals=None, pim=None, shots=None, games=None, hits=None,
                 powerPlayGoals=None, powerPlayPoints=None,
                 powerPlayTimeOnIce=None, evenTimeOnIce=None, penaltyMinutes=None, faceOffPct=None, shotPct=None,
                 gameWinningGoals=None,
                 overTimeGoals=None, shortHandedGoals=None, shortHandedPoints=None, shortHandedTimeOnIce=None,
                 blocked=None, plusMinus=None,
                 points=None, shifts=None, timeOnIcePerGame=None, evenTimeOnIcePerGame=None,
                 shortHandedTimeOnIcePerGame=None,
                 powerPlayTimeOnIcePerGame=None):
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


class GoalieStat:
    def __init__(self, timeOnIce, ot, shutouts, ties, wins, losses, saves, powerPlaySaves, shortHandedSaves,
                 evenSaves, shortHandedShots, evenShots, powerPlayShots, savePercentage, goalAgainstAverage,
                 games, gamesStarted, shotsAgainst, goalsAgainst, timeOnIcePerGame, powerPlaySavePercentage,
                 shortHandedSavePercentage, evenStrengthSavePercentage):
        self.timeOnIce = timeOnIce
        self.ot = ot
        self.shutouts = shutouts
        self.ties = ties
        self.wins = wins
        self.losses = losses
        self.saves = saves
        self.powerPlaySaves = powerPlaySaves
        self.shortHandedSaves = shortHandedSaves
        self.evenSaves = evenSaves
        self.shortHandedShots = shortHandedShots
        self.evenShots = evenShots
        self.powerPlayShots = powerPlayShots
        self.savePercentage = savePercentage
        self.goalAgainstAverage = goalAgainstAverage
        self.games = games
        self.gamesStarted = gamesStarted
        self.shotsAgainst = shotsAgainst
        self.goalsAgainst = goalsAgainst
        self.timeOnIcePerGame = timeOnIcePerGame
        self.powerPlaySavePercentage = powerPlaySavePercentage
        self.shortHandedSavePercentage = shortHandedSavePercentage
        self.evenStrengthSavePercentage = evenStrengthSavePercentage
