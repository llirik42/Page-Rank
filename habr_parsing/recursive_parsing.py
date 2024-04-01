import re
from typing import Optional

from aiohttp import ClientSession

from dto import Pair, HabrArticle
from general_parsing import extract_links_from_html
from .article_parsing import parse_article


def is_habr_articles_link(url):
    pattern = r"^https?:\/\/habr\.com\/ru\/.*?(?:post|articles|blog|news)\/\d+\/?$"
    return bool(re.match(pattern, url))


async def parse_recursive_articles(session: ClientSession,
                                   url: str,
                                   res: Optional[list[Pair]] = None,
                                   visited_links: Optional[set] = None,
                                   max_depth: int = 1,
                                   current_depth: int = 0,
                                   only_habr_links=True) -> list[Pair]:
    if res is None:
        res: list[Pair] = []

    if visited_links is None:
        visited_links = set()
    if current_depth >= max_depth or url in visited_links:
        return res

    visited_links.add(url)
    parent_article: HabrArticle = await parse_article(url=url, session=session)
    links: list[str] = await extract_links_from_html(parent_article.html)

    for link in links:
        if not is_habr_articles_link(link) and only_habr_links:
            continue

        current_article: HabrArticle = await parse_article(url=link, session=session)

        pair = Pair(src=parent_article, dst=current_article)
        res.append(pair)
        await parse_recursive_articles(
            session=session,
            url=link,
            res=res,
            visited_links=visited_links,
            max_depth=max_depth,
            current_depth=current_depth + 1,
            only_habr_links=only_habr_links)

    return res
