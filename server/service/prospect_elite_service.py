from server.repository.prospect_elite_dao import ProspectEliteDao

class ProspectEliteService:



    def initTable(self):
        try:
            ProspectEliteDao().initProspectEliteTable()
        except:
            print("Unable to initialize table for prospect")
            raise
    
    def getProspectById(self,id):
        try:
            return ProspectEliteDao().getProspectById(id)
        except:
            print(f"[{id}] Unable to get prospect")
            raise
    def getAllProspects(self):
        try:
            return ProspectEliteDao().getAllProspects()
        except:
            print("Unable to get all prospects")
            raise

    def insertOrUpdateProspectElite(self, prospect):
        try:
            return ProspectEliteDao().insertOrUpdateProspectElite(prospect)
        except:
            print("Unable to insert prospect")
            raise