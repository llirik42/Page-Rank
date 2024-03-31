import asyncio

from aiohttp import ClientSession

from habr_parsing.article_parsing import parse_article


async def main():
    async with ClientSession() as session:
        res = await parse_article(url='https://habr.com/ru/articles/804135/', session=session)
        print(res)
# from ranking import calculate_ranks, RankedObject, Pair
#
# pairs: list[Pair] = [
#     Pair('a', 'b', 1),
#     Pair('c', 'b', 1),
#     Pair('b', 'd', 1),
#     Pair('a', 'x', 1),
#     Pair('x', 'b', 1),
#     Pair('w', 'g', 1),
#     Pair('d', 'x', 1),
#     Pair('w', 'c', 1),
# ]
#
# ranked_objects: list[RankedObject] = calculate_ranks(pairs, precision=5, damping_factor=1)
#
# for ro in ranked_objects:
#     print(ro)

if __name__ == '__main__':
    asyncio.run(main())
