from dataclasses import dataclass, field

@dataclass
class Prospect:
    id: str
    rank: str
    player_name: str
    height: str
    weight: str
    position: str
    team: str
    league: str



@dataclass
class ProspectElite:
    id: str = ""
    name: str = None
    position: str = None
    hp: str = None
    fc: str = None
    iss: str = None
    mh: str = None
    elite: str = None
    league: str = None
    team: str = None
    gp: str = None
    g: str = None
    a: str = None
    p: str = None
    pim: str = None
    grade: str = None
    avg_rank: float = field(default=None, init=False)

    def __post_init__(self):
        self.avg_rank = self._get_avg_rank()

    def _get_avg_rank(self):
        total = 0
        count = 0
        list_items = [self.hp, self.fc, self.iss, self.mh, self.elite]

        for item in list_items:
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
