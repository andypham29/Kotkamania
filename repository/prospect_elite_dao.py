import sqlite3

class ProspectEliteDao:

    def __init__(self):
        self.conn = sqlite3.connect('db/elite.db')
        self.c = self.conn.cursor()

    def initProspectEliteTable(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS prospectelite(
            id INTEGER PRIMARY KEY,
            name_position VARCHAR NOT NULL UNIQUE,
            hp VARCHAR,
            fc VARCHAR,
            iss VARCHAR,
            mh VARCHAR,
            elite VARCHAR)''')

        self.conn.commit()
        self.conn.close()

    def getAllProspects(self):
        self.c.execute('''SELECT * FROM prospectelite''')

        records = self.c.fetchall()
        #
        # list = []
        # for row in records:
        #     prospect = Prospect(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        #     list.append(prospect)

        self.conn.close()

        return records

    def createProspectElite(self, prospect):
        self.c.execute('''INSERT INTO prospectelite (name_position, hp, fc, iss, mh, elite) VALUES (?,?,?,?,?,?,?)''',
        (prospect.name_position,
        prospect.hp,
        prospect.fc,
        prospect.iss,
        prospect.mh,
        prospect.elite))

        self.conn.commit()
        self.conn.close()

    def insertOrUpdateProspectElite(self, prospect):
        self.c.execute('''INSERT OR IGNORE INTO prospectelite (name_position, hp, fc, iss, mh, elite) VALUES (?,?,?,?,?,?)''',
            (prospect.name_position,
            prospect.hp,
            prospect.fc,
            prospect.iss,
            prospect.mh,
            prospect.elite))

        self.c.execute('''UPDATE prospectelite SET
            name_position = ifnull(?, name_position),
            hp = ifnull(?, hp),
            fc = ifnull(?, fc),
            iss = ifnull(?, iss),
            mh = ifnull(?, mh),
            elite = ifnull(?, elite)  WHERE name_position = ?''',
            (prospect.name_position,
            prospect.hp,
            prospect.fc,
            prospect.iss,
            prospect.mh,
            prospect.elite,
            prospect.name_position))

        self.conn.commit()
        self.conn.close()

    def updateProspectEliteHP(self, rank, name_position):
        self.c.execute('''UPDATE prospectelite SET hp = ? WHERE name_position = ?;''', (rank, name_position))

        self.conn.commit()
        self.conn.close()

    def updateProspectEliteFC(self, rank, name_position):
        self.c.execute('''UPDATE prospectelite SET fc = ? WHERE name_position = ?;''', (rank, name_position))

        self.conn.commit()
        self.conn.close()

    def updateProspectEliteISS(self, rank, name_position):
        self.c.execute('''UPDATE prospectelite SET iss = ? WHERE name_position = ?;''', (rank, name_position))

        self.conn.commit()
        self.conn.close()

    def updateProspectEliteMH(self, rank, name_position):
        self.c.execute('''UPDATE prospectelite SET mh = ? WHERE name_position = ?;''', (rank, name_position))

        self.conn.commit()
        self.conn.close()

    def updateProspectEliteElite(self, rank, name_position):
        self.c.execute('''UPDATE prospectelite SET elite = ? WHERE name_position = ?;''', (rank, name_position))

        self.conn.commit()
        self.conn.close()
