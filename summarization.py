import asyncio

from aiohttp import ClientSession

from dto import HabrArticle
from habr_parsing import parse_article
from summarization import summarize


async def main():
    async with ClientSession() as session:
        article_link: str = 'https://habr.com/ru/articles/789252/'
        article: HabrArticle = await parse_article(session=session, url=article_link)

        for ranked_sentence in summarize(article.text, partition=5):
            print(list(ranked_sentence.obj.words), ranked_sentence.rank)
            print()

if __name__ == '__main__':
    asyncio.run(main())
