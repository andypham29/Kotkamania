class FantasyNhlPlayer:

    def __init__(self, id="",
                 skaterFullName="",
                 positionCode="",
                 teamId="",
                 fantasyGrade=None,
                 yahooEligibility=None,
                 avgPick=None,
                 avgRound=None,
                 percentDrafted=None,
                 teamName="",
                 nhlRank=None):
        self.playerId = id
        self.skaterFullName = skaterFullName
        self.positionCode = positionCode
        self.teamId = teamId
        self.fantasyGrade = fantasyGrade
        self.yahooEligibility = yahooEligibility
        self.avgPick = avgPick
        self.avgRound = avgRound
        self.percentDrafted = percentDrafted
        self.teamName = teamName
        self.nhlRank = nhlRank
