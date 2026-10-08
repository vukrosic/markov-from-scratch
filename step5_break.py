"""Step 5. Where it breaks. Three chains: islands, a ping-pong, and a sticky one."""
import random
from chain import walk, cloud_step
from save import save

random.seed(5)
N = 100_000
# islands: A and B send to each other, C and D send to each other, and nothing crosses.  We watch the time spent on A.
ISL = {'A': [(0.5, 'A'), (0.5, 'B')], 'B': [(0.5, 'A'), (0.5, 'B')], 'C': [(0.5, 'C'), (0.5, 'D')], 'D': [(0.5, 'C'), (0.5, 'D')]}
islands = {s: sum(x == 'A' for x in walk(ISL, s, N)) / N for s in 'ABCD'}
print('islands, share of time on A after', f'{N:,}', 'steps:', {k: f'{100 * v:.1f}%' for k, v in islands.items()})

# one thin bridge of 1 in 100 between the islands, each way
BR = {'A': [(0.5, 'A'), (0.49, 'B'), (0.01, 'C')], 'B': [(0.5, 'A'), (0.5, 'B')], 'C': [(0.5, 'C'), (0.49, 'D'), (0.01, 'A')], 'D': [(0.5, 'C'), (0.5, 'D')]}
bridge = {s: sum(x == 'A' for x in walk(BR, s, 1_000_000)) / 1_000_000 for s in 'ABCD'}
print('with a bridge, after 1,000,000 steps:', {k: f'{100 * v:.1f}%' for k, v in bridge.items()})

# ping-pong: always switch.  The crowd never settles, but the share of time does.
PP = {'sun': [(1.0, 'rain')], 'rain': [(1.0, 'sun')]}
cloud, crowd = {'sun': 1.0, 'rain': 0.0}, []
for _ in range(8):
    crowd.append(cloud['sun'])
    cloud = cloud_step(PP, cloud)
pp_share = sum(s == 'sun' for s in walk(PP, 'sun', 1_001)) / 1_001
print('ping-pong: share of the crowd on sun, day by day:', crowd, f' share of time after 1,001 days: {100 * pp_share:.2f}%')

# sticky: stay where you are 999 times in 1,000.  The balance is 50%, but how long until 1,000 worlds agree?
ST = {'sun': [(0.999, 'sun'), (0.001, 'rain')], 'rain': [(0.001, 'sun'), (0.999, 'rain')]}
sticky = []
print('sticky chain, 200 worlds: lowest and highest share of sunny days')
for n in (1_000, 10_000, 100_000):
    shares = sorted(sum(s == 'sun' for s in walk(ST, 'sun', n)) / n for _ in range(200))
    sticky.append([n, shares[0], shares[-1]])
    print(f'{n:>8,} days: {100 * shares[0]:5.1f}% to {100 * shares[-1]:5.1f}%')
save(5, islands=islands, bridge=bridge, crowd=crowd, pp=pp_share, sticky=sticky)
