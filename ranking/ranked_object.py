from dataclasses import dataclass


@dataclass
class RankedObject:
    obj: object
    rank: float
