class Player:

    def __init__(self, playerId, fullName, position, team, primaryNumber, birthDate, currentAge, birthCity,
                 birthCountry, height, weight, stats=None):
        self.playerId = playerId
        self.fullName = fullName
        self.position = position
        self.team = team
        self.primaryNumber = primaryNumber
        self.birthDate = birthDate
        self.currentAge = currentAge
        self.birthCity = birthCity
        self.birthCountry = birthCountry
        self.height = height
        self.weight = weight
        self.stats = stats


class PlayerStat:

    def __init__(self, player_id, full_name, position, team, games_played, goals, assists, points):
        self.player_id = player_id
        self.full_name = full_name
        self.position = position
        self.team = team
        self.games_played = games_played
        self.goals = goals
        self.assists = assists
        self.points = points


class RosterPlayerInfo:

    def __init__(self, playerId, fullName, position):
        self.playerId = playerId
        self.fullName = fullName
        self.position = position
