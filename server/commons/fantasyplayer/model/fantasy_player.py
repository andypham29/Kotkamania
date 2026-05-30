from dataclasses import dataclass
from typing import Optional


@dataclass
class FantasyPlayer:
    id: str = ""
    name: str = ""
    games: str = ""
    goals: str = ""
    assists: str = ""
    points: str = ""
    shotPctIndex: str = ""
    score: str = ""
    pptoi: str = ""
    badge: Optional[str] = None
