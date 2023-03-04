import sqlite3
import pymysql

from server.internaldata.model.fantasy_player_streak_index import FantasyPlayerStreakIndex
from setting import Setting


class FantasyPlayerStreakIndexDao:

    def __init__(self, uri=None):
        # uri = 'server/internaldata/db/fantasy.db' if uri is None else uri
        # self.conn = sqlite3.connect(uri)
        # self.c = self.conn.cursor()
        self.conn = pymysql.connect(host=Setting.FREESQLDB_HOST,
                                    user=Setting.FREESQLDB_USERNAME,
                                    password=Setting.FREESQLDB_PASSWORD,
                                    db=Setting.FREESQLDB_DB,
                                    charset='utf8mb4',
                                    port=int(Setting.FREESQLDB_PORT),
                                    cursorclass=pymysql.cursors.DictCursor)
        # (driver='{SQL Server}', host="sql9.freesqldatabase.com", database="sql9602963",
        #                        trusted_connection="yes", user="sql9602963", password="qbRXwACteW", port="3306")
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
            '''INSERT IGNORE INTO fantasy_streak (playerId, 
            skaterFullName, 
            positionCode, 
            pts, 
            toi, 
            pptoi,
            streakIndex,
            lastUpdated
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)''',
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
            skaterFullName = ifnull(%s, skaterFullName), 
            positionCode = ifnull(%s, positionCode), 
            pts = ifnull(%s, pts), 
            toi = ifnull(%s, toi), 
            pptoi = ifnull(%s, pptoi),
            streakIndex = ifnull(%s, streakIndex),
            lastUpdated = ifnull(%s, lastUpdated)
            WHERE playerId = %s''',
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
        self.c.execute('''SELECT * FROM fantasy_streak WHERE playerId = %s''', (playerId,))

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
        self.c.execute('''DELETE FROM fantasy_streak WHERE playerId=%s''', (playerId,))

        self.conn.commit()
        self.conn.close()

    def deleteAllFantasySkaterStreak(self):
        self.c.execute('''DELETE FROM fantasy_streak''')

        self.conn.commit()
        self.conn.close()

    def __row_to_object(self, row):
        return FantasyPlayerStreakIndex(
            row.get("playerId", None),
            row.get("skaterFullName", None),
            row.get("positionCode", None),
            row.get("pts", None),
            row.get("toi", None),
            row.get("pptoi", None),
            row.get("streakIndex", None),
            row.get("lastUpdated", None))


if __name__ == "__main__":
    print(FantasyPlayerStreakIndexDao().getFantasyPlayerStreakIndex(8471218).__dict__)
