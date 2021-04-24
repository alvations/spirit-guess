
import string
from collections import Counter

from spirit_guess.languages import unicode_block

def count_chars_in_blocks(text: str) -> Counter:
    # Initialize counter.
    block_counts = Counter()
    for ch in text:  # Iterate through each character.
        if ch in string.punctuation or not ch.strip() or ch.isdigit():
            continue
        try:
            # For some reason, the original code shifts to right by 4 bits
            # See https://stackoverflow.com/a/8345671/610569
            block_counts.update(unicode_block(ord(ch) >> 4))
        except (TypeError, KeyError):
            block_counts[{'unknown'}] += 1
    # Normalize ths score.
    sum_scores = sum(block_counts.values())
    for lang, count in block_counts.items():
        block_counts[lang] = count / sum_scores
    # Return the full counter object.
    return block_counts
