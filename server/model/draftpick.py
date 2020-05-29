class DraftPick:

    def __init__(self,id="", pick=0, team="", name_position="", odds=0, list_ball=[], picked_ball=0):
        self.id = id
        self.pick = pick
        self.team = team
        self.name_position = name_position
        self.odds = odds
        self.list_ball = list_ball
        self.picked_ball = picked_ball

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
