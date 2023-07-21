from sqlalchemy import and_

from server.internaldata.model.models import session, base, engine, InternalPlayerStat


class PlayerCardRepository:

    def __init__(self):
        # self.create_database()
        pass

    def create_database(self):
        base.metadata.create_all(engine)

    def get_internal_players_stats_by_playerId_and_seasonId(self, playerId, seasonId):
        return session.query(InternalPlayerStat) \
            .filter(and_(InternalPlayerStat.playerId == playerId,
                         InternalPlayerStat.seasonId == seasonId)).first()

    def save_internal_player_stats(self, player):
        stats = []
        stats += [
            InternalPlayerStat(
                playerId=player.playerId,
                seasonId=data.season,
                timeOnIce=data.stat.timeOnIce,
                assists=data.stat.assists,
                goals=data.stat.goals,
                pim=data.stat.pim,
                shots=data.stat.shots,
                games=data.stat.games,
                hits=data.stat.hits,
                powerPlayGoals=data.stat.powerPlayGoals,
                powerPlayPoints=data.stat.powerPlayPoints,
                powerPlayTimeOnIce=data.stat.powerPlayTimeOnIce,
                evenTimeOnIce=data.stat.evenTimeOnIce,
                penaltyMinutes=data.stat.penaltyMinutes,
                faceOffPct=data.stat.faceOffPct,
                shotPct=data.stat.shotPct,
                gameWinningGoals=data.stat.gameWinningGoals,
                overTimeGoals=data.stat.overTimeGoals,
                shortHandedGoals=data.stat.shortHandedGoals,
                shortHandedPoints=data.stat.shortHandedPoints,
                shortHandedTimeOnIce=data.stat.shortHandedTimeOnIce,
                blocked=data.stat.blocked,
                plusMinus=data.stat.plusMinus,
                points=data.stat.points,
                shifts=data.stat.shifts,
                timeOnIcePerGame=data.stat.timeOnIcePerGame,
                evenTimeOnIcePerGame=data.stat.evenTimeOnIcePerGame,
                shortHandedTimeOnIcePerGame=data.stat.shortHandedTimeOnIcePerGame,
                powerPlayTimeOnIcePerGame=data.stat.powerPlayTimeOnIcePerGame)
            for data in player.stats if data is not None]

        for stat in stats:
            try:
                session.add(stat)
                print(f"[{player.playerId}.{stat.seasonId}] Success!")
                session.commit()
            except Exception as e:
                print(f"[{player.playerId}.{stat.seasonId}] Unable to save season, {e}")

        session.close()

    def bulk_save_internal_players_stats(self, players):
        stats = []
        for player in players:
            stats += [
                InternalPlayerStat(
                    playerId=player.playerId,
                    seasonId=data.season,
                    timeOnIce=data.stat.timeOnIce,
                    assists=data.stat.assists,
                    goals=data.stat.goals,
                    pim=data.stat.pim,
                    shots=data.stat.shots,
                    games=data.stat.games,
                    hits=data.stat.hits,
                    powerPlayGoals=data.stat.powerPlayGoals,
                    powerPlayPoints=data.stat.powerPlayPoints,
                    powerPlayTimeOnIce=data.stat.powerPlayTimeOnIce,
                    evenTimeOnIce=data.stat.evenTimeOnIce,
                    penaltyMinutes=data.stat.penaltyMinutes,
                    faceOffPct=data.stat.faceOffPct,
                    shotPct=data.stat.shotPct,
                    gameWinningGoals=data.stat.gameWinningGoals,
                    overTimeGoals=data.stat.overTimeGoals,
                    shortHandedGoals=data.stat.shortHandedGoals,
                    shortHandedPoints=data.stat.shortHandedPoints,
                    shortHandedTimeOnIce=data.stat.shortHandedTimeOnIce,
                    blocked=data.stat.blocked,
                    plusMinus=data.stat.plusMinus,
                    points=data.stat.points,
                    shifts=data.stat.shifts,
                    timeOnIcePerGame=data.stat.timeOnIcePerGame,
                    evenTimeOnIcePerGame=data.stat.evenTimeOnIcePerGame,
                    shortHandedTimeOnIcePerGame=data.stat.shortHandedTimeOnIcePerGame,
                    powerPlayTimeOnIcePerGame=data.stat.powerPlayTimeOnIcePerGame)
                for data in player.stats if data is not None]
        session.bulk_save_objects(stats)
        session.commit()

    def delete_player_stat(self, playerId):
        session.query(InternalPlayerStat).filter(InternalPlayerStat.playerId == playerId).delete()
        session.commit()
