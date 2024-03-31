import asyncio
import aiohttp
from dto.pair import Pair
from general_parsing.parse_links import get_links, get_links_by_url


async def fetch_page(session, page_number):
    url = f'https://habr.com/all/page{page_number}/'
    async with session.get(url) as response:
        return url, await response.text()


async def fetch_raw_habr_pages_async(pages=10):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_page(session, page_number) for page_number in range(1, pages + 1)]
        return await asyncio.gather(*tasks)


async def get_links_recursive(url, res=None, visited=None, max_links_cnt=10):
    if res is None:
        res = []
    if visited is None:
        visited = set()
    if len(res) >= max_links_cnt or url in visited:
        return res

    visited.add(url)

    links = await get_links_by_url(url)
    for link in links:
        res.append(Pair(src=url, dst=link))
        await get_links_recursive(link, res, visited, max_links_cnt)

    return res


async def parse_articles(pages=1, max_links=10) -> list[Pair]:
    res = []
    habr_pages = await fetch_raw_habr_pages_async(pages=pages)
    for page in habr_pages:
        url, content = page
        links = await get_links(content, url)
        for link in links:
            res.append(Pair(src=url, dst=link))
            await get_links_recursive(link, res, max_links_cnt=max_links)

    print(res)
    return res


async def main():
    num_pages = 5
    max_links = 10
    await parse_articles(pages=num_pages, max_links=max_links)


if __name__ == '__main__':
    asyncio.run(main())
