from urllib.parse import urljoin

import aiohttp
from bs4 import BeautifulSoup


async def get_html_content(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html_content = await response.text()
    return html_content


async def get_links(html_content: str, base_url: str) -> list[str]:
    soup = BeautifulSoup(html_content, 'html.parser')
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href:
            full_url = urljoin(base_url, href)
            links.append(full_url)
    return links


async def get_links_by_url(url: str) -> list[str]:
    html_content = await get_html_content(url)
    return await get_links(html_content, url)
