from server.commons.fantasybadge.model.fantasy_player_badge import FantasyPlayerBadge


class DisplayStat:

    def __init__(self, assists=0, goals=0, points=0, games=0, shots=0,
                 hits=0, blocked=0, plusMinus=0, powerPlayGoals=0, powerPlayPoints=0):
        self.assists = assists
        self.goals = goals
        self.points = points
        self.games = games
        self.shots = shots
        self.hits = hits
        self.blocked = blocked
        self.plusMinus = plusMinus
        self.powerPlayGoals = powerPlayGoals
        self.powerPlayPoints = powerPlayPoints


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
                 nhlRank=None,
                 badge=None,
                 stat=None):
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
        self.badge = badge if badge else FantasyPlayerBadge()
        self.stat = stat if stat else DisplayStat()
