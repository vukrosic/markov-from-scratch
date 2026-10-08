"""A chain: the next state is drawn from a row of chances that belongs to the state we are in now. Nothing older counts."""
import random


def walk(rows, start, steps, rng=random):
    """Yield `steps` states. rows[s] is a list of (chance, next state) for state s."""
    s = start
    for _ in range(steps):
        r, total = rng.random(), 0.0
        for chance, nxt in rows[s]:
            total += chance
            if r < total:
                s = nxt
                break
        yield s


def cloud_step(rows, cloud):
    """One step for a whole crowd at once: cloud[s] is the share of the crowd standing on state s."""
    new = {s: 0.0 for s in rows}
    for s, share in cloud.items():
        for chance, nxt in rows[s]:
            new[nxt] += share * chance
    return new
