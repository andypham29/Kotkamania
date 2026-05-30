from dataclasses import dataclass
from typing import Optional




@dataclass
class Team:
    id: Optional[int] = None,
    franchiseId: Optional[int] = None,
    fullName: Optional[str] = None,
    leagueId: Optional[int] = None,
    rawTricode: Optional[str] = None
    triCode: Optional[str] = None

