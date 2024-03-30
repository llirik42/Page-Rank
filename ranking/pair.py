from dataclasses import dataclass


@dataclass
class Pair:
    """
    Represents directed pair of objects.
    """

    src: object
    dst: object
