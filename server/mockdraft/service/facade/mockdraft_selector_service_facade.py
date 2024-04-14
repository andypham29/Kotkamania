from server.mockdraft.service.mockdraft_selector_service import MockDraftSelectorService
from server.mockdraft.service.prospect_elite_service import ProspectEliteService
from server.nhlapi.service.nhl_team_service import NhlTeamService


class MockDraftSelectorServiceFacade:

    def __init__(self, total_round=32):
        self.total_round = total_round
    
    def getEntireDraftSimulation(self):
        prospects = ProspectEliteService().getAllProspectsWithRanking()
        mockdraft = MockDraftSelectorService(prospects)
        teams = NhlTeamService().getAllTeamsForDraft()
        reverseSortedTeams = sorted(teams, key=lambda x: x.leagueRank, reverse=True)

        draftlist = []
        for i in range(self.total_round):
            draftpick = mockdraft.pickPlayerBySelection(i+1)
            draftpick.team = reverseSortedTeams[i % len(teams)]
            draftlist.append(draftpick)

        return draftlist
