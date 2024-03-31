import asyncio
from typing import Optional

from aiohttp import ClientSession

from helpers import draw_graph
from dto import HabrArticle
from dto.habr_article import articles
from dto.pair import Pair
from habr_parsing.article_parsing import parse_article
from habr_parsing.recursive_parse import parse_articles, get_links_recursive
from ranking import RankedObject, calculate_ranks


async def main():
    async with ClientSession() as session:
        articles_links = ['https://habr.com/ru/articles/789252/']

        tasks = []

        for link in articles_links:
            tasks.append(asyncio.create_task(parse_article(link, session)))
        articles_parsed: tuple[Optional[HabrArticle]] = await asyncio.gather(*tasks)
        articles_filtered: articles = list(filter(None, articles_parsed))
        all_pairs: list[Pair] = []
        for article_filtered in articles_filtered:
            pairs = (await get_links_recursive(session, article_filtered.link, max_links_cnt=2, only_habr_links=True))
            all_pairs.extend(pairs)

        ranked_objects: list[RankedObject] = calculate_ranks(all_pairs, precision=5, damping_factor=1)
        print(ranked_objects)
        draw_graph(all_pairs)


if __name__ == '__main__':
    asyncio.run(main())
