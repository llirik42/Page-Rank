def extract_article_id(article_url: str) -> int:
    return int(article_url.split('/')[-2])


def construct_default_article_url(article_id: int) -> str:
    return f'https://habr.com/ru/articles/{article_id}/'
