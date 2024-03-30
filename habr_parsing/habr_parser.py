import asyncio
from datetime import datetime
from urllib.parse import urlparse, ParseResult

import aiohttp
import bs4
import requests
from bs4 import BeautifulSoup, ResultSet

from dto.habr_article import articles, HabrArticle
from habr_consts_parser import habr_article_selector, base_habr_articles_link, habr_body_selector, \
    habr_article_link_selector, habr_article_time_tag


async def fetch_raw_habr_pages_async(pages=10):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_page(session, page_number) for page_number in range(1, pages + 1)]
        return await asyncio.gather(*tasks)


async def fetch_page(session, page_number):
    url = f'https://habr.com/all/page{page_number}/'
    async with session.get(url) as response:
        return await response.text()


def fetch_raw_habr_pages(pages=10) -> tuple[str]:
    return asyncio.run(fetch_raw_habr_pages_async(pages))


def get_habr_id_from_href(url) -> str:
    res: ParseResult = urlparse(url)
    return list(filter(None, res.path.split("/")))[-1]


def article_get_text(link) -> bs4.Tag:
    page = requests.get(link)
    if page.status_code != 200:
        raise Exception("Article link is not valid")
    soup: bs4.BeautifulSoup = BeautifulSoup(page.text, "html.parser")
    return soup.select_one(selector=habr_body_selector)


def parse_article(article_tag) -> HabrArticle:
    habr_id = article_tag.get("id")
    article_full_link = base_habr_articles_link + habr_id
    name: str = article_tag.select_one(habr_article_link_selector).text
    body: bs4.Tag = article_get_text(article_full_link)
    text: str = body.text
    created_date: str = article_tag.select_one(selector=habr_article_time_tag).get("datetime")
    parsed_created_date: datetime = datetime.fromisoformat(created_date.replace('Z', '+00:00'))
    return HabrArticle(title=name, text=text, html_body=body, link=article_full_link, creation_date=parsed_created_date)


def parse_articles(pages=1) -> articles:
    res: articles = []
    habr_pages = fetch_raw_habr_pages(pages=pages)

    for page in habr_pages:
        name: str
        soup: bs4.BeautifulSoup = BeautifulSoup(page, "html.parser")
        articles_tags: ResultSet = soup.select(selector=habr_article_selector)

        for article_tag in articles_tags:
            article: HabrArticle = parse_article(article_tag)
            print(article.title)
            res.append(article)

    return res
