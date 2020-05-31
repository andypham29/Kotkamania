from server.repository.prospect_elite_dao import ProspectEliteDao

class ProspectEliteService:

    def initTable(self):
        try:
            ProspectEliteDao().initProspectEliteTable()
        except:
            print("Unable to initialize table for prospect")
            raise Exception("Unable to initialize table for prospect")
    
    def getProspectById(self,id):
        try:
            return ProspectEliteDao().getProspectById(id)
        except:
            print(f"[{id}] Unable to get prospect")
            raise Exception(f"[{id}] Unable to get prospect")

    def getAllProspects(self):
        try:
            return ProspectEliteDao().getAllProspects()
        except:
            print("Unable to get all prospects")
            raise Exception("Unable to get all prospects")
    
    def getAllProspectsWithRanking(self):
        try:
            return ProspectEliteDao().getAllProspectsWithRanking()
        except:
            print("Unable to get prospects")
            raise Exception("Unable to get prospects")
    
    def getProspectsAtPage(self, page=1):
        try:
            return ProspectEliteDao().getProspectsAtPage(page)
        except:
            print("Unable to get prospects")
            raise Exception("Unable to get prospects")

    def insertOrUpdateProspectElite(self, prospect):
        try:
            return ProspectEliteDao().insertOrUpdateProspectElite(prospect)
        except:
            print("Unable to insert prospect")
            raise Exception("Unable to insert prospect")