# Проверка введенного количества элементов для блока
def is_valid_words_in_block(n: str) -> bool:
    if not n.isdigit():
        return False

    n = int(n)
    return 5 <= n <= 20


# Проверка введенного числа повторений на блок
def is_valid_repetitions_for_block(n: str) -> bool:
    if not n.isdigit():
        return False

    n = int(n)
    return 1 <= n <= 10
