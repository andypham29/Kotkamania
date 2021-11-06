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
        self.abbreviation = abbreviation
        self.teamName = teamName
        self.score = score
