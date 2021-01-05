from sqlalchemy import or_

from server.internaldata.model.models import InternalPlayer, session, base, engine


class InternalPlayerRepository:

    def __init__(self):
        # self.create_database()
        pass

    def create_database(self):
        base.metadata.create_all(engine)

    def save_internal_players(self, players):
        internal_players = [
            InternalPlayer(
                assists=player.assists,
                evGoals=player.evGoals,
                evPoints=player.evPoints,
                faceoffWinPct=player.faceoffWinPct,
                gameWinningGoals=player.gameWinningGoals,
                gamesPlayed=player.gamesPlayed,
                goals=player.goals,
                lastName=player.lastName,
                otGoals=player.otGoals,
                penaltyMinutes=player.penaltyMinutes,
                playerId=player.playerId,
                plusMinus=player.plusMinus,
                points=player.points,
                pointsPerGame=player.pointsPerGame,
                positionCode=player.positionCode,
                ppGoals=player.ppGoals,
                ppPoints=player.ppPoints,
                seasonId=player.seasonId,
                shGoals=player.shGoals,
                shPoints=player.shPoints,
                shootingPct=player.shootingPct,
                shootsCatches=player.shootsCatches,
                shots=player.shots,
                skaterFullName=player.skaterFullName,
                teamAbbrevs=player.teamAbbrevs,
                timeOnIcePerGame=player.timeOnIcePerGame)
            for player in players]
        session.bulk_save_objects(internal_players)
        session.commit()

    def get_all_players(self):
        return session.query(InternalPlayer).all()

    def get_defensemen(self, amount=150):
        return session.query(InternalPlayer) \
                   .order_by(InternalPlayer.points.desc()) \
                   .filter(InternalPlayer.positionCode == 'D')[:amount]

    def get_forwards(self, amount=300):
        return session.query(InternalPlayer) \
                   .order_by(InternalPlayer.points.desc()) \
                   .filter(or_(InternalPlayer.positionCode == 'L',
                               InternalPlayer.positionCode == 'R',
                               InternalPlayer.positionCode == 'C'))[:amount]
