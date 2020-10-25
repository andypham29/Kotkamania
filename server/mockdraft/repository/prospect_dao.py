import sqlite3
from server.mockdraft.model.prospect import Prospect


class ProspectDao:

    def __init__(self):
        self.conn = sqlite3.connect('server/mockdraft/db/example.db')
        self.c = self.conn.cursor()

    def initProspectTable(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS prospects(
            id INTEGER PRIMARY KEY,
        	rank TEXT NOT NULL,
        	player_name TEXT NOT NULL,
        	height TEXT NOT NULL,
        	weight TEXT NOT NULL,
        	position TEXT NOT NULL,
        	team TEXT NOT NULL,
        	league TEXT NOT NULL)''')

        self.conn.commit()
        self.conn.close()

    def createProspect(self, prospect):
        self.c.execute(
            '''INSERT INTO prospects (rank, player_name, height, weight, position, team, league) VALUES (?,?,?,?,?,?,?)''',
            (prospect.rank,
             prospect.player_name,
             prospect.height,
             prospect.weight,
             prospect.position,
             prospect.team,
             prospect.league))

        self.conn.commit()
        self.conn.close()

    def getProspectById(self, id):
        self.c.execute('''SELECT * FROM prospects WHERE id = ?''', (id,))

        row = self.c.fetchone()
        # for row in rows:
        #     print(row)

        self.conn.close()
        return Prospect(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])

    def getAllProspects(self):
        self.c.execute('''SELECT * FROM prospects''')

        records = self.c.fetchall()

        list = []
        for row in records:
            prospect = Prospect(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            list.append(prospect)

        self.conn.close()

        return list

    def deleteProspectById(self, id):
        self.c.execute('''DELETE FROM tasks WHERE id=?''', (id,))

        self.conn.commit()
        self.conn.close()
