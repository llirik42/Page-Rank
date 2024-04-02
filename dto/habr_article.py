from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class HabrArticle:
    title: str
    text: str
    html: str
    creation_datetime: datetime
    link: str
    id: int

    def __str__(self) -> str:
        return str(self.id)

    def brief(self) -> str:
        max_length: int = 60
        length: int = len(str(self.title))

        if length >= max_length:
            return f'{self.title[:max_length]}... ({self.link})'
        else:
            return f'{self.title} {" " * (max_length - length + 2)} ({self.link})'

    def __eq__(self, other):
        if not isinstance(other, HabrArticle):
            return False

        return self.id == other.id
