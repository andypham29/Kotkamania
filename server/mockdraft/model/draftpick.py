from dataclasses import dataclass, field
from server.mockdraft.model.prospect import ProspectElite


@dataclass
class DraftPick:
    pick: int = 0
    team: str = ""
    player: ProspectElite = field(default_factory=ProspectElite)
    odds: int = 0
    list_ball: list = field(default_factory=list)
    picked_ball: int = 0
    prospectlist: list = field(default_factory=list)
