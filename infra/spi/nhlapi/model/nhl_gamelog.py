from dataclasses import dataclass
from typing import Optional


@dataclass
class CommonName:
    default: Optional[str] = None


@dataclass
class GameLog:
    gameId: int
    teamAbbrev: str
    homeRoadFlag: str
    gameDate: str
    goals: int
    assists: int
    commonName: Optional[CommonName]
    opponentCommonName: Optional[CommonName]
    points: int
    plusMinus: int
    powerPlayGoals: int
    powerPlayPoints: int
    gameWinningGoals: int
    otGoals: int
    shots: int
    shifts: int
    shorthandedGoals: int
    shorthandedPoints: int
    opponentAbbrev: str
    pim: int
    toi: str
