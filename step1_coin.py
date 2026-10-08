"""Step 1. The law of large numbers, the easy case: a fair coin, where no flip cares about the one before."""
import random
from save import save

random.seed(1913)
heads, marks, path = 0, {}, []
for n in range(1, 1_000_001):
    heads += random.random() < 0.5
    if n in (10, 100, 1_000, 10_000, 100_000, 1_000_000):
        marks[n] = heads / n
    if n <= 400:
        path.append(heads / n)
print('one player, share of heads')
for n, share in marks.items():
    print(f'{n:>10,} flips: {100 * share:7.3f}%')

# 1,000 players: how far apart are they after n flips each?
table = []
print('1,000 players, each flipping n times: lowest and highest share of heads')
for n in (10, 100, 1_000, 10_000):
    shares = sorted(sum(random.random() < 0.5 for _ in range(n)) / n for _ in range(1_000))
    table.append([n, shares[0], shares[-1], round(100 * (shares[-1] - shares[0]), 2)])
    print(f'{n:>7,} flips: {100 * shares[0]:5.1f}% to {100 * shares[-1]:5.1f}%   gap {100 * (shares[-1] - shares[0]):5.1f} points')
save(1, marks={str(k): v for k, v in marks.items()}, path=path, table=table)
