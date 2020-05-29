class Team:

    def __init__(self,name = "",points = 0, leagueRank = 0):
        self.name = name
        self.points = points
        self.leagueRank = leagueRank

    def toString(self):
        print("({0}) {1}: {2}".format(self.leagueRank, self.name, self.points))


class Player:

    def __init__(self, rank, playerId, fullName, position, team, gamesPlayed, goals, assists, points):
        self.playerId = playerId
        self.rank = rank
        self.fullName = fullName
        self.position = position
        self.team = team
        self.gamesPlayed = gamesPlayed
        self.goals = goals
        self.assists = assists
        self.points = points

    def toString(self):
        print("(id:{0}) {1}\t{2}\t{3}\t{4}\tgp:{5} g:{6} a:{7} p:{8}"
            .format(self.playerId, self.rank, self.fullName, self.position, self.team, self.gamesPlayed, self.goals, self.assists, self.points))
