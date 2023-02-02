from dataclasses import dataclass
from enum import Enum
from typing import NamedTuple


@dataclass
class Plan:
    id: str
    year: int


class PotentialRange(NamedTuple):
    min: int | None
    max: int | float | None


class Potential(Enum):
    dS = PotentialRange(6000, float('inf'))
    dA = PotentialRange(1500, 5999)
    dB = PotentialRange(300, 1499)
    dC = PotentialRange(1, 299)
    d0 = PotentialRange(0, 0)
    dR = PotentialRange(None, None)
    bS = PotentialRange(6000, float('inf'))
    bA = PotentialRange(1500, 5999)
    bB = PotentialRange(300, 1499)
    bC = PotentialRange(1, 299)
    b0 = PotentialRange(0, 0)
    bR = PotentialRange(None, None)
    aS = PotentialRange(3000, float('inf'))
    aA = PotentialRange(750, 2999)
    aB = PotentialRange(150, 749)
    aC = PotentialRange(1, 149)
    a0 = PotentialRange(0, 0)
    aR = PotentialRange(None, None)


@dataclass
class Client:
    client_id: str
    code: str
    name: str
    potential_electric: Potential
    potential_krep: Potential
    potential_sb: Potential
    spk_electric: int
    spk_krep: int
    spk_sb: int
    plan_id: Plan | None
