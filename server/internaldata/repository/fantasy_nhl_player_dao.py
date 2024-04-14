import sqlite3

from server.commons.fantasybadge.model.fantasy_player_badge import FantasyPlayerBadge
from server.commons.helper.nhl_season_converter import NhlYearConverter
from server.internaldata.model.fantasy_nhl_player import FantasyNhlPlayer, DisplayStat


class FantasyNhlPlayerDao:

    def __init__(self, uri=None):
        # uri = 'server/internaldata/db/fantasy.db' if uri is None else uri
        uri = 'server/internaldata/db/internal.db' if uri is None else uri
        # uri = '../../server/internaldata/db/internal.db' if uri is None else uri
        self.conn = sqlite3.connect(uri)
        self.c = self.conn.cursor()
        self.year = NhlYearConverter.get_previous_season_by_year_removed(1)

    def initFantasySkaterTable(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS fantasy_nhl_player(
            playerId INTEGER PRIMARY KEY,
            skaterFullName TEXT NOT NULL,
            positionCode TEXT NOT NULL,
            teamId INTEGER NOT NULL,
            fantasyGrade DOUBLE,
            yahooEligibility TEXT,
            avgPick DOUBLE,
            avgRound DOUBLE,
            percentDrafted TEXT,
            teamName TEXT NOT NULL,
            nhlRank INTEGER,
            scoring DOUBLE,
            playmaking DOUBLE,
            defense DOUBLE,
            powerplay DOUBLE,
            intangibles DOUBLE
            )''')

        self.conn.commit()
        self.conn.close()

    def saveFantasySkater(self, fantasy_skater):

        self.c.execute(
            '''INSERT OR IGNORE INTO fantasy_nhl_player (playerId, 
            skaterFullName, 
            positionCode, 
            teamId, 
            teamName, 
            fantasyGrade,
            yahooEligibility,
            avgPick,
            avgRound,
            percentDrafted,
            nhlRank) VALUES (?,?,?,?,?,?,?,?,?,?,?)''',
            (fantasy_skater.playerId,
             fantasy_skater.skaterFullName,
             fantasy_skater.positionCode,
             fantasy_skater.teamId,
             fantasy_skater.teamName,
             fantasy_skater.fantasyGrade,
             fantasy_skater.yahooEligibility,
             fantasy_skater.avgPick,
             fantasy_skater.avgRound,
             fantasy_skater.percentDrafted,
             fantasy_skater.nhlRank))

        self.c.execute(
            '''UPDATE fantasy_nhl_player SET
            skaterFullName = ifnull(?, skaterFullName), 
            positionCode = ifnull(?, positionCode), 
            teamId = ifnull(?, teamId), 
            teamName = ifnull(?, teamName), 
            fantasyGrade = ifnull(?, fantasyGrade),
            yahooEligibility = ifnull(?, yahooEligibility),
            avgPick = ifnull(?, avgPick),
            avgRound = ifnull(?, avgRound),
            percentDrafted = ifnull(?, percentDrafted),
            nhlRank = ifnull(?, nhlRank)
            WHERE playerId = ?''',
            (fantasy_skater.skaterFullName,
             fantasy_skater.positionCode,
             fantasy_skater.teamId,
             fantasy_skater.teamName,
             fantasy_skater.fantasyGrade,
             fantasy_skater.yahooEligibility,
             fantasy_skater.avgPick,
             fantasy_skater.avgRound,
             fantasy_skater.percentDrafted,
             fantasy_skater.nhlRank,
             fantasy_skater.playerId))

        self.conn.commit()
        self.conn.close()

    def getFantasySkaterById(self, playerId):
        self.c.execute('''SELECT * FROM fantasy_nhl_player WHERE playerId = ?''', (playerId,))

        row = self.c.fetchone()

        self.conn.close()
        return self.__convert_to_model(row)

    def getAllFantasySkatersWithStat(self):
        self.c.execute(f'''SELECT a.playerId, skaterFullName, positionCode, teamId, fantasyGrade, yahooEligibility, 
            avgPick, avgRound, percentDrafted, teamName, nhlRank, scoring, playmaking, defense, powerplay, intangibles,
            assists, goals, points, games, shots, hits, blocked, plusMinus, powerPlayGoals, powerPlayPoints 
            FROM fantasy_nhl_player a
            LEFT JOIN (SELECT * FROM internal_player_stat WHERE seasonId == {self.year}) b
            USING(playerId)
            ''')

        records = self.c.fetchall()

        list = []
        for row in records:
            fantasy_skater = self.__convert_to_model_with_display_stat(row)
            list.append(fantasy_skater)

        self.conn.close()

        return list

    def getAllFantasySkatersByPositionCodesWithStats(self, positionCodes, offset):
        positionCodes[:] = [value for value in positionCodes if value in ['L', 'C', 'R', 'D', 'G']]
        filter_parameters = str(positionCodes).replace('[', '(').replace(']', ')')

        query = f'''SELECT a.playerId, skaterFullName, positionCode, teamId, fantasyGrade, yahooEligibility, 
            avgPick, avgRound, percentDrafted, teamName, nhlRank, scoring, playmaking, defense, powerplay, intangibles, 
            assists, goals, points, games, shots, hits, blocked, plusMinus, powerPlayGoals, powerPlayPoints 
            FROM fantasy_nhl_player a
            LEFT JOIN (SELECT * FROM internal_player_stat WHERE seasonId == {self.year}) b
            USING(playerId)
            WHERE positionCode IN {filter_parameters}'''
        for position in positionCodes:
            query += f" OR yahooEligibility LIKE '%{position}%'"

        if offset is not None:
            query += f"LIMIT 125 OFFSET {125 * offset}"

        self.c.execute(query)

        records = self.c.fetchall()

        list = []
        for row in records:
            fantasy_skater = self.__convert_to_model_with_display_stat(row)
            list.append(fantasy_skater)

        self.conn.close()

        return list

    def getAllFantasySkatersByPositionCodes(self, positionCodes, offset):
        positionCodes[:] = [value for value in positionCodes if value in ['L', 'C', 'R', 'D', 'G']]
        filter_parameters = str(positionCodes).replace('[', '(').replace(']', ')')

        query = f'''SELECT a.playerId, skaterFullName, positionCode, teamId, fantasyGrade, yahooEligibility, 
            avgPick, avgRound, percentDrafted, teamName, nhlRank, scoring, playmaking, defense, powerplay, intangibles, 
            assists, goals, points, games, shots, hits, blocked, plusMinus, powerPlayGoals, powerPlayPoints 
            WHERE positionCode IN {filter_parameters}'''
        for position in positionCodes:
            query += f" OR yahooEligibility LIKE '%{position}%'"

        if offset is not None:
            query += f"LIMIT 125 OFFSET {125 * offset}"

        self.c.execute(query)

        records = self.c.fetchall()

        list = []
        for row in records:
            fantasy_skater = self.__convert_to_model_with_display_stat(row)
            list.append(fantasy_skater)

        self.conn.close()

        return list

    def getAllFantasySkaters(self):
        self.c.execute('''SELECT * FROM fantasy_nhl_player WHERE fantasyGrade > 30''')  # temp

        records = self.c.fetchall()

        list = []
        for row in records:
            fantasy_skater = self.__convert_to_model(row)
            list.append(fantasy_skater)

        self.conn.close()

        return list

    def getAllFantasySkatersByPositionCodes(self, positionCodes, offset):
        positionCodes[:] = [value for value in positionCodes if value in ['L', 'C', 'R', 'D', 'G']]
        filter_parameters = str(positionCodes).replace('[', '(').replace(']', ')')

        query = f'''SELECT * FROM fantasy_nhl_player 
            WHERE positionCode IN {filter_parameters}'''
        for position in positionCodes:
            query += f" OR yahooEligibility LIKE '%{position}%'"
        # query += f"LIMIT 125 OFFSET {125 * offset}"

        self.c.execute(query)

        records = self.c.fetchall()

        list = []
        for row in records:
            fantasy_skater = self.__convert_to_model(row)
            list.append(fantasy_skater)

        self.conn.close()

        return list

    def getAllFantasySkatersInPlayerIdList(self, playerIdList):
        # positionCodes[:] = [value for value in positionCodes if value in ['L', 'C', 'R', 'D', 'G']]
        filter_parameters = str(playerIdList).replace('[', '(').replace(']', ')')

        query = f'''SELECT * FROM fantasy_nhl_player 
            WHERE positionCode IN {filter_parameters}'''

        self.c.execute(query)

        records = self.c.fetchall()

        list = []
        for row in records:
            fantasy_skater = self.__convert_to_model(row)
            list.append(fantasy_skater)

        self.conn.close()

        return list

    def getAllFantasySkatersByTeamId(self, teamId):
        self.c.execute('''SELECT * FROM fantasy_nhl_player WHERE teamId=?''', (teamId,))

        records = self.c.fetchall()

        list = []
        for row in records:
            fantasy_skater = self.__convert_to_model(row)
            list.append(fantasy_skater)

        self.conn.close()

        return list

    def getAllFantasySkatersBySearchName(self, name):
        self.c.execute(f"SELECT * FROM fantasy_nhl_player WHERE skaterFullName LIKE \'%{name}%\'")

        records = self.c.fetchall()

        list = []
        for row in records:
            fantasy_skater = self.__convert_to_model(row)
            list.append(fantasy_skater)

        self.conn.close()

        return list

    def deleteFantasySkaterById(self, playerId):
        self.c.execute('''DELETE FROM fantasy_nhl_player WHERE playerId=?''', (playerId,))

        self.conn.commit()
        self.conn.close()

    def updateFantasyGradeForFantasySkaterWithId(self, playerId, grade):
        self.c.execute('''UPDATE fantasy_nhl_player SET
        fantasyGrade = ?
        WHERE playerId = ?''', (grade, playerId,))

        self.conn.commit()
        self.conn.close()

    def updateNhlRankForFantasySkaterWithName(self, playerName, nhlRank):
        print(playerName, ": ", nhlRank)
        # self.c.execute('''UPDATE fantasy_nhl_player SET nhlRank = NULL''')
        self.c.execute('''UPDATE fantasy_nhl_player SET
        nhlRank = ?
        WHERE skaterFullName = ?''', (nhlRank, playerName,))

        self.conn.commit()
        self.conn.close()

    def updateFantasyYahooInfoForFantasySkater(self, yahoo_info):
        self.c.execute('''UPDATE fantasy_nhl_player SET
        yahooEligibility = ?,
        avgPick = ?,
        avgRound = ?,
        percentDrafted = ?
        WHERE skaterFullName = ?''', (yahoo_info[1], yahoo_info[2], yahoo_info[3], yahoo_info[4], yahoo_info[0],))

        self.conn.commit()
        self.conn.close()

    def updateFantasyBadgeForFantasySkaterByPlayerId(self, fantasy_badge, playerId):
        self.c.execute('''UPDATE fantasy_nhl_player SET
        scoring = ?,
        playmaking = ?,
        defense = ?,
        powerplay = ?,
        intangibles = ?
        WHERE playerId = ?''', (fantasy_badge.scoring, fantasy_badge.playmaking, fantasy_badge.defense,
                                fantasy_badge.powerplay, fantasy_badge.intangibles, playerId,))

        self.conn.commit()
        self.conn.close()

    def removeTeamIdFromAllFantasySkates(self):
        self.c.execute('''UPDATE fantasy_nhl_player SET teamId = 0''')

        self.conn.commit()
        self.conn.close()

    @staticmethod
    def __convert_to_model(row):
        return FantasyNhlPlayer(row[0], row[1], row[2], row[3], row[4], row[5], row[6],
                                row[7], row[8], row[9], row[10],
                                badge=FantasyPlayerBadge(row[11], row[12], row[13], row[14], row[15]))

    @staticmethod
    def __convert_to_model_with_display_stat(row):
        return FantasyNhlPlayer(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10],
                                badge=FantasyPlayerBadge(row[11], row[12], row[13], row[14], row[15]),
                                stat=DisplayStat(
                                    row[16], row[17], row[18], row[19], row[20],
                                    row[21], row[22], row[23], row[24], row[25])
                                )
