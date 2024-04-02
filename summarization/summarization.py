from dataclasses import dataclass
from math import log

from dto import HabrArticle, Pair
from ranking import calculate_ranks, RankedObject


@dataclass(frozen=True)
class Sentence:
    words: frozenset[str]


def summarize(article: HabrArticle) -> list[RankedObject]:
    sentences: list[Sentence] = [Sentence(frozenset(s.strip().split(' '))) for s in article.text.split('.')]

    sentences_count: int = len(sentences)
    pairs: list[Pair] = []

    for i in range(sentences_count):
        for j in range(sentences_count):
            if i == j:
                continue
            si: Sentence = sentences[i]
            sj: Sentence = sentences[j]
            similarity: float = _calculate_sentences_similarity(si, sj)

            if similarity > 0:
                pairs.append(Pair(si, sj, similarity))
                pairs.append(Pair(sj, si, similarity))

    return calculate_ranks(pairs)


def _calculate_sentences_similarity(s1: Sentence, s2: Sentence) -> float:
    s1_words_set: set[str] = set(s1.words)
    s2_words_set: set[str] = set(s2.words)

    l1: int = len(s1_words_set)
    l2: int = len(s2_words_set)

    # One of sentences is empty
    if l1 == 0 or l2 == 0:
        return 0.0

    # Exclude a possible division by zero
    if l1 == l2 and l1 == 1:
        return float(1 - len(s1_words_set.difference(s2_words_set)))

    common_words_set: set[str] = set.intersection(s1_words_set, s2_words_set)

    return len(common_words_set) / (log(l1) + log(l2))
