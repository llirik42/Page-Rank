from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class HabrArticle:
    title: str
    text: str
    html: str
    link: str
    creation_date: datetime
