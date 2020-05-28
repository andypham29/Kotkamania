from mockdraft_selector import MockDraftSelector

from model.prospect import ProspectElite
from model.draftpick import DraftPick
from repository.prospect_elite_dao import ProspectEliteDao

import json

prospects = ProspectEliteDao().getAllProspects()
mockdraft = MockDraftSelector(prospects)

list = []
for i in range(31):
    # print(i)
    list.append(mockdraft.pickPlayerBySelection(i+1))
# prospect = mockdraft.pickPlayerBySelection(1)


for prospect in list:
    print(prospect.__dict__)
