from dataclasses import dataclass


@dataclass
class RankedObject:
    """
    Represents object with a given rank.
    """

    obj: object
    rank: float
