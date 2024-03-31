import asyncio
from datetime import datetime

import aiohttp
import bs4
from aiohttp import ClientSession

from dto import HabrArticle
from habr_parsing.consts import habr_article_selector, habr_article_main_title, habr_article_body, \
    habr_article_timestamp


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
    # TODO
    # Function accepts article and returns all links on page with it (links to habr only)
    return ['URL-1', 'URL-2', 'URL-3', 'URL-4']


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


# Run the asyncio event loop


if __name__ == "__main__":
    asyncio.run(main())
