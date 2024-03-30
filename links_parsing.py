import asyncio
import logging
import networkx as nx
import matplotlib.pyplot as plt
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import aiohttp

from ranking import calculate_ranks


async def fetch_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


async def find_links(url, tag, graph, level=0, max_nodes=None):
    logging.info(f"Fetching {url} at level {level}")
    try:
        if max_nodes is not None and len(graph) >= max_nodes:
            return
        html = await fetch_url(url)
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all('a', href=True)
        for link in links:
            href = link.get('href')
            absolute_url = urljoin(url, href)
            graph.add_edge(url, absolute_url)
            if level > 0:
                await find_links(absolute_url, tag, graph, level - 1, max_nodes)
    except Exception as e:
        logging.error(f"Error fetching {url}: {e}")


async def build_graph(url, tag, level=1, max_nodes=None):
    graph = nx.DiGraph()
    await find_links(url, tag, graph, level, max_nodes)
    return graph


async def main():
    logging.basicConfig(level=logging.INFO)
    url = "https://example.com"
    tag = None
    max_nodes = 10
    graph = await build_graph(url, tag, level=2, max_nodes=max_nodes)

    nx.draw_networkx(graph)
    plt.show()

    result = calculate_ranks(pairs=graph.edges(), precision=5, damping_factor=1)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
