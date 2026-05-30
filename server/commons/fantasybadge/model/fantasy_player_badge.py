from dataclasses import dataclass


@dataclass
class FantasyPlayerBadge:
    scoring: int = 0
    playmaking: int = 0
    defense: int = 0
    powerplay: int = 0
    intangibles: int = 0
