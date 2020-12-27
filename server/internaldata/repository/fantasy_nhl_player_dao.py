import sqlite3

from server.internaldata.model.fantasy_nhl_player import FantasyNhlPlayer


class FantasyNhlPlayerDao:

    def __init__(self):
        self.conn = sqlite3.connect('../../server/internaldata/db/fantasy.db')
        self.c = self.conn.cursor()

    def initFantasySkaterTable(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS fantasy_nhl_player(
            id INTEGER PRIMARY KEY,
        	name TEXT NOT NULL,
        	position TEXT NOT NULL,
        	teamId INTEGER NOT NULL,
        	fantasyGrade DOUBLE)''')

        self.conn.commit()
        self.conn.close()

    def saveFantasySkater(self, fantasy_skater):
        self.c.execute(
            '''INSERT INTO fantasy_nhl_player (id, name, position, teamId, fantasyGrade) VALUES (?,?,?,?,?)''',
            (fantasy_skater.id,
             fantasy_skater.name,
             fantasy_skater.position,
             fantasy_skater.teamId,
             fantasy_skater.fantasyGrade))

        self.conn.commit()
        self.conn.close()

    def getFantasySkaterById(self, id):
        self.c.execute('''SELECT * FROM fantasy_nhl_player WHERE id = ?''', (id,))

        row = self.c.fetchone()
        # for row in rows:
        #     print(row)

        self.conn.close()
        return FantasyNhlPlayer(row[0], row[1], row[2], row[3], row[4])

    def getAllFantasySkaters(self):
        self.c.execute('''SELECT * FROM fantasy_nhl_player''')

        records = self.c.fetchall()

        list = []
        for row in records:
            fantasy_skater = FantasyNhlPlayer(row[0], row[1], row[2], row[3], row[4])
            list.append(fantasy_skater)

        self.conn.close()

        return list

    def deleteFantasySkaterById(self, id):
        self.c.execute('''DELETE FROM fantasy_nhl_player WHERE id=?''', (id,))

        self.conn.commit()
        self.conn.close()

    def updateFantasyGradeForFantasySkaterWithId(self, id, grade):
        self.c.execute('''UPDATE fantasy_nhl_player SET
        fantasyGrade = ?
        WHERE id = ?''', (grade, id,))

        self.conn.commit()
        self.conn.close()
