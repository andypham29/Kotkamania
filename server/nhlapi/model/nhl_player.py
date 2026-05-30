from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class PlayerDraftDetails:
    year: int
    teamAbbrev: str
    draftRound: int
    pickInRound: int
    overallPick: int


@dataclass
class PlayerStat:
    timeOnIce: Optional[str] = None
    assists: Optional[int] = None
    goals: Optional[int] = None
    pim: Optional[int] = None
    shots: Optional[int] = None
    games: Optional[int] = None
    hits: Optional[int] = None
    powerPlayGoals: Optional[int] = None
    powerPlayPoints: Optional[int] = None
    powerPlayTimeOnIce: Optional[str] = None
    evenTimeOnIce: Optional[str] = None
    penaltyMinutes: Optional[int] = None
    faceOffPct: Optional[float] = None
    shotPct: float = 0.0
    gameWinningGoals: Optional[int] = None
    overTimeGoals: Optional[int] = None
    shortHandedGoals: Optional[int] = None
    shortHandedPoints: Optional[int] = None
    shortHandedTimeOnIce: Optional[str] = None
    blocked: Optional[int] = None
    plusMinus: Optional[int] = None
    points: Optional[int] = None
    shifts: Optional[int] = None
    timeOnIcePerGame: Optional[str] = None
    evenTimeOnIcePerGame: Optional[str] = None
    shortHandedTimeOnIcePerGame: Optional[str] = None
    powerPlayTimeOnIcePerGame: Optional[str] = None


@dataclass
class GoalieStat:
    timeOnIce: str
    ot: int
    shutouts: int
    ties: int
    wins: int
    losses: int
    saves: int
    powerPlaySaves: int
    shortHandedSaves: int
    evenSaves: int
    shortHandedShots: int
    evenShots: int
    powerPlayShots: int
    savePercentage: float
    goalAgainstAverage: float
    games: int
    gamesStarted: int
    shotsAgainst: int
    goalsAgainst: int
    timeOnIcePerGame: str
    powerPlaySavePercentage: float
    shortHandedSavePercentage: float
    evenStrengthSavePercentage: float


@dataclass
class SeasonStat:
    season: str
    stat: PlayerStat | GoalieStat


@dataclass
class Player:
    playerId: int
    fullName: str
    position: str
    teamId: int
    team: str
    primaryNumber: Optional[str]
    birthDate: str
    currentAge: int
    birthCity: str
    birthCountry: str
    height: str
    weight: int
    shootCatches: str
    stats: List[SeasonStat] = field(default_factory=list)
    badge: Optional[str] = None
    playerDraftDetails: Optional[PlayerDraftDetails] = None
