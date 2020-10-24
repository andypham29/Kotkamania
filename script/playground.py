from server.mockdraft.repository.prospect_elite_dao import ProspectEliteDao

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