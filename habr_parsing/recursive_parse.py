import asyncio
import os
from urllib.parse import urljoin

import aiohttp
from aiohttp import ClientSession

from dto import HabrArticle
from dto.pair import Pair
from general_parsing.parse_links import get_links, get_links_by_url, get_html_content
from habr_parsing.article_parsing import extract_article_links_in_list_page, parse_article


async def fetch_page(session, page_number):
    url = f'https://habr.com/all/page{page_number}/'
    res = await get_html_content(session, url)
    return url, res


async def fetch_raw_habr_pages_async(session: ClientSession, pages=10):
    tasks = [fetch_page(session, page_number) for page_number in range(1, pages + 1)]
    return await asyncio.gather(*tasks)


async def get_links_recursive(session: ClientSession, url, res=None, visited=None, max_links_cnt=10):
    if res is None:
        res = []
    if visited is None:
        visited = set()
    if len(res) >= max_links_cnt or url in visited:
        return res

    visited.add(url)

    links = await get_links_by_url(session, url)
    for link in links:
        res.append(Pair(src=url, dst=link))
        await get_links_recursive(session, link, res, visited, max_links_cnt)

    return res


async def parse_articles(session: ClientSession, pages: int = 1) -> list[str]:
    res = []
    habr_pages = await fetch_raw_habr_pages_async(session=session, pages=pages)

    for url, content in habr_pages:
        links = await extract_article_links_in_list_page(content)
        link_joined = map(lambda link: urljoin(url, link), links)
        res.extend(link_joined)
    return res


async def main():
    async with aiohttp.ClientSession() as session:
        articles_links = await parse_articles(session, pages=10)
        articles_parsed: tuple[HabrArticle | None] = await asyncio.gather(
            *(parse_article(link, session) for link in articles_links)
        )
        print(articles_parsed.count(None))
        articles_parsed: list[HabrArticle] = list(filter(None, articles_parsed))
        print(articles_parsed[0].creation_date)
if __name__ == '__main__':
    asyncio.run(main())
