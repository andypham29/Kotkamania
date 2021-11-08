from server.internaldata.repository.fantasy_nhl_player_dao import FantasyNhlPlayerDao


def hello():
    a = FantasyNhlPlayerDao('../server/internaldata/db/fantasy.db')
    b = FantasyNhlPlayerDao('../server/internaldata/db/internal.db')
    #
    # quinn = a.getFantasySkaterById(8480800)
    # b.saveFantasySkater(quinn)

    brady = a.getFantasySkaterById(8480801)
    print(brady.teamId + 10)
    # b.saveFantasySkater(brady)


if __name__ == '__main__':
    hello()
    # prospects = ProspectEliteDao().getProspectByPosition("G", 0)
    # mockdraft = MockDraftSelectorService(prospects)

    # list = []
    # for i in range(31):
    # print(i)
    # list.append(mockdraft.pickPlayerBySelection(i+1))
    # prospect = mockdraft.pickPlayerBySelection(1)

    # for prospect in prospects:
    #     print(prospect.__dict__)

    # print([prospect.__dict__ for prospect in prospects])
