"""Step 6. A chain that ranks pages. A surfer clicks a random link; the share of time on a page is its rank."""
import random
from chain import walk, cloud_step
from save import save

random.seed(1998)
# a small web: page -> the pages it links to.  'club' and 'fans' are an island: they link only to each other.
LINKS = {'news': ['wiki', 'shop'], 'wiki': ['news', 'blog', 'maps'], 'shop': ['wiki'], 'blog': ['wiki', 'news'],
         'maps': ['wiki', 'shop'], 'club': ['fans'], 'fans': ['club']}
PAGES = list(LINKS)


def rows(jump):
    """Follow a link with chance 1 - jump; with chance `jump`, go to any page at all."""
    out = {}
    for p in PAGES:
        row = {q: jump / len(PAGES) for q in PAGES}
        for q in LINKS[p]:
            row[q] += (1 - jump) / len(LINKS[p])
        out[p] = [(c, q) for q, c in row.items() if c > 0]
    return out


def show(title, rank):
    print(title, '  '.join(f'{p} {100 * rank[p]:.1f}%' for p in sorted(PAGES, key=lambda p: -rank[p])))


# 1. links only: the answer depends on where the surfer starts (the islands of step 5)
N = 1_000_000
only = {}
for start in ('news', 'club'):
    seen = {s: 0 for s in PAGES}
    for s in walk(rows(0.0), start, N):
        seen[s] += 1
    only[start] = {p: c / N for p, c in seen.items()}
    show(f'links only, start on {start}:        ', only[start])

# 2. with a jump to a random page 15 times in 100 (the 0.85 of the first search engine papers)
R = rows(0.15)
ranks = {}
for start in ('news', 'club'):
    seen = {s: 0 for s in PAGES}
    for s in walk(R, start, N):
        seen[s] += 1
    ranks[start] = {p: c / N for p, c in seen.items()}
    show(f'with the jump, start on {start:<5}:    ', ranks[start])

# 3. the same ranks with no dice: a crowd, moved step by step until it stops changing
cloud, steps = {p: 1.0 if p == 'news' else 0.0 for p in PAGES}, 0
while True:
    new = cloud_step(R, cloud)
    steps += 1
    if max(abs(new[p] - cloud[p]) for p in PAGES) < 1e-6:
        break
    cloud = new
show(f'the crowd, still after {steps} steps: ', new)
diff = round(100 * max(abs(new[p] - ranks["news"][p]) for p in PAGES), 2)
print('largest difference between the surfer and the crowd:', f'{diff:.2f} points')
print('links pointing at each page:', {p: sum(p in v for v in LINKS.values()) for p in PAGES})
save(6, links=LINKS, only=only, ranks=ranks, crowd=new, steps=steps, diff=diff, inl={p: sum(p in v for v in LINKS.values()) for p in PAGES})
