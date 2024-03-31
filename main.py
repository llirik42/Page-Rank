import asyncio
from typing import Optional

from aiohttp import ClientSession

from dto import HabrArticle
from dto.habr_article import articles
from dto.pair import Pair
from habr_parsing.article_parsing import parse_article
from habr_parsing.recursive_parse import parse_articles, get_links_recursive
from ranking import RankedObject, calculate_ranks


async def main():
    async with ClientSession() as session:
        articles_links = await parse_articles(session, pages=1)

        tasks = []

        for link in articles_links:
            tasks.append(asyncio.create_task(parse_article(link, session)))
        articles_parsed: tuple[Optional[HabrArticle]] = await asyncio.gather(*tasks)
        articles_filtered: articles = list(filter(None, articles_parsed))
        for article in articles_filtered:
            task = asyncio.create_task(get_links_recursive(session, article.link, max_links_cnt=10))
            tasks.append(task)

        results: tuple[list[Pair]] = await asyncio.gather(*tasks)
        pairs: list[Pair] = [*results]
        ranked_objects: list[RankedObject] = calculate_ranks(pairs, precision=5, damping_factor=1)
        print(ranked_objects)


if __name__ == '__main__':
    asyncio.run(main())
