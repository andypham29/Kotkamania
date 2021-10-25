import re

from server.internaldata.repository.fantasy_nhl_player_dao import FantasyNhlPlayerDao


class FantasyNhlPlayerService:

    def __init__(self, uri=None):
        self.uri = uri

    def initFantasySkaterTable(self):
        FantasyNhlPlayerDao(self.uri).initFantasySkaterTable()

    def saveFantasySkater(self, fantasy_skater):
        FantasyNhlPlayerDao(self.uri).saveFantasySkater(fantasy_skater)

    def getFantasySkaterById(self, id):
        return FantasyNhlPlayerDao(self.uri).getFantasySkaterById(id)

    def getAllFantasySkaters(self):
        return FantasyNhlPlayerDao(self.uri).getAllFantasySkatersWithStat()

    def getAllFantasySkatersWithPositionCodes(self, positionCodes, offset=None):
        return FantasyNhlPlayerDao(self.uri).getAllFantasySkatersByPositionCodesWithStats(positionCodes, offset)

    def getAllFantasySkatersInPlayerIdList(self, playerIdList):
        return FantasyNhlPlayerDao(self.uri).getAllFantasySkatersInPlayerIdList(playerIdList)

    def getAllFantasySkatersWithTeamId(self, teamId):
        return FantasyNhlPlayerDao(self.uri).getAllFantasySkatersByTeamId(teamId)

    def getAllFantasySkatersBySearchName(self, name):
        regex = re.compile('[^a-zA-Z- ]')
        name = regex.sub('', name)
        if name == "" or len(name) < 3:
            return []
        return FantasyNhlPlayerDao(self.uri).getAllFantasySkatersBySearchName(name)

    def deleteFantasySkaterById(self, id):
        FantasyNhlPlayerDao(self.uri).deleteFantasySkaterById(id)

    def updateFantasyGradeForFantasySkaterWithId(self, id, grade):
        FantasyNhlPlayerDao(self.uri).updateFantasyGradeForFantasySkaterWithId(id, grade)

    def updateFantasyYahooInfoForFantasySkater(self, yahoo_info):
        FantasyNhlPlayerDao(self.uri).updateFantasyYahooInfoForFantasySkater(yahoo_info)
