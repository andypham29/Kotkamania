from server.service.prospect_elite_service import ProspectEliteService
from server.service.mockdraft_selector_service import MockDraftSelectorService
from server.service.nhl_team_service import NhlTeamService

from server.model.team import Team
class MockDraftSelectorServiceFacade:

    def __init__(self, total_round=31):
        self.total_round = total_round
    
    def getEntireDraftSimulation(self):
        prospects = ProspectEliteService().getAllProspectsWithRanking()
        mockdraft = MockDraftSelectorService(prospects)
        teams = NhlTeamService().getAllTeams() # unused
        reverseSortedTeams = sorted(teams, key=lambda x: x.leagueRank, reverse=True) # unused

        teams2020 = [Team(name="New York Rangers"), Team(name="Los Angeles Kings"), Team(name="Ottawa Senators (SJS)"), Team(name="Detroit Red Wings"), Team(name="Ottawa Senators"), 
            Team(name="Anaheim Ducks"),Team(name="New Jersey Devils"), Team(name="Buffalo Sabres"), Team(name="Minnesota Wild"), Team(name="Winnipeg Jets"), Team(name="Nashville Predators"), 
            Team(name="Florida Panthers"), Team(name="Carolina Hurricanes (TOR)"),Team(name="Edmonton Oilers"), Team(name="Toronto Maple Leafs(PIT)"), Team(name="Montreal Canadiens"), 
            Team(name="Chicago Blackhawks"), Team(name="New Jersey Devils(ARZ)"), Team(name="Calgary Flames"), Team(name="New Jersey Devils (VAN)"), Team(name="Columbus Blue Jackets"),
            Team(name="New York Rangers (CAR)"), Team(name="Philadelphia Flyers"), Team(name="Washington Capitals"), Team(name="Colorado Avalanche"), Team(name="St. Louis Blues"), 
            Team(name="Anaheim Ducks (BOS)"), Team(name="Ottawa Senators (NYI)"), Team(name="Vegas Golden Knight"), Team(name="Dallas Stars"), Team(name="San Jose Sharks (TBL)")]
        
        draftlist = []
        for i in range(self.total_round):
            draftpick = mockdraft.pickPlayerBySelection(i+1)
            # draftpick.team = reverseSortedTeams[i%len(teams)]
            draftpick.team = teams2020[i%len(teams)]
            draftlist.append(draftpick)

        return draftlist
        # return json.dumps([draft.__dict__ for draft in draftlist])