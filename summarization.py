import asyncio

from summarization import summarize


WORDS_IN_GROUP_COUNT: int = 10
TEXT_PATH: str = 'texts/T3L.txt'


async def main():
    file = open(TEXT_PATH, 'r')
    text: str = file.read()
    file.close()

    for ranked in summarize(text, partition=WORDS_IN_GROUP_COUNT):
        print(list(ranked.obj.words), ranked.rank)
        print()


if __name__ == '__main__':
    asyncio.run(main())
