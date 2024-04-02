import asyncio

from summarization import summarize


async def main():
    file = open('texts/T3L.txt', 'r')
    text: str = file.read()
    file.close()

    for ranked_sentence in summarize(text, partition=10)[:1]:
        print(list(ranked_sentence.obj.words))
        print()


if __name__ == '__main__':
    asyncio.run(main())
