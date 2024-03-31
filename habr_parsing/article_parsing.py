import asyncio
from datetime import datetime

import aiohttp
import bs4
from aiohttp import ClientSession

from dto import HabrArticle
from habr_parsing.consts import habr_article_selector, habr_article_main_title, habr_article_body, \
    habr_article_timestamp, link_tag


async def parse_article(url: str, session: ClientSession) -> HabrArticle:
    content: str = await (await session.get(url)).text()
    soup: bs4.BeautifulSoup = bs4.BeautifulSoup(content, "html.parser")
    article_tag: bs4.Tag = soup.select_one(selector=habr_article_selector)

    title = article_tag.select_one(habr_article_main_title).text.strip()
    text = article_tag.select_one(habr_article_body).text.strip()
    html = article_tag.select_one(habr_article_body).prettify()
    link = url
    created_date: str = article_tag.select_one(selector=habr_article_timestamp).get("datetime")
    parsed_created_date: datetime = datetime.fromisoformat(created_date.replace('Z', '+00:00'))

    return HabrArticle(
        title=title,
        text=text,
        html=html,
        link=link,
        creation_date=parsed_created_date
    )


async def extract_article_links(article: HabrArticle) -> list[str]:
    soup: bs4.BeautifulSoup = bs4.BeautifulSoup(article.html, "html.parser")
    links = [link.get('href') for link in soup.select(selector=link_tag)]
    return list(map(str, links))


async def main():
    async with aiohttp.ClientSession() as session:
        # Call the parse_article function with the URL and session
        habr_article = await parse_article("https://habr.com/ru/articles/454/", session)

        # Print the parsed article information
        print("Title:", habr_article.title)
        print("Text:", habr_article.text)
        print("Html:", habr_article.html)
        print("Link:", habr_article.link)
        print("Creation Date:", habr_article.creation_date)
        print(await extract_article_links(habr_article))


# Run the asyncio event loop


if __name__ == "__main__":
    asyncio.run(main())
