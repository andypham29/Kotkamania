class Schedule:

    def __init__(self, firstDay, lastDay, games):
        self.firstDay = firstDay
        self.lastDay = lastDay
        self.games = games


class NhlGame:

    def __init__(self, gamePk, day, date, homeTeam, awayTeam):
        self.gamePk = gamePk
        self.day = day
        self.date = date
        self.homeTeam = homeTeam
        self.awayTeam = awayTeam


class TeamGameInfo:

    def __init__(self, teamId, abbreviation, teamName, score):
        self.teamId = teamId
        self.abbreviation = self.__abbreviation_by_teamId(teamId)
        self.teamName = teamName
        self.score = score

    def __abbreviation_by_teamId(self, teamId):
        options = {1: "NJD",
                   2: "NYI",
                   3: "NYR",
                   4: "PHI",
                   5: "PIT",
                   6: "BOS",
                   7: "BUF",
                   8: "MTL",
                   9: "OTT",
                   10: "TOR",
                   12: "CAR",
                   13: "FLA",
                   14: "TBL",
                   15: "WSH",
                   16: "CHI",
                   17: "DET",
                   18: "NSH",
                   19: "STL",
                   20: "CGY",
                   21: "COL",
                   22: "EDM",
                   23: "VAN",
                   24: "ANA",
                   25: "DAL",
                   26: "LAK",
                   28: "SJS",
                   29: "CBJ",
                   30: "MIN",
                   52: "WPG",
                   53: "ARZ",
                   54: "VGK",
                   55: "SEA"
                   }
        return options[teamId]
