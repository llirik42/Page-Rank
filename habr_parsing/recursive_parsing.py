import asyncio
import re
from typing import Optional

from aiohttp import ClientSession

from dto import Pair, HabrArticle
from general_parsing import extract_links_from_html
from .article_parsing import parse_article


def is_habr_articles_link(url):
    pattern = r"^https?:\/\/habr\.com\/ru\/.*?(?:post|articles|blog|news)\/\d+\/?$"
    return bool(re.match(pattern, url))


async def handle_link(parent_article: HabrArticle,
                      session: ClientSession,
                      link: str,
                      only_habr_links: bool,
                      res: Optional[list[Pair]],
                      visited_habr_article_ids: Optional[set[int]],
                      max_depth: int,
                      current_depth: int
                      ):
    if not is_habr_articles_link(link) and only_habr_links:
        return

    current_article: HabrArticle = await parse_article(url=link, session=session)

    if parent_article != current_article:
        pair = Pair(src=parent_article, dst=current_article)
        res.append(pair)

    await parse_recursive_articles(
        session=session,
        url=link,
        res=res,
        visited_articles_ids=visited_habr_article_ids,
        max_depth=max_depth,
        current_depth=current_depth + 1,
        only_habr_links=only_habr_links)


async def parse_recursive_articles(session: ClientSession,
                                   url: str,
                                   res: Optional[list[Pair]] = None,
                                   visited_articles_ids: Optional[set[int]] = None,
                                   max_depth: int = 1,
                                   current_depth: int = 0,
                                   only_habr_links: bool = True) -> list[Pair]:
    if res is None:
        res: list[Pair] = []

    if visited_articles_ids is None:
        visited_articles_ids = set()

    parent_article: HabrArticle = await parse_article(url=url, session=session)

    if current_depth >= max_depth or parent_article.id in visited_articles_ids:
        return res

    visited_articles_ids.add(parent_article.id)
    links: list[str] = await extract_links_from_html(parent_article.html)

    tasks = []
    for link in links:
        tasks.append(asyncio.create_task(handle_link(
            parent_article=parent_article,
            session=session,
            link=link,
            visited_habr_article_ids=visited_articles_ids,
            max_depth=max_depth,
            current_depth=current_depth,
            only_habr_links=only_habr_links,
            res=res
        )))

    await asyncio.gather(*tasks)

    return res
