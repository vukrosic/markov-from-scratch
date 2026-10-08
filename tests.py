"""Checks. run_all.sh runs them last, on the numbers the seven steps saved in runs/."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
r = {i: json.load(open(os.path.join(HERE, 'runs', 'step%d.json' % i))) for i in range(1, 8)}

# 1. the coin settles at a half, and 1,000 players agree more the longer they flip
assert abs(r[1]['marks']['1000000'] - 0.5) < 0.002
gaps = [hi - lo for _, lo, hi, _gap in r[1]['table']]
assert all(a > b for a, b in zip(gaps, gaps[1:]))

# 2. linked weather settles at 5/6 from both starts; the days are linked; linked worlds agree less than coin worlds
for start in ('sun', 'rain'):
    assert abs(r[2]['share'][start]['1000000'] - 5 / 6) < 0.003
assert abs(r[2]['after']['sun'] - 0.9) < 0.005 and abs(r[2]['after']['rain'] - 0.5) < 0.005
assert all(row[2] - row[1] > row[4] - row[3] for row in r[2]['table'])

# 3. the crowd reaches the balance; the gap shrinks by 0.4 a day; the balance rule predicts the quiz chain
assert abs(r[3]['tracks']['rain'][30] - 5 / 6) < 1e-9 and abs(r[3]['tracks']['sun'][30] - 5 / 6) < 1e-9
assert abs(r[3]['ratio'] - 0.4) < 1e-9 and abs(r[3]['quiz'][0] - r[3]['quiz'][1]) < 0.003

# 4. letters lean on the letter before, in Markov's count and in ours; blocks agree more than a coin would
assert r[4]['his']['vv'] < r[4]['his']['share'] / 2 and abs(r[4]['his']['fixed'] - r[4]['his']['share']) < 0.001
assert r[4]['a_vv'] < r[4]['share'] / 2 < r[4]['a_cv'] and r[4]['spread'] < r[4]['coin']
assert abs(r[4]['fixed'] - r[4]['share']) < 0.001

# 5. islands depend on the start; a bridge repairs them; ping-pong settles in time only; sticky worlds agree slowly
assert r[5]['islands']['C'] == 0 and r[5]['islands']['A'] > 0.45
assert all(abs(v - 0.25) < 0.02 for v in r[5]['bridge'].values())
assert r[5]['crowd'][:4] == [1.0, 0.0, 1.0, 0.0] and abs(r[5]['pp'] - 0.5) < 0.001
assert r[5]['sticky'][0][2] - r[5]['sticky'][0][1] > 0.9 > r[5]['sticky'][2][2] - r[5]['sticky'][2][1]

# 6. links only: the start decides; with the jump: one answer, and the crowd agrees with the surfer
assert r[6]['only']['news']['club'] == 0 and r[6]['only']['club']['news'] == 0
assert all(abs(r[6]['ranks']['news'][p] - r[6]['ranks']['club'][p]) < 0.005 for p in r[6]['crowd'])
assert all(abs(r[6]['ranks']['news'][p] - r[6]['crowd'][p]) < 0.005 for p in r[6]['crowd'])
assert max(r[6]['crowd'], key=r[6]['crowd'].get) == 'wiki' and abs(sum(r[6]['crowd'].values()) - 1) < 1e-9

# 7. longer memory: more real words, more states; the longest memory starts to copy
real = [row[2] for row in r[7]['rows']]
states = [row[1] for row in r[7]['rows']]
assert all(a < b for a, b in zip(real, real[1:])) and all(a < b for a, b in zip(states, states[1:]))
assert r[7]['rows'][-1][3] > 0.05 and r[7]['rows'][3][3] == 0
print('all checks passed')
