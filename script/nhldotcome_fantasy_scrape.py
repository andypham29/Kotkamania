import csv

from server.internaldata.repository.fantasy_nhl_player_dao import FantasyNhlPlayerDao


class NhlFantasyPlayerDao(object):
    pass


def hello():
    with open('nhl_data.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            playerName = row[1][1:]
            nhlRank = int(row[0])
            # print(playerName[1:], ": ", nhlRank)
            FantasyNhlPlayerDao(
                '../server/internaldata/db/internal.db'
            ).updateNhlRankForFantasySkaterWithName(playerName, nhlRank)


if __name__ == '__main__':
    hello()
