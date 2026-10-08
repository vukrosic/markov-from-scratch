"""Step 3. Why it settles. Follow a whole crowd of worlds at once, day by day, with no dice at all."""
import random
from chain import walk, cloud_step
from save import save

random.seed(3)
ROWS = {'sun': [(0.9, 'sun'), (0.1, 'rain')], 'rain': [(0.5, 'sun'), (0.5, 'rain')]}
tracks = {}
for start in ('rain', 'sun'):
    cloud = {'sun': 1.0 if start == 'sun' else 0.0, 'rain': 0.0 if start == 'sun' else 1.0}
    track = [cloud['sun']]
    for _ in range(30):
        cloud = cloud_step(ROWS, cloud)
        track.append(cloud['sun'])
    tracks[start] = track
print('day   sunny share, all worlds start rainy   all start sunny   gap')
for d in (0, 1, 2, 3, 4, 5, 10, 20):
    print(f'{d:>3}   {100 * tracks["rain"][d]:26.4f}%   {100 * tracks["sun"][d]:14.4f}%   {100 * (tracks["sun"][d] - tracks["rain"][d]):8.4f}')
ratio = (tracks['sun'][3] - tracks['rain'][3]) / (tracks['sun'][2] - tracks['rain'][2])
print(f'each day the gap is multiplied by {ratio:.2f}')
day = next(d for d in range(31) if tracks['sun'][d] - tracks['rain'][d] < 0.001)
print(f'the gap is under a tenth of a point on day {day}')

# the balance: the share where as many worlds leave sun as come back
balance = 0.5 / (0.1 + 0.5)
print(f'balance: sunny share x 0.1 = rainy share x 0.5  ->  sunny share {100 * balance:.4f}% = 5/6')

# quiz chain: after sun, sun 0.7; after rain, sun 0.2
QUIZ = {'sun': [(0.7, 'sun'), (0.3, 'rain')], 'rain': [(0.2, 'sun'), (0.8, 'rain')]}
guess = 0.2 / (0.3 + 0.2)
counted = sum(s == 'sun' for s in walk(QUIZ, 'rain', 1_000_000)) / 1_000_000
print(f'quiz chain: balance says {100 * guess:.1f}%, a million days give {100 * counted:.2f}%')
save(3, tracks=tracks, ratio=ratio, day=day, balance=balance, quiz=[guess, counted])
