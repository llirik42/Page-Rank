from dataclasses import dataclass


@dataclass(frozen=True)
class RankedObject:
    """
    Represents object with a given rank.
    """

    obj: object
    rank: float
