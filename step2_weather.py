"""Step 2. A linked case: tomorrow's weather leans on today's. Does the share of sunny days still settle?"""
import random
from chain import walk
from save import save

random.seed(1906)
ROWS = {'sun': [(0.9, 'sun'), (0.1, 'rain')], 'rain': [(0.5, 'sun'), (0.5, 'rain')]}
MARKS = (10, 100, 1_000, 10_000, 100_000, 1_000_000)
out, first = {}, {}
for start in ('sun', 'rain'):
    sunny, row, days = 0, {}, []
    for n, s in enumerate(walk(ROWS, start, 1_000_000), 1):
        sunny += s == 'sun'
        if n in MARKS:
            row[n] = sunny / n
        if n <= 60:
            days.append(1 if s == 'sun' else 0)
    out[start], first[start] = row, days
    print(f'start on a day of {start}: share of sunny days')
    for n, share in row.items():
        print(f'{n:>10,} days: {100 * share:7.3f}%')

# after a sunny day, and after a rainy day, in the long run from 'sun'
after = {'sun': [0, 0], 'rain': [0, 0]}
prev = 'sun'
for s in walk(ROWS, 'sun', 1_000_000):
    after[prev][0] += s == 'sun'
    after[prev][1] += 1
    prev = s
for k, (a, b) in after.items():
    print(f'the day after {k}: sunny {100 * a / b:.1f}% of {b:,} times')

# 1,000 worlds: linked weather against a coin with the same share of sunny days
table = []
print('1,000 worlds, n days each: lowest and highest share of sunny days (linked | a coin with 5 sunny sides of 6)')
for n in (100, 1_000, 10_000):
    linked = sorted(sum(s == 'sun' for s in walk(ROWS, 'sun', n)) / n for _ in range(1_000))
    coin = sorted(sum(random.random() < 5 / 6 for _ in range(n)) / n for _ in range(1_000))
    table.append([n, linked[0], linked[-1], coin[0], coin[-1]])
    print(f'{n:>7,} days: {100 * linked[0]:5.1f}% to {100 * linked[-1]:5.1f}%  |  {100 * coin[0]:5.1f}% to {100 * coin[-1]:5.1f}%')
save(2, share=out, first=first, after={k: a / b for k, (a, b) in after.items()}, table=table)
