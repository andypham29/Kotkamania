from server.internaldata.repository.fantasy_nhl_player_dao import FantasyNhlPlayerDao


class FantasyNhlPlayerService:

    def __init__(self):
        pass

    def initFantasySkaterTable(self):
        FantasyNhlPlayerDao().initFantasySkaterTable()

    def saveFantasySkater(self, fantasy_skater):
        FantasyNhlPlayerDao().saveFantasySkater(fantasy_skater)

    def getFantasySkaterById(self, id):
        return FantasyNhlPlayerDao().getFantasySkaterById(id)

    def getAllFantasySkaters(self):
        return FantasyNhlPlayerDao().getAllFantasySkaters()

    def deleteFantasySkaterById(self, id):
        FantasyNhlPlayerDao().deleteFantasySkaterById(id)

    def updateFantasyGradeForFantasySkaterWithId(self, id, grade):
        FantasyNhlPlayerDao().updateFantasyGradeForFantasySkaterWithId(id, grade)
