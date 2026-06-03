from dataclasses import dataclass
from typing import Optional

from domain.fantasyplayer.model.fantasy_nhl_player import FantasyNhlPlayer


@dataclass
class LocalizedString:
    default: str
    cs: Optional[str] = None
    de: Optional[str] = None
    es: Optional[str] = None
    fi: Optional[str] = None
    sk: Optional[str] = None
    sv: Optional[str] = None
    fr: Optional[str] = None

    def __init__(self, default: str, **kwargs):
        self.default = default
        for key, value in kwargs.items():
            setattr(self, key, value)



@dataclass
class PlayerInfo:
    id: int
    headshot: str
    firstName: LocalizedString
    lastName: LocalizedString
    sweaterNumber: int
    positionCode: str
    shootsCatches: str
    heightInInches: int
    weightInPounds: int
    heightInCentimeters: int
    weightInKilograms: int
    birthDate: str
    birthCity: LocalizedString
    birthCountry: str
    birthStateProvince: LocalizedString

    def full_name(self) -> str:
        return f"{self.firstName.default} {self.lastName.default}"

    def to_fantasy_player(self) -> "FantasyNhlPlayer":
        full_name = f"{self.firstName.default} {self.lastName.default}"
        return FantasyNhlPlayer(
            id=str(self.id),
            skaterFullName=full_name,
            positionCode=self.positionCode
        )