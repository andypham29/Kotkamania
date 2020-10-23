from server.mockdraft.repository.prospect_elite_dao import ProspectEliteDao

class ProspectEliteService:

    def initTable(self):
        try:
            ProspectEliteDao().initProspectEliteTable()
        except:
            raise Exception("Unable to initialize table for prospect")
    
    def getProspectById(self,id):
        try:
            return ProspectEliteDao().getProspectById(id)
        except:
            raise Exception(f"[{id}] Unable to get prospect")

    def getAllProspects(self):
        try:
            return ProspectEliteDao().getAllProspects()
        except:
            raise Exception("Unable to get all prospects")
    
    def getProspectByPosition(self, position, page=0):
        try:
            return ProspectEliteDao().getProspectByPosition(position, page)
        except:
            raise Exception("Unable to get prospects with requested position")
    
    def getAllProspectsWithRanking(self):
        try:
            return ProspectEliteDao().getAllProspectsWithRanking()
        except:
            raise Exception("Unable to get prospects")
    
    def getProspectsAtPage(self, page=1):
        try:
            return ProspectEliteDao().getProspectsAtPage(page)
        except:
            raise Exception("Unable to get prospects")

    def insertOrUpdateProspectElite(self, prospect):
        try:
            return ProspectEliteDao().insertOrUpdateProspectElite(prospect)
        except:
            raise Exception("Unable to insert prospect")

    def updateProspectEliteAvgRank(self, prospect):
        try:
            return ProspectEliteDao().updateProspectEliteAvgRank(prospect)
        except:
            raise Exception("Unable to update prospect")

