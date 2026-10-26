import os
import timeit


def boyer_moore(text, pattern):
    """Boyer-Moore з правилом поганого символу. Повертає індекс або -1."""
    n, m = len(text), len(pattern)
    if m == 0:
        return 0
    last = {ch: i for i, ch in enumerate(pattern)}
    shift = 0
    while shift <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[shift + j]:
            j -= 1
        if j < 0:
            return shift
        shift += max(1, j - last.get(text[shift + j], -1))
    return -1


def compute_prefix(pattern):
    prefix = [0] * len(pattern)
    k = 0
    for i in range(1, len(pattern)):
        while k > 0 and pattern[k] != pattern[i]:
            k = prefix[k - 1]
        if pattern[k] == pattern[i]:
            k += 1
        prefix[i] = k
    return prefix


def kmp(text, pattern):
    """Knuth-Morris-Pratt. Повертає індекс або -1."""
    m = len(pattern)
    if m == 0:
        return 0
    prefix = compute_prefix(pattern)
    k = 0
    for i, ch in enumerate(text):
        while k > 0 and pattern[k] != ch:
            k = prefix[k - 1]
        if pattern[k] == ch:
            k += 1
        if k == m:
            return i - m + 1
    return -1


def rabin_karp(text, pattern, base=256, mod=1_000_000_007):
    """Rabin-Karp з перевіркою збігу після збігу хешів. Повертає індекс або -1."""
    n, m = len(text), len(pattern)
    if m == 0:
        return 0
    if m > n:
        return -1
    high = pow(base, m - 1, mod)
    p_hash = t_hash = 0
    for i in range(m):
        p_hash = (p_hash * base + ord(pattern[i])) % mod
        t_hash = (t_hash * base + ord(text[i])) % mod
    for i in range(n - m + 1):
        if p_hash == t_hash and text[i:i + m] == pattern:
            return i
        if i < n - m:
            t_hash = ((t_hash - ord(text[i]) * high) * base + ord(text[i + m])) % mod
    return -1


def read_text(name):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), name)
    with open(path, encoding="cp1251") as f:
        return f.read()


ALGORITHMS = {
    "Боєр-Мур": boyer_moore,
    "КМП": kmp,
    "Рабін-Карп": rabin_karp,
}

ARTICLES = {
    "article_1.txt": {
        "існуючий": "інтерполяції. Найефективніше застосовувати",
        "вигаданий": "квантовий алгоритм сортування бананів",
    },
    "article_2.txt": {
        "існуючий": "нерозв’язні через значну розмірність",
        "вигаданий": "квантовий алгоритм сортування бананів",
    },
}

RUNS = 20


def main():
    totals = {name: 0.0 for name in ALGORITHMS}
    for article, patterns in ARTICLES.items():
        text = read_text(article)
        print(f"\n{article} ({len(text)} символів)")
        article_totals = {name: 0.0 for name in ALGORITHMS}
        for kind, pattern in patterns.items():
            expected = text.find(pattern)
            print(f"  {kind} підрядок: {pattern!r}, позиція {expected}")
            for name, func in ALGORITHMS.items():
                assert func(text, pattern) == expected, f"{name} дав хибний результат"
                seconds = timeit.timeit(lambda: func(text, pattern), number=RUNS) / RUNS
                article_totals[name] += seconds
                totals[name] += seconds
                print(f"    {name:<12} {seconds:.6f} с")
        fastest = min(article_totals, key=article_totals.get)
        print(f"  Найшвидший для {article}: {fastest}")
    print("\nСума по обох текстах:")
    for name, seconds in totals.items():
        print(f"  {name:<12} {seconds:.6f} с")
    print(f"Найшвидший в цілому: {min(totals, key=totals.get)}")


if __name__ == "__main__":
    main()
