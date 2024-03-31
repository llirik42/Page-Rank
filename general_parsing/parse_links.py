from urllib.parse import urljoin

import aiohttp
from aiohttp import ClientSession
from bs4 import BeautifulSoup


async def get_html_content(session: ClientSession, url: str) -> str:
    async with session.get(url) as response:
        if response.status != 200:
            raise ValueError(f"Failed to fetch URL {url}. Status code: {response.status}")
        return await response.text()


async def get_links(html_content: str, base_url: str) -> list[str]:
    soup = BeautifulSoup(html_content, 'html.parser')
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href:
            full_url = urljoin(base_url, href)
            links.append(full_url)
    return links


async def get_links_by_url(session: ClientSession, url: str) -> list[str]:
    html_content = await get_html_content(session, url)
    return await get_links(html_content, url)
