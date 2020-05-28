import sqlite3
from model.prospect import ProspectElite

class ProspectEliteDao:

    def __init__(self, year = "2020"):
        self.tablename = f"eliteprospect{year}"
        self.conn = sqlite3.connect('db/elite.db')
        self.c = self.conn.cursor()

    def initProspectEliteTable(self):
        self.c.execute(f'''CREATE TABLE IF NOT EXISTS {self.tablename}(
            id INTEGER PRIMARY KEY,
            name_position VARCHAR NOT NULL UNIQUE,
            hp VARCHAR,
            fc VARCHAR,
            iss VARCHAR,
            mh VARCHAR,
            elite VARCHAR)''')

        self.conn.commit()
        self.conn.close()

    def getProspectById(self, id):
        self.c.execute(f'''SELECT * FROM {self.tablename} WHERE id = ?''', (id,))

        row = self.c.fetchone()
        # for row in rows:
        #     print(row)

        self.conn.close()
        return ProspectElite(id=row[0], name_position=row[1], hp=row[2], fc=row[3], iss=row[4], mh=row[5], elite=row[6])

    def getAllProspects(self):
        self.c.execute(f'''SELECT * FROM {self.tablename}''')
        records = self.c.fetchall()

        list = []
        for row in records:
            prospect = ProspectElite(id=row[0], name_position=row[1], hp=row[2], fc=row[3], iss=row[4], mh=row[5], elite=row[6])
            list.append(prospect)

        self.conn.close()

        return list

    def createProspectElite(self, prospect):
        self.c.execute(f'''INSERT INTO {self.tablename} (name_position, hp, fc, iss, mh, elite) VALUES (?,?,?,?,?,?,?)''',
        (prospect.name_position,
        prospect.hp,
        prospect.fc,
        prospect.iss,
        prospect.mh,
        prospect.elite))

        self.conn.commit()
        self.conn.close()

    def insertOrUpdateProspectElite(self, prospect):
        self.c.execute(f'''INSERT OR IGNORE INTO {self.tablename} (name_position, hp, fc, iss, mh, elite) VALUES (?,?,?,?,?,?)''',
            (prospect.name_position,
            prospect.hp,
            prospect.fc,
            prospect.iss,
            prospect.mh,
            prospect.elite))

        self.c.execute(f'''UPDATE {self.tablename} SET
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
        self.c.execute(f'''UPDATE {self.tablename} SET hp = ? WHERE name_position = ?;''', (rank, name_position))

        self.conn.commit()
        self.conn.close()

    def updateProspectEliteFC(self, rank, name_position):
        self.c.execute(f'''UPDATE {self.tablename} SET fc = ? WHERE name_position = ?;''', (rank, name_position))

        self.conn.commit()
        self.conn.close()

    def updateProspectEliteISS(self, rank, name_position):
        self.c.execute(f'''UPDATE {self.tablename} SET iss = ? WHERE name_position = ?;''', (rank, name_position))

        self.conn.commit()
        self.conn.close()

    def updateProspectEliteMH(self, rank, name_position):
        self.c.execute(f'''UPDATE {self.tablename} SET mh = ? WHERE name_position = ?;''', (rank, name_position))

        self.conn.commit()
        self.conn.close()

    def updateProspectEliteElite(self, rank, name_position):
        self.c.execute(f'''UPDATE {self.tablename} SET elite = ? WHERE name_position = ?;''', (rank, name_position))

        self.conn.commit()
        self.conn.close()
