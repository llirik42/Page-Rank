import asyncio

from aiohttp import ClientSession

from drawing import draw_graph
from dto import Pair
from habr_parsing import parse_recursive_articles
from ranking import RankedObject, calculate_ranks

START_HABR_ARTICLE = 'https://habr.com/ru/articles/789252/'


async def main():
    async with ClientSession() as session:
        pairs: list[Pair] = list(await parse_recursive_articles(
            session=session,
            url=START_HABR_ARTICLE,
            max_depth=5,
            only_habr_links=True
        ))

        print(len(pairs))

        ranked_objects: list[RankedObject] = calculate_ranks(pairs)

        for r in ranked_objects:
            print(r.obj.brief(), r.rank)

        draw_graph(pairs)


if __name__ == '__main__':
    asyncio.run(main())
