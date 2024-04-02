from datetime import datetime

import aiohttp
import bs4

from dto import HabrArticle
from general_parsing import fetch_html_content
from .consts import (
    ARTICLE_SELECTOR,
    ARTICLE_MAIN_TITLE,
    ARTICLE_BODY,
    ARTICLE_TIMESTAMP,
)
from .habr_utils import construct_default_article_url, extract_article_id


async def parse_article(url: str, session: aiohttp.ClientSession) -> HabrArticle:
    try:
        content: str = await fetch_html_content(session=session, url=url)
    except ValueError:
        exit(1)

    soup: bs4.BeautifulSoup = bs4.BeautifulSoup(content, "html.parser")
    article_tag: bs4.Tag = soup.select_one(selector=ARTICLE_SELECTOR)

    title: str = article_tag.select_one(ARTICLE_MAIN_TITLE).text.strip()
    text: str = article_tag.select_one(ARTICLE_BODY).text.strip()
    html: str = article_tag.select_one(ARTICLE_BODY).prettify()
    created_datetime_str: str = article_tag.select_one(selector=ARTICLE_TIMESTAMP).get("datetime")
    create_datetime: datetime = datetime.fromisoformat(created_datetime_str.replace('Z', '+00:00'))
    article_id: int = extract_article_id(url)

    return HabrArticle(
        title=title,
        text=text,
        html=html,
        link=construct_default_article_url(article_id),
        creation_datetime=create_datetime,
        id=article_id
    )
