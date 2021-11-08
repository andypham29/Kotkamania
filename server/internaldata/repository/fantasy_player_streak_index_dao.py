import sqlite3

from server.internaldata.model.fantasy_player_streak_index import FantasyPlayerStreakIndex


class FantasyPlayerStreakIndexDao:

    def __init__(self, uri=None):
        uri = 'server/internaldata/db/fantasy.db' if uri is None else uri
        self.conn = sqlite3.connect(uri)
        self.c = self.conn.cursor()

    def initFantasyPlayerStreakIndexTable(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS fantasy_streak(
           playerId INTEGER PRIMARY KEY,
        skaterFullName TEXT NOT NULL,
        positionCode TEXT NOT NULL,
        pts INTEGER NOT NULL,
        toi DOUBLE NOT NULL,
        pptoi DOUBLE NOT NULL,
        streakIndex DOUBLE NOT NULL,
        lastUpdated TEXT
        );''')

        self.conn.commit()
        self.conn.close()

    def saveOrUpdateFantasyPlayerStreakIndex(self, fantasy_streak_info):
        self.c.execute(
            '''INSERT OR IGNORE INTO fantasy_streak (playerId, 
            skaterFullName, 
            positionCode, 
            pts, 
            toi, 
            pptoi,
            streakIndex,
            lastUpdated
            ) VALUES (?,?,?,?,?,?,?,?)''',
            (fantasy_streak_info.playerId,
             fantasy_streak_info.skaterFullName,
             fantasy_streak_info.positionCode,
             fantasy_streak_info.pts,
             fantasy_streak_info.toi,
             fantasy_streak_info.pptoi,
             fantasy_streak_info.index,
             fantasy_streak_info.lastUpdated
             ))

        self.c.execute(
            '''UPDATE fantasy_streak SET
            skaterFullName = ifnull(?, skaterFullName), 
            positionCode = ifnull(?, positionCode), 
            pts = ifnull(?, pts), 
            toi = ifnull(?, toi), 
            pptoi = ifnull(?, pptoi),
            streakIndex = ifnull(?, streakIndex),
            lastUpdated = ifnull(?, lastUpdated)
            WHERE playerId = ?''',
            (fantasy_streak_info.skaterFullName,
             fantasy_streak_info.positionCode,
             fantasy_streak_info.pts,
             fantasy_streak_info.toi,
             fantasy_streak_info.pptoi,
             fantasy_streak_info.index,
             fantasy_streak_info.lastUpdated,
             fantasy_streak_info.playerId,))

        self.conn.commit()
        self.conn.close()

    def getFantasyPlayerStreakIndex(self, playerId):
        self.c.execute('''SELECT * FROM fantasy_streak WHERE playerId = ?''', (playerId,))

        row = self.c.fetchone()

        self.conn.close()
        return self.__row_to_object(row)

    def getAllFantasyPlayerStreakIndexes(self):
        self.c.execute('''SELECT * FROM fantasy_streak ORDER BY streakIndex DESC''')

        records = self.c.fetchall()

        list = []
        for row in records:
            fantasy_skater = self.__row_to_object(row)
            list.append(fantasy_skater)

        self.conn.close()

        return list

    def getAllFantasyPlayerStreakIndexesByPositionCodes(self, positionCodes):
        positionCodes[:] = [value for value in positionCodes if value in ['L', 'C', 'R', 'D']]
        filter_parameters = str(positionCodes).replace('[', '(').replace(']', ')')

        query = f'''SELECT * FROM fantasy_streak 
            WHERE positionCode IN {filter_parameters} ORDER BY streakIndex DESC'''
        self.c.execute(query)

        records = self.c.fetchall()

        list = []
        for row in records:
            fantasy_skater = self.__row_to_object(row)
            list.append(fantasy_skater)

        self.conn.close()

        return list

    def getAllFantasyPlayerStreakIndexInPlayerIdList(self, playerIdList):
        filter_parameters = str(playerIdList).replace('[', '(').replace(']', ')')

        query = f'''SELECT * FROM fantasy_streak 
            WHERE playerId IN {filter_parameters}'''

        self.c.execute(query)

        records = self.c.fetchall()

        list = []
        for row in records:
            fantasy_skater = self.__row_to_object(row)
            list.append(fantasy_skater)

        self.conn.close()

        return list

    def getAllFantasySkatersBySearchName(self, name):
        self.c.execute(f"SELECT * FROM fantasy_streak WHERE skaterFullName LIKE \'%{name}%\'")

        records = self.c.fetchall()

        list = []
        for row in records:
            fantasy_skater = self.__row_to_object(row)
            list.append(fantasy_skater)

        self.conn.close()

        return list

    def deleteFantasySkaterById(self, playerId):
        self.c.execute('''DELETE FROM fantasy_streak WHERE playerId=?''', (playerId,))

        self.conn.commit()
        self.conn.close()

    def __row_to_object(self, row):
        return FantasyPlayerStreakIndex(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
