from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class HabrArticle:
    title: str
    text: str
    html: str
    link: str
    creation_datetime: datetime

    def __str__(self) -> str:
        return '/'.join(self.link.split('/')[-3:-1])

    def brief(self) -> str:
        max_length: int = 60
        length: int = len(str(self.title))

        if length >= max_length:
            return f'{self.title[:max_length]}... ({self.link})'
        else:
            return f'{self.title} {" " * (max_length - length + 2)} ({self.link})'

    def __eq__(self, other) -> bool:
        if not isinstance(other, HabrArticle):
            return False

        return other.link == self.title
