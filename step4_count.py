"""Step 4. Markov's count of 1913, checked, and then repeated on an English text.  python3 step4_count.py [your.txt]"""
import sys
from save import save

# A. His published counts for the first 20,000 letters of Pushkin's "Eugene Onegin" (see the sources in the README).
LETTERS, VOWELS, VV, CC, MIXED = 20_000, 8_638, 1_104, 3_827, 15_069
cons = LETTERS - VOWELS
share = VOWELS / LETTERS
v_after_v = VV / VOWELS
v_after_c = (MIXED / 2) / cons
fixed = v_after_c / (v_after_c + 1 - v_after_v)          # the balance of step 3
blind = LETTERS * share * share                          # vowel-vowel pairs if letters did not care about each other
print(f'Markov 1913: vowels {100 * share:.2f}% of {LETTERS:,} letters')
print(f'  vowel after a vowel {100 * v_after_v:.1f}%   vowel after a consonant {100 * v_after_c:.1f}%')
print(f'  vowel-vowel pairs: {VV:,} counted; {blind:,.0f} if each letter ignored the one before')
print(f'  balance of his two chances: {100 * fixed:.2f}% vowels; he counted {100 * share:.2f}%')
his = dict(share=share, vv=v_after_v, cv=v_after_c, fixed=fixed, blind=blind)

# B. The same count on our own text.
name = sys.argv[1] if len(sys.argv) > 1 else 'shakespeare.txt'
letters = [c for c in open(name, encoding='utf-8').read().lower() if 'a' <= c <= 'z'][:20_000]
is_v = [c in 'aeiou' for c in letters]
n = len(is_v)
vowels = sum(is_v)
pairs = list(zip(is_v, is_v[1:]))
vv = sum(a and b for a, b in pairs)
cv = sum((not a) and b for a, b in pairs)
p = vowels / n
a_vv = vv / sum(a for a, _ in pairs)
a_cv = cv / sum(not a for a, _ in pairs)
fixed = a_cv / (a_cv + 1 - a_vv)
print(f'{name}: first {n:,} letters, starting "{"".join(letters[:40])}"')
print(f'  vowels {vowels:,} = {100 * p:.2f}%')
print(f'  vowel after a vowel {100 * a_vv:.1f}%   vowel after a consonant {100 * a_cv:.1f}%')
print(f'  vowel-vowel pairs: {vv:,} counted; {n * p * p:,.0f} if each letter ignored the one before')
print(f'  balance of the two chances: {100 * fixed:.2f}% vowels; counted {100 * p:.2f}%')

# does the share settle as we read on?  And how alike are blocks of 100 letters?
running = [sum(is_v[:k]) / k for k in range(50, n + 1, 50)]
for k in (100, 1_000, 5_000, 20_000):
    print(f'  after {k:>6,} letters: {100 * sum(is_v[:k]) / k:.2f}% vowels')
blocks = [sum(is_v[i:i + 100]) for i in range(0, n, 100)]
mean = sum(blocks) / len(blocks)
spread = (sum((b - mean) ** 2 for b in blocks) / len(blocks)) ** 0.5
coin = (100 * p * (1 - p)) ** 0.5
print(f'  {len(blocks)} blocks of 100 letters: {min(blocks)} to {max(blocks)} vowels; typical distance from the average {spread:.2f}')
print(f'  a coin with the same share would give {coin:.2f}')
save(4, his=his, n=n, start=''.join(letters[:300]), vowels=vowels, share=p, vv=vv, vv_blind=n * p * p, a_vv=a_vv, a_cv=a_cv,
     fixed=fixed, running=running, blocks=blocks, spread=spread, coin=coin)
