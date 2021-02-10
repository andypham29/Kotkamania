import sqlite3


class InternalLogDao:

    def __init__(self, uri=None):
        uri = 'server/admin/db/log.db' if uri is None else uri
        self.conn = sqlite3.connect(uri)
        self.c = self.conn.cursor()

    def initNhlPlayerStatLogTable(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS nhl_player_stat_log(
           id INTEGER PRIMARY KEY,
        	date DATE NOT NULL UNIQUE,
        	description TEXT
        	)''')

        self.conn.commit()
        self.conn.close()

    def getNhlPlayerStatLogByDate(self, date):
        self.c.execute('''SELECT * FROM nhl_player_stat_log WHERE date = ?''', (date,))

        row = self.c.fetchone()

        self.conn.close()
        return NhlPlayerStatLog(row[1], row[2])

    def saveNhlPlayerStatLog(self, log):
        self.c.execute(
            '''INSERT INTO nhl_player_stat_log (
            date, 
            description) VALUES (?,?)''',
            (log.date,
             log.description,))

        self.conn.commit()
        self.conn.close()


class NhlPlayerStatLog:

    def __init__(self, date, description):
        self.date = date
        self.description = description
