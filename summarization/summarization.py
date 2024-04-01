from dto import HabrArticle


def summarize(article: HabrArticle) -> list[str]:
    return [t.strip() for t in article.text.split('.')]
