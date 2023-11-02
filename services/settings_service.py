from icecream import ic


def is_valid_words_in_block(n: str) -> bool:
    if not n.isdigit():
        return False

    n = int(n)
    return 5 <= n <= 20


def is_valid_repetitions_for_block(n: str) -> bool:
    if not n.isdigit():
        return False

    n = int(n)
    return 1 <= n <= 10
