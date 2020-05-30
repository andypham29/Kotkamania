from server.service.prospect_elite_service import ProspectEliteService
from server.service.mockdraft_selector_service import MockDraftSelectorService

class MockDraftSelectorServiceFacade:

    def __init__(self, total_round=31):
        self.total_round = total_round
    
    def getEntireDraftSimulation(self):
        prospects = ProspectEliteService().getAllProspects()
        mockdraft = MockDraftSelectorService(prospects)

        draftlist = []
        for i in range(self.total_round):
            draftlist.append(mockdraft.pickPlayerBySelection(i+1))

        return draftlist
        # return json.dumps([draft.__dict__ for draft in draftlist])