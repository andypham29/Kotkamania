from dataclasses import dataclass


@dataclass
class LeaderPlayer:
    assists: int
    evGoals: int
    evPoints: int
    faceoffWinPct: float
    gameWinningGoals: int
    gamesPlayed: int
    goals: int
    lastName: str
    otGoals: int
    penaltyMinutes: int
    playerId: int
    plusMinus: int
    points: int
    pointsPerGame: float
    positionCode: str
    ppGoals: int
    ppPoints: int
    seasonId: int
    shGoals: int
    shPoints: int
    shootingPct: float
    shootsCatches: str
    shots: int
    skaterFullName: str
    teamAbbrevs: str
    timeOnIcePerGame: str
