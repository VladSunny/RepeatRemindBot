import math
import random
from icecream import ic


def get_blocks_num(module_len: int, words_in_block: int) -> int:
    return math.ceil(module_len / words_in_block)


def get_blocks(content: dict[str, str], words_in_block: int) -> dict[str, dict[str, str]]:
    items = list(content.items())
    random.shuffle(items)

    blocks: dict[str, dict[str, str]] = {}

    for i in range(get_blocks_num(len(content), words_in_block)):
        blocks[f"block_{i + 1}"] = {}

    for i in range(len(items)):
        blocks[f"block_{math.ceil((i + 1) / words_in_block)}"][items[i][0]] = items[i][1]

    return blocks


def get_blocks_str(content: dict[str, str], words_in_block: int, separator: str) -> str:
    blocks = get_blocks(content, words_in_block)
    text: str = ""

    for i in range(len(blocks)):
        block = list(blocks.items())[i]
        text += f"* block {i + 1}:\n"
        for j in range(len(block[1])):
            pair = list(block[1].items())[j]
            text += f"\t\t {j + 1}. {pair[0]} {separator} {pair[1]}\n"
        text += "\n"

    return text
