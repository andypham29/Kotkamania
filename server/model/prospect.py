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

    def __init__(self, id="", name=None, position=None, hp=None, fc=None, iss=None, mh=None, elite=None, avg_rank=None, league=None, team=None, gp=None, g=None, a=None, p=None, pim=None):
        self.id = id
        self.name = name
        self.position = position
        self.hp = hp
        self.fc = fc
        self.iss = iss
        self.mh = mh
        self.elite = elite
        self.avg_rank = None
        self.league = league
        self.team = team
        self.gp = gp
        self.g = g
        self.a = a
        self.p = p
        self.pim = pim

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
