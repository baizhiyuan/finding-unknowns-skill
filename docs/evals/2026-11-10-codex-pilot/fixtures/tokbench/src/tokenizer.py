from functools import lru_cache

@lru_cache(maxsize=4096)
def _split_word(word: str) -> tuple[str, ...]:
    # byte-pair style split; expensive for long words
    return tuple(word[i:i + 3] for i in range(0, len(word), 3))

def tokenize(text: str) -> list[str]:
    out: list[str] = []
    for w in text.split():
        out.extend(_split_word(w))
    return out
