from server.internaldata.repository.fantasy_player_streak_index_dao import FantasyPlayerStreakIndexDao


class FantasyPlayerStreakIndexService:

    def __init__(self, uri=None):
        self.uri = uri

    def initFantasyPlayerStreakIndexTable(self):
        FantasyPlayerStreakIndexDao().initFantasyPlayerStreakIndexTable()

    def saveOrUpdateFantasyPlayerStreakIndex(self, fantasy_streak_info):
        FantasyPlayerStreakIndexDao().saveOrUpdateFantasyPlayerStreakIndex(fantasy_streak_info)

    def getFantasyPlayerStreakIndexById(self, playerId):
        return FantasyPlayerStreakIndexDao().getFantasyPlayerStreakIndex(playerId)

    def getAllFantasyPlayerStreakIndexes(self):
        return FantasyPlayerStreakIndexDao().getAllFantasyPlayerStreakIndexes()

    def getAllFantasyPlayerStreakIndexesByPositionCodes(self, positionCodes):
        return FantasyPlayerStreakIndexDao().getAllFantasyPlayerStreakIndexesByPositionCodes(positionCodes)

    def getAllFantasyPlayerStreakIndexInPlayerIdList(self, playerIdList):
        return FantasyPlayerStreakIndexDao().getAllFantasyPlayerStreakIndexInPlayerIdList(playerIdList)

    def getAllFantasySkatersBySearchName(self, name):
        return FantasyPlayerStreakIndexDao().getAllFantasySkatersBySearchName(name)

    def deleteFantasySkaterById(self, playerId):
        FantasyPlayerStreakIndexDao().deleteFantasySkaterById(playerId)
