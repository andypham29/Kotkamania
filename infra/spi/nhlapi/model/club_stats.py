from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class LocalizedName:
    default: str

    @classmethod
    def from_dict(cls, data: Dict) -> 'LocalizedName':
        return cls(default=data.get('default', ''))


@dataclass
class ClubSkaterStats:
    player_id: int
    headshot_url: str
    first_name: LocalizedName
    last_name: LocalizedName
    position_code: str
    games_played: int
    goals: int
    assists: int
    points: int
    plus_minus: int
    penalty_minutes: int
    power_play_goals: int
    shorthanded_goals: int
    game_winning_goals: int
    overtime_goals: int
    shots: int
    shooting_percentage: float
    average_time_on_ice_per_game: float
    average_shifts_per_game: float
    faceoff_win_percentage: float

    @classmethod
    def from_dict(cls, data: Dict) -> 'ClubSkaterStats':
        return cls(
            player_id=data.get('playerId'),
            headshot_url=data.get('headshot', ''),
            first_name=LocalizedName.from_dict(data.get('firstName', {})),
            last_name=LocalizedName.from_dict(data.get('lastName', {})),
            position_code=data.get('positionCode', ''),
            games_played=data.get('gamesPlayed', 0),
            goals=data.get('goals', 0),
            assists=data.get('assists', 0),
            points=data.get('points', 0),
            plus_minus=data.get('plusMinus', 0),
            penalty_minutes=data.get('penaltyMinutes', 0),
            power_play_goals=data.get('powerPlayGoals', 0),
            shorthanded_goals=data.get('shorthandedGoals', 0),
            game_winning_goals=data.get('gameWinningGoals', 0),
            overtime_goals=data.get('overtimeGoals', 0),
            shots=data.get('shots', 0),
            shooting_percentage=data.get('shootingPctg', 0.0),
            average_time_on_ice_per_game=data.get('avgTimeOnIcePerGame', 0.0),
            average_shifts_per_game=data.get('avgShiftsPerGame', 0.0),
            faceoff_win_percentage=data.get('faceoffWinPctg', 0.0),
        )


@dataclass
class ClubGoalieStats:
    player_id: int
    headshot_url: str
    first_name: LocalizedName
    last_name: LocalizedName
    games_played: int
    games_started: int
    wins: int
    losses: int
    overtime_losses: int
    goals_against_average: float
    save_percentage: float
    shots_against: int
    saves: int
    goals_against: int
    shutouts: int
    goals: int
    assists: int
    points: int
    penalty_minutes: Optional[int]
    time_on_ice: int

    @classmethod
    def from_dict(cls, data: Dict) -> 'ClubGoalieStats':
        return cls(
            player_id=data.get('playerId'),
            headshot_url=data.get('headshot', ''),
            first_name=LocalizedName.from_dict(data.get('firstName', {})),
            last_name=LocalizedName.from_dict(data.get('lastName', {})),
            games_played=data.get('gamesPlayed', 0),
            games_started=data.get('gamesStarted', 0),
            wins=data.get('wins', 0),
            losses=data.get('losses', 0),
            overtime_losses=data.get('overtimeLosses', 0),
            goals_against_average=data.get('goalsAgainstAverage', 0.0),
            save_percentage=data.get('savePercentage', 0.0),
            shots_against=data.get('shotsAgainst', 0),
            saves=data.get('saves', 0),
            goals_against=data.get('goalsAgainst', 0),
            shutouts=data.get('shutouts', 0),
            goals=data.get('goals', 0),
            assists=data.get('assists', 0),
            points=data.get('points', 0),
            penalty_minutes=data.get('penaltyMinutes'),
            time_on_ice=data.get('timeOnIce', 0),
        )


@dataclass
class ClubStatsResponse:
    season: str
    game_type: int
    skaters: List[ClubSkaterStats]
    goalies: List[ClubGoalieStats]

    @classmethod
    def from_dict(cls, data: Dict) -> 'ClubStatsResponse':
        return cls(
            season=data.get('season', ''),
            game_type=data.get('gameType'),
            skaters=[
                ClubSkaterStats.from_dict(skater)
                for skater in data.get('skaters', [])
            ],
            goalies=[
                ClubGoalieStats.from_dict(goalie)
                for goalie in data.get('goalies', [])
            ],
        )
