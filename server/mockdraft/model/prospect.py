class Prospect:

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

    def __init__(self, id="", name=None, position=None, hp=None, fc=None, iss=None, mh=None, elite=None, avg_rank=None,
                 league=None, team=None, gp=None, g=None, a=None, p=None, pim=None, grade=None):
        self.id = id
        self.name = name
        self.position = position
        self.hp = hp
        self.fc = fc
        self.iss = iss
        self.mh = mh
        self.elite = elite
        self.avg_rank = self.__get_avg_rank()
        self.league = league
        self.team = team
        self.gp = gp
        self.g = g
        self.a = a
        self.p = p
        self.pim = pim
        self.grade = None

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __get_avg_rank(self):
        total = 0
        count = 0
        list = [self.hp, self.fc, self.iss, self.mh, self.elite]

        for item in list:
            if item is None or item == "-":
                count += 1
                total += 42

            else:
                if str.isdigit(item):
                    count += 1
                    total += int(item)
                else:
                    count += 1
                    total += 42
        if total / count == 42:
            return None
        return total / count
