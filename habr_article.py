from dataclasses import dataclass
from datetime import datetime

import bs4


@dataclass(frozen=True)
class HabrArticle:
    title: str
    text: str
    html_body: bs4.Tag
    link: str
    created_date: datetime


articles = list[HabrArticle]
