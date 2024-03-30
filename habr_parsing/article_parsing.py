from urllib.parse import urlparse, ParseResult

import bs4
import requests
from aiohttp import ClientSession
from bs4 import ResultSet

from habr_parsing.habr_consts_parser import habr_article_selector
from ranking import Pair
from dto import HabrArticle
from datetime import datetime


async def parse_article(url: str, session: ClientSession) -> HabrArticle:
    content: str = await (await session.get(url)).text()
    soup: bs4.BeautifulSoup = bs4.BeautifulSoup(content, "html.parser")
    article_tag: bs4.Tag = soup.select_one(selector=habr_article_selector)

    # TODO:
    # Function parses info about one single article by url

    return HabrArticle(
        title='title',
        text='text',
        link='link',
        creation_date=datetime.now()
    )
