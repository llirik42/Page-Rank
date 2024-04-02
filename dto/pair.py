from dataclasses import dataclass


@dataclass(frozen=True)
class Pair:
    """
    Represents directed pair of objects.
    """

    src: object
    dst: object
    weight: float = 1
