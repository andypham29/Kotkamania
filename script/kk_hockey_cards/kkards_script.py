from server.internaldata.service.fantasy_nhl_player_service import FantasyNhlPlayerService
import csv


if __name__ == '__main__':

    fantasy = FantasyNhlPlayerService(uri="../../server/internaldata/db/internal.db")
    with open('hockey_cards.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            # print(row)
            player = fantasy.getAllFantasySkatersBySearchName(row[1])
            if len(player) > 0:
                print(",".join([str(player[0].playerId), player[0].skaterFullName, row[2]]))
