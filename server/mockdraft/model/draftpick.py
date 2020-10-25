from server.mockdraft.model.prospect import ProspectElite

class DraftPick:

    def __init__(self, pick=0, team="", player=ProspectElite(), odds=0, list_ball=[], picked_ball=0, prospectlist=[]):
        self.pick = pick
        self.team = team
        self.player = player
        self.odds = odds
        self.list_ball = list_ball
        self.picked_ball = picked_ball
        self.prospectlist = prospectlist

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
