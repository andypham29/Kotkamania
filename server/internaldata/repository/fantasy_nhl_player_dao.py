import sqlite3

from server.internaldata.model.fantasy_nhl_player import FantasyNhlPlayer


class FantasyNhlPlayerDao:

    def __init__(self, uri=None):
        uri = 'server/internaldata/db/fantasy.db' if uri is None else uri
        self.conn = sqlite3.connect(uri)
        self.c = self.conn.cursor()

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
        	percentDrafted TEXT
        	teamName TEXT NOT NULL,
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
            percentDrafted) VALUES (?,?,?,?,?,?,?,?,?,?)''',
            (fantasy_skater.playerId,
             fantasy_skater.skaterFullName,
             fantasy_skater.positionCode,
             fantasy_skater.teamId,
             fantasy_skater.teamName,
             fantasy_skater.fantasyGrade,
             fantasy_skater.yahooEligibility,
             fantasy_skater.avgPick,
             fantasy_skater.avgRound,
             fantasy_skater.percentDrafted))

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
            percentDrafted = ifnull(?, percentDrafted)
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
             fantasy_skater.playerId))

        self.conn.commit()
        self.conn.close()

    def getFantasySkaterById(self, playerId):
        self.c.execute('''SELECT * FROM fantasy_nhl_player WHERE playerId = ?''', (playerId,))

        row = self.c.fetchone()

        self.conn.close()
        return FantasyNhlPlayer(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])

    def getAllFantasySkaters(self):
        self.c.execute('''SELECT * FROM fantasy_nhl_player''')

        records = self.c.fetchall()

        list = []
        for row in records:
            fantasy_skater = FantasyNhlPlayer(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8],
                                              row[9])
            list.append(fantasy_skater)

        self.conn.close()

        return list

    def getAllFantasySkatersByPositionCodes(self, positionCodes):
        positionCodes[:] = [value for value in positionCodes if value in ['L', 'C', 'R', 'D', 'G']]
        filter_parameters = str(positionCodes).replace('[', '(').replace(']', ')')

        query = f'''SELECT * FROM fantasy_nhl_player 
            WHERE positionCode IN {filter_parameters}'''
        for position in positionCodes:
            query += f" OR yahooEligibility LIKE '%{position}%'"
        self.c.execute(query)

        records = self.c.fetchall()

        list = []
        for row in records:
            fantasy_skater = FantasyNhlPlayer(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8],
                                              row[9])
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
            fantasy_skater = FantasyNhlPlayer(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8],
                                              row[9])
            list.append(fantasy_skater)

        self.conn.close()

        return list

    def getAllFantasySkatersByTeamId(self, teamId):
        self.c.execute('''SELECT * FROM fantasy_nhl_player WHERE teamId=?''', (teamId,))

        records = self.c.fetchall()

        list = []
        for row in records:
            fantasy_skater = FantasyNhlPlayer(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8],
                                              row[9])
            list.append(fantasy_skater)

        self.conn.close()

        return list

    def getAllFantasySkatersBySearchName(self, name):
        self.c.execute(f"SELECT * FROM fantasy_nhl_player WHERE skaterFullName LIKE \'%{name}%\'")

        records = self.c.fetchall()

        list = []
        for row in records:
            fantasy_skater = FantasyNhlPlayer(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8],
                                              row[9])
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

    def updateFantasyYahooInfoForFantasySkater(self, yahoo_info):
        self.c.execute('''UPDATE fantasy_nhl_player SET
        yahooEligibility = ?,
        avgPick = ?,
        avgRound = ?,
        percentDrafted = ?
        WHERE skaterFullName = ?''', (yahoo_info[1], yahoo_info[2], yahoo_info[3], yahoo_info[4], yahoo_info[0],))

        self.conn.commit()
        self.conn.close()
