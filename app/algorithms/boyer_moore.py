def _build_bad_char_table(pattern: str) -> dict[str, int]:
    m = len(pattern)
    table: dict[str, int] = {}
    for i in range(m - 1):
        table[pattern[i]] = i
    return table

def boyer_moore_contains(text: str, pattern: str, *, case_insensitive: bool = True) -> bool:
    if not pattern: return True
    if not text: return False
    if case_insensitive:
        text = text.casefold()
        pattern = pattern.casefold()
    n, m = len(text), len(pattern)
    if m > n: return False
    bad = _build_bad_char_table(pattern)
    i = 0
    while i <= n - m:
        j = m - 1
        while j >= 0 and text[i + j] == pattern[j]: j -= 1
        if j < 0: return True
        shift = j - bad.get(text[i + j], -1)
        if shift < 1: shift = 1
        i += shift
    return False