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

    def __init__(self):
        self.id = ""
        self.name_position = None
        self.hp = None
        self.fc = None
        self.iss = None
        self.mh = None
        self.elite = None

    # def __init__(self, name_position, hp, fc, iss, mh, elite):
    #     self.id = ""
    #     self.name_position = name_position
    #     self.hp = hp
    #     self.fc = fc
    #     self.iss = iss
    #     self.mh = mh
    #     self.elite = elite
    #
    # def __init__(self, id, name_position, hp, fc, iss, mh, elite):
    #     self.id = id
    #     self.name_position = name_position
    #     self.hp = hp
    #     self.fc = fc
    #     self.iss = iss
    #     self.mh = mh
    #     self.elite = elite

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
