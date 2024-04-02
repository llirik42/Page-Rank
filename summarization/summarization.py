from math import log
from dataclasses import dataclass

from dto import Pair
from ranking import calculate_ranks, RankedObject


@dataclass(frozen=True)
class WordsGroup:
    words: frozenset[str]


def summarize(text: str, partition: int) -> list[RankedObject]:
    all_words: list[str] = []
    for i in text.split('.'):
        all_words.extend(i.split(' '))
    all_words = [w for w in all_words if _accept_word(w)]

    words_groups: list[WordsGroup] = []
    for i in range(len(all_words) // partition + 1):
        words_groups.append(WordsGroup(frozenset(all_words[i*partition:(i+1)*partition])))

    words_groups_count: int = len(words_groups)

    pairs: list[Pair] = []
    for i in range(words_groups_count):
        for j in range(words_groups_count):
            if i == j:
                continue
            g1: WordsGroup = words_groups[i]
            g2: WordsGroup = words_groups[j]
            similarity: float = _calculate_sentences_similarity(g1.words, g2.words)

            if similarity > 0:
                pairs.append(Pair(g1, g2, similarity))
                pairs.append(Pair(g1, g2, similarity))

    return calculate_ranks(pairs)


def _accept_word(word: str) -> bool:
    forbidden: list[str] = [
        'на',
        'и',
        'ещё',
        'в',
        'за',
        'для',
        'её',
        'а',
        'нужно',
        'что',
        'не',
        'с',
        'то',
        'от',
    ]

    return word.isalpha() and word.lower() not in forbidden


def _calculate_sentences_similarity(s1: frozenset[str], s2: frozenset[str]) -> float:
    s1_words_set: set[str] = set(s1)
    s2_words_set: set[str] = set(s2)

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
