import sqlite3
from server.model.prospect import ProspectElite

class ProspectEliteDao:

    def __init__(self, year = "2020"):
        self.tablename = f"eliteprospect{year}"
        self.conn = sqlite3.connect('server/db/eliteprospect.db')
        self.c = self.conn.cursor()

    def initProspectEliteTable(self):
        self.c.execute(f'''CREATE TABLE IF NOT EXISTS {self.tablename}(
            id INTEGER PRIMARY KEY,
            name VARCHAR NOT NULL UNIQUE,
            position VARCHAR,
            hp VARCHAR,
            fc VARCHAR,
            iss VARCHAR,
            mh VARCHAR,
            elite VARCHAR,
            league VARCHAR,
            team VARCHAR,
            gp VARCHAR,
            g VARCHAR,
            a VARCHAR,
            p VARCHAR,
            pim VARCHAR
            )''')

        self.conn.commit()
        self.conn.close()

    def getProspectById(self, id):
        self.c.execute(f'''SELECT * FROM {self.tablename} WHERE id = ?''', (id,))

        row = self.c.fetchone()
        # for row in rows:
        #     print(row)

        self.conn.close()
        return ProspectElite(id=row[0], name=row[1], position=row[2], hp=row[3], fc=row[4], iss=row[5], mh=row[6], elite=row[7], league=row[8], team=row[9], gp=row[10], g=row[11], a=row[12], p=row[13], pim=row[14])

    def getAllProspects(self):
        self.c.execute(f'''SELECT * FROM {self.tablename}''')
        records = self.c.fetchall()

        list = []
        for row in records:
            prospect = ProspectElite(id=row[0], name=row[1], position=row[2], hp=row[3], fc=row[4], iss=row[5], mh=row[6], elite=row[7], league=row[8], team=row[9], gp=row[10], g=row[11], a=row[12], p=row[13], pim=row[14])
            list.append(prospect)

        self.conn.commit()
        self.conn.close()

        return list
    
    def getAllProspectsWithRanking(self):
        self.c.execute(f'''SELECT * FROM {self.tablename} WHERE
            hp NOT LIKE '%-%' OR
            fc NOT LIKE '%-%' OR
            iss NOT LIKE '%-%' OR
            mh NOT LIKE '%-%' OR
            elite NOT LIKE '%-%'
        ''')
        records = self.c.fetchall()

        list = []
        for row in records:
            prospect = ProspectElite(id=row[0], name=row[1], position=row[2], hp=row[3], fc=row[4], iss=row[5], mh=row[6], elite=row[7], league=row[8], team=row[9], gp=row[10], g=row[11], a=row[12], p=row[13], pim=row[14])
            list.append(prospect)

        self.conn.commit()
        self.conn.close()

        return list

    def getProspectsAtPage(self, page=1):
        if page < 1:
            raise Exception("Error fetching prospects")
        self.c.execute(f'''SELECT * FROM {self.tablename} LIMIT 20*{page-1},20''')
        records = self.c.fetchall()

        list = []
        for row in records:
            prospect = ProspectElite(id=row[0], name=row[1], position=row[2], hp=row[3], fc=row[4], iss=row[5], mh=row[6], elite=row[7], league=row[8], team=row[9], gp=row[10], g=row[11], a=row[12], p=row[13], pim=row[14])
            list.append(prospect)

        self.conn.commit()
        self.conn.close()

        return list

    def insertOrUpdateProspectElite(self, prospect):
        self.c.execute(f'''INSERT OR IGNORE INTO {self.tablename} (name, position, hp, fc, iss, mh, elite, league, team, gp, g, a, p, pim) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
            (prospect.name,
            prospect.position,
            prospect.hp,
            prospect.fc,
            prospect.iss,
            prospect.mh,
            prospect.elite,
            prospect.league,
            prospect.team,
            prospect.gp,
            prospect.g,
            prospect.a,
            prospect.p,
            prospect.pim))

        self.c.execute(f'''UPDATE {self.tablename} SET
            hp = ifnull(?, hp),
            fc = ifnull(?, fc),
            iss = ifnull(?, iss),
            mh = ifnull(?, mh),
            elite = ifnull(?, elite),
            league = ifnull(?, league),
            team = ifnull(?, team),
            gp = ifnull(?, gp),
            g = ifnull(?, g),
            a = ifnull(?, a),
            p = ifnull(?, p),
            pim = ifnull(?, pim)
            WHERE name = ?''',
            (prospect.hp,
            prospect.fc,
            prospect.iss,
            prospect.mh,
            prospect.elite,
            prospect.league,
            prospect.team,
            prospect.gp,
            prospect.g,
            prospect.a,
            prospect.p,
            prospect.pim,
            prospect.name))

        self.conn.commit()
        self.conn.close()
