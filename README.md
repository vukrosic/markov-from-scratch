# Markov from scratch

Code for the video **Become Andrey Markov in 14 Minutes**.
In 1902 Pavel Nekrasov claimed that averages settle only when events are independent. Andrey Markov answered with events that lean on each other, and in 1913 he counted 20,000 letters of a poem by hand to show it.
These seven small programs test the question: do linked events settle too? 364 lines of Python 3, standard library only, nothing to install.

```bash
python3 tests.py      # checks every step
./run_all.sh          # runs all seven, about 40 seconds; expected output is in demo-output.txt
```

| File | Idea | What the run shows |
| --- | --- | --- |
| `step1_coin.py` | Independent events: the coin | One player, a million flips: 50.03% heads. 1,000 players with 100 flips each range from 35% to 65% (30 points apart); with 10,000 flips each, from 48.3% to 51.7% (3.5 points). |
| `step2_weather.py` | Linked events: a chain | Two kinds of day. After sun, sun 9 times in 10; after rain, 1 in 2. A million days from a sunny start give 83.2% sun; from a rainy start, 83.4%. |
| `step3_settle.py` | Why it settles | A crowd of worlds moved by multiplication, no dice. From all rain: 0, 50, 70, 78, 81.2%. From all sun: 100, 90, 86%. The gap is multiplied by 0.4 each day and is under 0.1 points on day 8. Balance gives 5/6. |
| `step4_count.py` | Letters | Markov's published 1913 numbers (8,638 vowels in 20,000 letters; vowel after vowel 12.8%, after consonant 66.3%) and the same count on the first 20,000 letters of `shakespeare.txt`: 38.6% vowels, 17.5% and 51.8%. Blocks of 100 letters sit 2.75 vowels from the average; a coin would give 4.87. |
| `step5_break.py` | When it fails | Two islands of rooms: the share of time on A is 50% or 0%, depending on the start. One small door: 25% from every start. A sticky chain (stays 999 times in 1,000): 200 worlds still range from 37.4% to 65.1% after 100,000 days. |
| `step6_rank.py` | Ranking a web | A random surfer on 7 pages. With links only, the start decides the answer. With a jump to any page 15 times in 100, both starts agree: wiki 26.4%. A crowd of surfers stops changing after 63 steps and matches within 0.04 points. |
| `step7_write.py` | A chain that writes | Next letter drawn from counts in a million letters of Shakespeare. Real words: 12.7% with no memory, 24.3% with 1 letter, 41.4% with 2, 69.4% with 3, 89.8% with 4, 99.2% with 6. With 10 letters: 753,857 states, and 14.7% of its 30-letter pieces are copied word for word. |

`chain.py` holds the shared step and count functions. `save.py` writes each step's numbers to `runs/`; `values.py` collects them for the animation, so every number on screen comes from these runs.

## What this is not

- The weather has two kinds of day and made-up chances. It is a toy, not a forecast.
- The web has 7 pages. The 1998 method ran on millions. Rank measures where a random surfer spends time, not quality.
- Markov's numbers in `step4_count.py` are the ones he published for the Russian text of *Eugene Onegin*; the program does not recount the poem. Our own count is on English.
- `step4_count.py` keeps only the letters a to z. Accented and non-Latin letters are dropped, so a text in another alphabet needs its own vowel list.
- `step7_write.py` is a table of counts. A chatbot runs the same loop (look at the state, draw the next piece, add it), but a neural network works out the chances.
- A table of vowels did not settle the question of free will. It removed one argument: settled averages do not prove independence.

## One experiment not run

`step4_count.py` takes any text file: `python3 step4_count.py yourbook.txt`. Give it 20,000 letters of a book in your language. Is a vowel after a vowel rare there too?

## Sources

`shakespeare.txt` is about a million characters from Shakespeare's plays (public domain). History and Markov's 1913 numbers: MacTutor (St Andrews), "Andrei Andreyevich Markov"; Wikipedia, "Andrey Markov" and "Markov chain"; IEEE Spectrum, "Andrey Markov & Claude Shannon Counted Letters to Build the First Language-Generation Models".

MIT licence.
