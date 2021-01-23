import sqlite3

from server.internaldata.model.internal_nhl_player_stat import InternalPlayerStat


class InternalPlayerStatDao:
    def __init__(self, uri=None):
        uri = 'server/internaldata/db/internal.db' if uri is None else uri
        self.conn = sqlite3.connect(uri)
        self.c = self.conn.cursor()

    def get_internal_players_stats_by_playerId_and_seasonId(self, playerId, seasonId):
        self.c.execute("SELECT * FROM internal_player_stat WHERE playerId=? AND seasonId=?", (playerId, seasonId,))
        row = self.c.fetchone()

        if not row:
            return None
        self.conn.close()
        return self.__row_to_object(row)

    def get_internal_players_stats_at_percentile_values_and_seasonId(self, percentile_values, seasonId):
        query = f'SELECT * FROM internal_player_stat WHERE seasonId=\"{seasonId}\"'
        for attr, value in percentile_values.__dict__.items():
            if value.percentile is None:
                continue
            query += f" AND {attr} > {value.value}"
        self.c.execute(query)
        records = self.c.fetchall()

        list = []
        for row in records:
            list.append(self.__row_to_object(row))
        self.conn.close()
        return list

    def __row_to_object(self, row):
        return InternalPlayerStat(
            playerId=row[1],
            seasonId=row[2],
            timeOnIce=None,
            assists=row[3],
            goals=row[4],
            pim=row[5],
            shots=row[6],
            games=row[7],
            hits=row[8],
            powerPlayGoals=row[9],
            powerPlayPoints=row[10],
            powerPlayTimeOnIce=row[11],
            evenTimeOnIce=row[12],
            penaltyMinutes=row[13],
            faceOffPct=row[14],
            shotPct=row[15],
            gameWinningGoals=row[16],
            overTimeGoals=row[17],
            shortHandedGoals=row[18],
            shortHandedPoints=row[19],
            shortHandedTimeOnIce=row[20],
            blocked=row[21],
            plusMinus=row[22],
            points=row[23],
            shifts=row[24],
            timeOnIcePerGame=row[25],
            evenTimeOnIcePerGame=row[26],
            shortHandedTimeOnIcePerGame=row[27],
            powerPlayTimeOnIcePerGame=row[28])
