class Team:

    def __init__(self, name="", points=0, leagueRank=0):
        self.name = name
        self.points = points
        self.leagueRank = leagueRank

    def toString(self):
        print("({0}) {1}: {2}".format(self.leagueRank, self.name, self.points))
