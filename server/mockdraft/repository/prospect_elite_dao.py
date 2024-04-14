import sqlite3

from server.mockdraft.model.prospect import ProspectElite
from setting import Setting


class ProspectEliteDao:

    def __init__(self, year=Setting.NHL_YEAR):
        self.tablename = f"eliteprospect{year}"
        self.conn = sqlite3.connect('server/mockdraft/db/eliteprospect.db')
        self.c = self.conn.cursor()

    def initProspectEliteTable(self):
        self.c.execute(f'''CREATE TABLE IF NOT EXISTS {self.tablename}(
            id INTEGER PRIMARY KEY,
            name VARCHAR NOT NULL UNIQUE,
            position VARCHAR,
            avg_rank VARCHAR,
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

        self.conn.close()
        return ProspectElite(id=row[0], name=row[1], position=row[2], avg_rank=row[3], hp=row[4], fc=row[5], iss=row[6],
                             mh=row[7], elite=row[8], league=row[9], team=row[10], gp=row[11], g=row[12], a=row[13],
                             p=row[14], pim=row[15])

    def getProspectByPosition(self, position, page):
        query = f'''SELECT * FROM {self.tablename} WHERE position LIKE '%{position}%' ORDER BY CAST(avg_rank AS UNSIGNED) IS NULL ASC'''

        if int(page) > 0:
            query += f'LIMIT 20*{page}, 20'

        print(query)
        self.c.execute(query)
        records = self.c.fetchall()
        list = []
        print("records", len(records))
        for row in records:
            prospect = ProspectElite(id=row[0], name=row[1], position=row[2], avg_rank=row[3], hp=row[4], fc=row[5],
                                     iss=row[6], mh=row[7], elite=row[8], league=row[9], team=row[10], gp=row[11],
                                     g=row[12], a=row[13], p=row[14], pim=row[15])
            list.append(prospect)

        self.conn.commit()
        self.conn.close()

        return list

    def getAllProspects(self):
        self.c.execute(f'''SELECT * FROM {self.tablename}''')
        records = self.c.fetchall()

        list = []
        for row in records:
            prospect = ProspectElite(id=row[0], name=row[1], position=row[2], avg_rank=row[3], hp=row[4], fc=row[5],
                                     iss=row[6], mh=row[7], elite=row[8], league=row[9], team=row[10], gp=row[11],
                                     g=row[12], a=row[13], p=row[14], pim=row[15])
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
            ORDER BY CAST(avg_rank AS UNSIGNED) ASC

        ''')
        records = self.c.fetchall()

        list = []
        for row in records:
            prospect = ProspectElite(id=row[0], name=row[1], position=row[2], avg_rank=row[3], hp=row[4], fc=row[5],
                                     iss=row[6], mh=row[7], elite=row[8], league=row[9], team=row[10], gp=row[11],
                                     g=row[12], a=row[13], p=row[14], pim=row[15])
            list.append(prospect)

        self.conn.commit()
        self.conn.close()

        return list

    def getProspectsAtPage(self, page=1):
        if int(page) < 1:
            raise Exception("Error fetching prospects")
        self.c.execute(
            f'''SELECT * FROM {self.tablename} ORDER BY avg_rank IS NULL, CAST(avg_rank AS UNSIGNED) ASC LIMIT 20*{int(page) - 1},20''')
        records = self.c.fetchall()

        list = []
        for row in records:
            prospect = ProspectElite(id=row[0], name=row[1], position=row[2], avg_rank=row[3], hp=row[4], fc=row[5],
                                     iss=row[6], mh=row[7], elite=row[8], league=row[9], team=row[10], gp=row[11],
                                     g=row[12], a=row[13], p=row[14], pim=row[15])
            list.append(prospect)

        self.conn.commit()
        self.conn.close()

        return list

    def insertOrUpdateProspectElite(self, prospect):
        self.c.execute(
            f'''INSERT OR IGNORE INTO {self.tablename} (name, position, hp, fc, iss, mh, elite, league, team, gp, g, a, p, pim) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
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

    def updateProspectEliteAvgRank(self, prospect):
        self.c.execute(f'''UPDATE {self.tablename} SET
            avg_rank = ?
            WHERE name = ?''',
                       (prospect.avg_rank,
                        prospect.name))

        self.conn.commit()
        self.conn.close()
