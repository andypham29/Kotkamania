from server.service.mockdraft_selector_service import MockDraftSelectorService


from server.model.prospect import ProspectElite
from server.model.draftpick import DraftPick
from server.repository.prospect_elite_dao import ProspectEliteDao

import json

prospects = ProspectEliteDao().getAllProspects()
mockdraft = MockDraftSelectorService(prospects)

list = []
for i in range(31):
    # print(i)
    list.append(mockdraft.pickPlayerBySelection(i+1))
# prospect = mockdraft.pickPlayerBySelection(1)


for prospect in list:
    print(prospect.__dict__)
