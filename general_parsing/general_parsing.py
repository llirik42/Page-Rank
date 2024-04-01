from typing import Optional

import bs4
from aiohttp import ClientSession


async def fetch_html_content(session: ClientSession, url: str) -> str:
    async with session.get(url) as response:
        if not response.ok:
            raise ValueError(f"Failed to fetch URL {url}. Status code: {response.status}")
        return await response.text()


async def extract_links_by_url(session: ClientSession, url: str) -> list[str]:
    html_content: str = await fetch_html_content(session, url)
    return await extract_links_from_html(html_content)


async def extract_links_from_html(html_content: str) -> list[str]:
    soup: bs4.BeautifulSoup = bs4.BeautifulSoup(markup=html_content, features='html.parser')
    links: set[str] = set()
    for link in soup.find_all('a'):
        href: Optional[str] = link.get('href')
        if href:
            links.add(href)
    return list(links)
