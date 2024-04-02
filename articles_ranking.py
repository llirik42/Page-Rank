import asyncio

from aiohttp import ClientSession

from dto import Pair
from habr_parsing import parse_recursive_articles
from ranking import RankedObject, calculate_ranks
from drawing import draw_graph


async def main():
    async with ClientSession() as session:
        article_link: str = 'https://habr.com/ru/articles/789252/'

        pairs: list[Pair] = list(await parse_recursive_articles(
            session=session,
            url=article_link,
            max_depth=3,
            only_habr_links=True
        ))

        ranked_objects: list[RankedObject] = calculate_ranks(pairs, damping_factor=1)

        for r in ranked_objects:
            print(r.obj.brief(), r.rank)

        draw_graph(pairs)

if __name__ == '__main__':
    asyncio.run(main())
