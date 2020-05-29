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

class ProspectElite:

    def __init__(self, id="", name_position=None, hp=None, fc=None, iss=None, mh=None, elite=None, avg_rank=None):
        self.id = id
        self.name_position = name_position
        self.hp = hp
        self.fc = fc
        self.iss = iss
        self.mh = mh
        self.elite = elite
        self.avg_rank = None

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
