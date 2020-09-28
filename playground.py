from server.service.mockdraft_selector_service import MockDraftSelectorService


from server.model.prospect import ProspectElite
from server.model.draftpick import DraftPick
from server.repository.prospect_elite_dao import ProspectEliteDao

from server.service.nhl_team_service import NhlTeamService

import json

prospects = ProspectEliteDao().getProspectByPosition("G", 0)
# mockdraft = MockDraftSelectorService(prospects)

# list = []
# for i in range(31):
    # print(i)
    # list.append(mockdraft.pickPlayerBySelection(i+1))
# prospect = mockdraft.pickPlayerBySelection(1)


for prospect in prospects:
    print(prospect.__dict__)

print([prospect.__dict__ for prospect in prospects])