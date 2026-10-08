"""Step 7. A chain that writes. The state is the last k letters; the row of chances is counted from a real text."""
import random
from collections import Counter, defaultdict
from save import save

random.seed(1948)
text = ' '.join(open('shakespeare.txt', encoding='utf-8').read().lower().split())
text = ''.join(c for c in text if c == ' ' or 'a' <= c <= 'z')
words = set(text.split())
print(f'the text: {len(text):,} letters and spaces, {len(words):,} different words')


def learn(k):
    table = defaultdict(Counter)
    for i in range(len(text) - k):
        table[text[i:i + k]][text[i + k]] += 1
    return table


def write(table, k, n):
    out = text[:k]
    for _ in range(n):
        row = table[out[len(out) - k:]] if k else table['']
        if not row:                                   # a state the text never continued: start again
            row = table[text[:k]]
        out += random.choices(list(row), weights=row.values())[0]
    return out[k:]


rows = []
print('memory  states seen  real words  copied   sample')
for k in (0, 1, 2, 3, 4, 6, 10):
    table = learn(k)
    made = write(table, k, 20_000)
    w = made.split()
    real = sum(x in words for x in w) / len(w)
    # copied: how many pieces of 30 letters appear word for word in the text?
    pieces = [made[i:i + 30] for i in range(0, 19_000, 100)]
    copied = sum(p in text for p in pieces) / len(pieces)
    rows.append([k, len(table), real, copied, made[:70]])
    print(f'{k:>4}   {len(table):>10,}   {100 * real:6.1f}%   {100 * copied:5.1f}%   {made[:70]}')
save(7, size=len(text), vocab=len(words), rows=rows)
