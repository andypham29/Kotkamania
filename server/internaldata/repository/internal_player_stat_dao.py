import sqlite3

from server.commons.helper.time_converter import TimeConverter
from server.internaldata.model.internal_nhl_player_stat import InternalPlayerStat


class InternalPlayerStatDao:
    def __init__(self, uri=None):
        uri = 'server/internaldata/db/internal.db' if uri is None else uri
        # uri = '../../server/internaldata/db/internal.db' if uri is None else uri
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
            if attr in ['timeOnIcePerGame', 'powerPlayTimeOnIcePerGame', 'evenTimeOnIcePerGame']:
                print(f"{attr} > {TimeConverter.convert_total_seconds_to_string(value.value)}")
                query += f' AND {attr} > "{TimeConverter.convert_total_seconds_to_string(value.value)}"'
            else:
                query += f" AND {attr} > {value.value} * games"
        print(query)
        self.c.execute(query)
        records = self.c.fetchall()

        list = []
        for row in records:
            list.append(self.__row_to_object(row))
        self.conn.close()
        print("[Percentile Filter] fetched number of rows: ", len(list))
        return list

    def insert_internal_players_stats(self, playerId, seasonId, stat):
        self.c.execute(
            f'''INSERT OR IGNORE INTO internal_player_stat (playerId,
            seasonId,
            timeOnIce,
            assists,
            goals,
            pim,
            shots,
            games,
            hits,
            powerPlayGoals,
            powerPlayPoints,
            powerPlayTimeOnIce,
            evenTimeOnIce,
            penaltyMinutes,
            faceOffPct,
            shotPct,
            gameWinningGoals,
            overTimeGoals,
            shortHandedGoals,
            shortHandedPoints,
            shortHandedTimeOnIce,
            blocked,
            plusMinus,
            points,
            shifts,
            timeOnIcePerGame,
            evenTimeOnIcePerGame,
            shortHandedTimeOnIcePerGame,
            powerPlayTimeOnIcePerGame
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
            (playerId,
             seasonId,
             stat.timeOnIce,
             stat.assists,
             stat.goals,
             stat.pim,
             stat.shots,
             stat.games,
             stat.hits,
             stat.powerPlayGoals,
             stat.powerPlayPoints,
             stat.powerPlayTimeOnIce,
             stat.evenTimeOnIce,
             stat.penaltyMinutes,
             stat.faceOffPct,
             stat.shotPct,
             stat.gameWinningGoals,
             stat.overTimeGoals,
             stat.shortHandedGoals,
             stat.shortHandedPoints,
             stat.shortHandedTimeOnIce,
             stat.blocked,
             stat.plusMinus,
             stat.points,
             stat.shifts,
             stat.timeOnIcePerGame,
             stat.evenTimeOnIcePerGame,
             stat.shortHandedTimeOnIcePerGame,
             stat.powerPlayTimeOnIcePerGame,))

        self.conn.commit()
        self.conn.close()

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
