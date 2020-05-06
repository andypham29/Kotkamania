class Prospect:

    def __init__(self, rank, player_name, height, weight, position, team, league):
        self.id = ""
        self.rank = rank
        self.player_name = player_name
        self.height = height
        self.weight = weight
        self.position = position
        self.team = team
        self.league = league

    def __init__(self, id, rank, player_name, height, weight, position, team, league):
        self.id = id
        self.rank = rank
        self.player_name = player_name
        self.height = height
        self.weight = weight
        self.position = position
        self.team = team
        self.league = league

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
