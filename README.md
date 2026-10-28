# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Your community, and what your classifier sorts posts into. Three or four
     sentences. -->

My community is r/playstation, a public subreddit with about 2 million
members. It covers the whole platform rather than a single game or release,
so there is no spoiler problem tied to one title's launch window.

Reddit blocks scripts from my network, and the API now requires approval I
don't have. So I logged into Reddit in my browser, ran searches, and saved
the resulting JSON pages by hand into `data/raw/`. `scripts/parse_raw.py`
reads those pages, keeps only real self posts from r/playstation (dropping
ads, stickied posts, mod megathreads, and posts with too little text), and
dedupes the result. That took 343 raw posts down to 269 after filtering.

Reading through those 269, four candidate distinctions stood out as things I
could actually point at in the text:

1. Whether a specific fact is carrying the argument, or is just decoration on
   a conclusion the writer already had.
2. Whether the post is about something that just happened to the writer,
   versus a general claim about the platform or the industry.
3. Whether the post offers any support for its claim, or is a bare
   assertion.
4. Whether the post is asking a question or looking for help, rather than
   making a claim at all.

The classifier sorts posts into four labels: `question`, `analysis`,
`hot_take`, and `share`.

---

## Label Taxonomy

<!-- Each label: a one-sentence definition and two real examples from your
     reading. Then your decision rule for the hardest boundary.

     The decision rule is worth a point on its own and it's the thing most
     people leave out. Every taxonomy has a hardest boundary. Name yours. -->

### `question`

**Definition:** The main point is to get an answer from the community, in
the form of help, info, or a recommendation.

**Example 1:**
> "Help! I want to gift my bf a PS5 for his birthday but I don't know which
> one to get... I want to know which one to get him... just want to make
> sure he can play GTA6 on it when it releases."

**Example 2:**
> "Just Bought a PS5... Anyone got any game recommendations?"

### `analysis`

**Definition:** Makes a claim and backs it with something checkable, like a
price, a date, a number, a specific game detail, or a quote.

**Example 1:**
> "ps5 pro is $1400 in Australia... base ps5 is $1000 and ps5 pro is $1400.
> Im pretty sure when ps5 released, it was around $700... and when ps5 pro
> released, it was $1150."

**Example 2:**
> "The time in between each PlayStation unveiling. PS1 (10/27/93) -> PS2
> (9/20/99) - 5y, 10m, 24d... PS4 -> PS5 (4/16/19) - 6y, 1m, 27d. Currently,
> it's been 6y, 9m, 11d since the PS5 unveiling."

### `hot_take`

**Definition:** Makes a claim or complaint with no checkable support. Rants
land here.

**Example 1:**
> "Am I the only one that would love a 'Buy a game for a friend' option on
> the PlayStation store?... the hassle of buying a PSN card... seems like a
> much crappier option."

**Example 2:**
> "Can't stand it when games make you mash the button as fast as possible
> sometimes. I'm not trying to wear out the buttons on my $200 DualSense
> Edge so I can win arm wrestling."

### `share`

**Definition:** The writer tells about something that happened to them or
how they feel, without arguing a claim beyond their own experience and
without asking for an answer.

**Example 1:**
> "Had to say Rest In Peace to my PS3... After two days i was told she is
> 'unfixable'. It sucks because it boots up, the sounds are there but i just
> can't see anything. Ugh, heart is broken."

**Example 2:**
> "It's a rather sad day. I pulled my PS3 out, got it all set up, turned it
> on, and was met with a screen I never wanted to see. HDD finally crapped
> out... I've just had this one since 2009."

**A note on where this label came from:** I added `share` after noticing
that about a quarter of the posts I read were personal stories or
celebrations, like "I finally bought a PS5," that did not fit `question`,
`analysis`, or `hot_take`.

### The hardest boundary

**Which two labels:** `question` vs `hot_take`.

**The decision rule I used every time:** If the ask can be answered with a
fact or a fix, it's `question`. If it's an opinion followed by "anyone
else?" or "am I the only one?", it's `hot_take`.

**The rule in action, on a real borderline post:**
> "PS5 music is lonely? Does anyone else get a sudden wave of loneliness
> right when they quit a game and hear that PS5 menu music?"

This is grammatically a question, and it even has a question mark twice. But
there is no fact or fix that answers it. The writer is not asking for help,
they are sharing a feeling and inviting others to say they feel it too. By
the rule, that makes it `hot_take`, not `question`.

**A second hardest boundary:** `analysis` vs `hot_take`.

**The decision rule I used every time:** A fact only counts if it's the
reason for the claim. A number that doesn't support the conclusion is
decoration, and the post is `hot_take`.

I added this rule after the stress test found a hole. Post #5 in
`data/stress_test.md` states a real sales number for Elden Ring Nightreign,
then jumps to a conclusion the number doesn't actually support. The fact is
there, but it isn't doing the work, so the post is `hot_take`, not
`analysis`.

**A third hardest boundary:** `share` vs `hot_take`.

**The decision rule I used every time:** If the post makes a judgment about
a game, company, or thing beyond "how I felt," it's `hot_take` (or
`analysis` if a fact is the reason for that judgment). If it stays on the
writer's own experience, it's `share`.

**A fourth hardest boundary:** `share` vs `question`.

**The decision rule I used every time:** If a personal story ends with a
real ask that a fact or recommendation could answer, it's `question`.

---

## The Dataset

<!-- Where you collected from, how you labelled, your counts, and three hard
     cases. -->

**Where the posts came from:** r/playstation text posts. Reddit blocks
scripts from my network, and API apps now need approval I don't have, so I
logged into Reddit in my browser, ran searches, and saved the result pages
as JSON by hand. `scripts/parse_raw.py` parsed those pages and filtered out
ads, image posts, mod and stickied posts, posts that were too short or
deleted, and duplicates. That took 343 raw posts down to 269.

**How I labelled them:** None of these were labelled cold by me. The first
20 (the cold20 sample) were labelled by Claude in chat, noted
`claude_label` in labels.csv. The remaining 249 were pre-labelled by Claude
Code under my taxonomy and decision rules, noted `ai_prelabel`. I did not
review the pre-labels row by row.

**Counts per label:**

| Label | Count | Share |
|---|---|---|
| `question` | 118 | 43.9% |
| `hot_take` | 63 | 23.4% |
| `share` | 47 | 17.5% |
| `analysis` | 41 | 15.2% |
| **Total** | 269 | 100% |

`analysis` is the thinnest label, with only about 6 posts landing in the
test split. Its F1 will be jumpy in Unit 6 because of that.

**Three hard cases**

<!-- Any post that made you pause: what it was, which two labels it could have
     been, and what you chose. These are worth more than the easy 190. -->

**1.**
> *The post:* "Should I feel bad?... There are many games that I haven't
> played yet or just haven't finished... I'm wondering if other people feel
> the same way. Do you care to beat a game that's not fun or might be too
> big? How often do you guys actually finish a game?"
>
> *Could have been:* `share` or `question`
>
> *I chose, because:* It reads mostly like a personal reflection on an
> unfinished backlog, and the closing questions feel more like venting out
> loud than a real ask a fact or recommendation could answer. I called it
> `share`.

**2.**
> *The post:* "UK Parliment Petition to aquire legal protections for
> consumers on their video games... An official parliment petition has been
> created to go against Playstation's recent statement to stop production
> of physical discs. Please sign to have a real governing body take
> action... [link to petition]"
>
> *Could have been:* `analysis` or `hot_take`
>
> *I chose, because:* It reads like a share-this call to action, but the
> petition itself, its wording, and the link are the checkable fact the
> whole post exists to deliver. I called it `analysis`.

**3.**
> *The post:* "GTA 6 isn't 'too advanced' for Current Gen, Devs Just Wasted
> Current-Gen's Potential... How many true 'next-gen' exclusives have we
> seen that look drastically better than PS4/Xbox One titles? Very few...
> So no, GTA 6 isn't 'too advanced' for PS5 or Xbox Series X, it's just the
> first major game to prove what these consoles were always capable of."
>
> *Could have been:* `analysis` or `hot_take`
>
> *I chose, because:* It makes a developer-effort argument, but the
> "evidence" (how few true next-gen exclusives we've seen) is a rhetorical
> impression, not a specific checkable number. The fact isn't really
> load-bearing, so I called it `hot_take`.

---

## The Training Run

<!-- Your starting model, your settings, and anything you changed and why. -->

**Base model:** `distilbert-base-uncased`

**Settings:** 3 epochs, learning rate 2e-5, batch size 16, max length 128,
seed 42.

**Anything I changed from the defaults, and why:** Nothing. All settings
are the notebook's defaults.

**Device:** CPU (torch 2.14.1+cpu), recorded in `results.json`.

**Split sizes:** train 187, val 41, test 41 (70/15/15 of 269 rows).

Per-label counts in the test split:

| Label | Train | Val | Test |
|---|---|---|---|
| `question` | 82 | 18 | 18 |
| `hot_take` | 43 | 10 | 10 |
| `share` | 33 | 7 | 7 |
| `analysis` | 29 | 6 | 6 |

`analysis` and `share` both have fewer than 8 examples in the test split,
so their F1 scores will move around a lot between seeds.

---

## How I Used AI

<!-- Two specific moments — what you asked, what came back, what you changed.

     ⚠️ Plus disclosure of any pre-labelling. If you had a model pre-label a
     batch and then read and corrected every one, say that. It's an allowed
     workflow and disclosing it costs you nothing. Not disclosing it is the
     problem. -->

**Moment 1**

- *What I asked for:* Claude wrote 8 made-up posts sitting right on my
  label boundaries, as a stress test of the taxonomy, with no answers
  given.
- *What came back:* Post #5 was a sales figure for Elden Ring Nightreign
  followed by a conclusion the number didn't actually support. Under my
  original taxonomy that would have counted as `analysis`, since it had a
  checkable fact in it.
- *What I changed:* I added a decision rule: a fact only counts if it's
  the reason for the claim. A number that doesn't support the conclusion
  is decoration, and the post is `hot_take`.

**Moment 2**

- *What I asked for:* I had Claude pull and read 20 random real posts
  (cold20) from the collected data so I could look for patterns before
  finalizing labels.
- *What came back:* About a quarter of those 20 were personal stories or
  celebrations, like "I finally bought a PS5," that didn't fit `question`,
  `analysis`, or `hot_take`.
- *What I changed:* I added a fourth label, `share`, with its own
  definition and two new decision rules against `hot_take` and `question`.

**Pre-labelling disclosure:** Claude drafted the five acceptance criteria
in `criteria.md` and I reviewed them. Claude labeled all 20 cold20 posts in
chat (`claude_label`). Claude Code then pre-labeled the remaining 249 posts
under my taxonomy and decision rules (`ai_prelabel`), and I did not review
those row by row. Claude Code also wrote the collection and parsing
scripts (`scripts/collect.py`, `scripts/parse_raw.py`).

**Unit 6 improvement disclosure:** Claude Code diagnosed the undertraining from the before-run loss numbers and ran the after run (10 epochs, three seeds). Claude helped plan the improvement.

**Staff set disclosure:** Claude, not me, labeled the 30 posts in
`my_staff_labels.csv` under the staff taxonomy. I did not label them myself.
So the agreement rate below says how well Claude applies the staff rules, not
how consistent I am.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline Prediction

I think the trained model will beat the baseline most on `hot_take` and `share`, because those two depend on how I drew the lines in my own labels, and a general model reading one-line definitions won't know that. I expect the baseline to do fine on `question`.

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy | 0.220 | 0.439 | +0.220 |
| Macro F1 | 0.163 | 0.153 | -0.011 |
| F1 — `analysis` | 0.300 | 0.000 | -0.300 |
| F1 — `hot_take` | 0.154 | 0.000 | -0.154 |
| F1 — `question` | 0.200 | 0.610 | +0.410 |
| F1 — `share` | 0.000 | 0.000 | +0.000 |

The baseline was run with `label_definitions.txt` on `test_split.csv`.

**What I predicted before I looked:**
I thought the trained model would beat the baseline most on hot_take and share, and that the baseline would do fine on question.

**What the gap actually means:**
The trained model scored 0.439 accuracy against the baseline's 0.220, but that gain is not real learning. 18 of the 41 test posts are question, and 18/41 is 0.439, so the model appears to predict question for almost everything. Macro F1 is about the same (0.153 trained vs 0.163 baseline), and the trained model got 0.000 F1 on analysis, hot_take, and share. My prediction was wrong. The baseline was bad at everything, and the trained model was only good at the biggest class.



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

The run used the cpu device with seeds 42, 7, and 2024.

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| C1 Overall accuracy | at least 0.70 | 0.439 | 0.439 | 0.439 | MISSED |
| C2 Lowest per-label F1 | at least 0.55 | 0.000 (analysis, hot_take, share all tied) | 0.000 (analysis, hot_take, share all tied) | 0.000 (analysis, hot_take, share all tied) | MISSED |
| C3 Largest label share in labels.csv | at most 65% | question 43.87% (118 of 269) | same, labels.csv does not change by seed | same | MET |
| C4 Staff agreement | at least 21 of 30 | 30 of 30 | same, one measurement | same | MET |
| C5 Accuracy of most-confident third minus least-confident third | at least 0.15 | 0.692 - 0.154 = 0.538 | 0.615 - 0.385 = 0.231 | 0.615 - 0.154 = 0.462 | MET |

Notes on the table:

- All three seeds gave the same confusion matrix. The model predicted question for all 41 test posts every time, so accuracy is exactly 18 of 41. Question is the only label with a nonzero F1, at 0.610.
- C3 is about labels.csv, so it is the same number for every seed. The other label shares are hot_take 23.42% (63), share 17.47% (47) and analysis 15.24% (41).
- C4 is one measurement, not three. It does not depend on the seed.
- C5 uses 13 posts per third, so one post moves a third by 7.7 points. Seed 7 is the thinnest pass at 0.231.

### Confusion matrix

| true \ predicted | question | analysis | hot_take | share |
|---|---|---|---|---|
| **question** | 18 | 0 | 0 | 0 |
| **analysis** | 6 | 0 | 0 | 0 |
| **hot_take** | 10 | 0 | 0 | 0 |
| **share** | 7 | 0 | 0 | 0 |

**My biggest off-diagonal number, and what it means:**
The biggest confusion is 10 real hot_take posts called question, but the model predicted question for all 41 test posts, so every other label was confused with question.



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Overall accuracy | at least 0.70 | MISSED | 0.439 on all three seeds, so it fails every seed. |
| 2 | Lowest per-label F1 | at least 0.55 | MISSED | Three labels (analysis, hot_take, share) have F1 0.000 on every seed. Only question clears 0.55, at 0.610. |
| 3 | Largest label share | at most 65% | MET | The biggest label is question at 43.87%, well under 65%. |
| 4 | Staff agreement | at least 21 of 30 | MET | 30 of 30 on one measurement. |
| 5 | Confident third vs unsure third | at least 0.15 | MET | The gap is 0.538, 0.231 and 0.462, so every seed is above 0.15. Technically met but hollow in the before run, see the diagnosis. After run: met for real, see Run Log — After. |

**Diagnoses**

The agreement check had 0 disagreements, so it can't be used as evidence for or against a labeling problem here. The diagnosis below rests on the confusion matrix, the test split counts and `data/hard_cases.md`.

**C1 and C2 have the same main cause: undertraining. Thin analysis and share data is a contributing factor.**

- *The loss barely moved.* The run was about 187 training posts at batch 16 for 3 epochs, which is 12 steps per epoch and 36 steps in total. The loss numbers from the before run (training loss is logged at steps 10, 20 and 30, validation loss at the end of each epoch. The validation set is the separate 15% validation split, not the test split):

| Seed | Train loss (step 10, 20, 30) | Validation loss (epoch 1, 2, 3) | Average train loss |
|---|---|---|---|
| 42 | 1.348, 1.259, 1.229 | 1.275, 1.234, 1.216 | 1.259 |
| 7 | 1.342, 1.278, 1.217 | 1.279, 1.238, 1.222 | 1.273 |
| 2024 | 1.349, 1.256, 1.250 | 1.270, 1.228, 1.214 | 1.268 |

  Random guessing across 4 labels gives a loss of about 1.386 (ln 4). Predicting the label shares in labels.csv every time gives about 1.29. Training started near 1.35 and finished near 1.22 on every seed, so it only just got below the "guess the label shares" level. That is not enough movement to learn anything past always saying question. Validation accuracy was 0.439 and validation macro F1 was 0.153 at every epoch on every seed, so nothing changed in the predictions at any point.
- *The matrix:* the model put all 41 test posts in question on every seed. The true counts in the test split are question 18, hot_take 10, share 7 and analysis 6. So 10 hot_take, 7 share and 6 analysis posts were all called question, and nothing was ever predicted as analysis, hot_take or share. This is the model sitting on the majority label because it never got enough steps to move off it.
- *Accuracy is just the question share of the test set (C1):* always guessing question gets 18 of 41, which is 0.439, the same as the model. criteria.md estimated always-question at about 0.56. That estimate came from a rough question-mark count during planning and was wrong. On the real test split it is 0.439, so the model did no better than that guess. I did not edit criteria.md.
- *Why not a labeling problem on one boundary:* an inconsistent boundary would show up as two labels swapping, like hot_take and analysis. The matrix has no swaps because the model never predicts those labels at all.
- *Contributing factor, too few examples:* analysis has 41 posts in labels.csv with only 6 in the test split, and share has 47 with 7 in the test split. Question has 118 and hot_take has 63. With so few steps, the thin labels give the model even less to pick up.
- *Hard cases on the same pairs:* `data/hard_cases.md` has 31 hard cases. The pairs that match the matrix errors are share or question (6), analysis or question (4 plus 1 listed the other way, so 5) and hot_take or question (4 plus 1, so 5). That is 16 of the 31, so these are real fuzzy pairs, but they are only a small part of why the model predicted question for everything. The biggest hard pair, analysis or hot_take at 8 cases, can't be checked here because the model never predicted either one.

**C3 and C4 were met, so no diagnosis.**

**C5 is technically MET but hollow.** Every seed is above 0.15, so by the rule I wrote it is met. But the model predicts question for every post, so the confidence only measures how question-like a post looks, not whether the model knows when it is right. The most-confident third is just the posts that look most like questions, and those are the ones the all-question guess gets right. With 13 posts per third it is also a weak signal. I'm not counting this as evidence that the confidence score is useful.

**C5 after the improvement:** it is MET for real. The after model predicts all four labels, and the gap between the most-confident third and the least-confident third is 0.385, 0.462 and 0.385, so the confidence now separates right guesses from wrong ones better than before. It is still only 13 posts per third.



---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** 30 / 30 = 100%

That is against `data/staff_labels.csv`, with 0 disagreements, so there is
nothing to adjudicate.

**Who labeled these:** Claude labeled the 30 posts, not me. The rate measures
whether Claude applies the staff rules the way staff does. It does not measure
my own consistency.

**Why it came out perfect:** I don't think this proves the rules are tight. The
30 posts sorted into three clean blocks. Posts 1 to 10 are data-backed
arguments, 11 to 20 are one-line opinions, and 21 to 30 are in-the-moment
feelings. The borderline ones were covered by the written rules. For example
#14 has a real 3% stat but the conclusion doesn't follow from it, so rule 1
makes it `hot_take`. So this was more an easy set than proof of tight rules.

**What this means for my diagnosis:** With zero disagreements the agreement
check can't tell a labeling problem from a model problem. The Verdicts and
Diagnoses section relies on the confusion matrix and `data/hard_cases.md`
instead.


---

## The Improvement

**What I changed:** EPOCHS went from 3 to 10. Nothing else changed. Learning rate 2e-5, batch size 16, max length 128, the labels and labels.csv are all the same as the before run.

**Which diagnosis pointed at it:** the before run predicted question for every post. The loss only went from about 1.35 to about 1.22 over 36 steps, which is barely below the level of just guessing the label shares, so the diagnosis was undertraining. 10 epochs is 120 steps.

Seed 42 loss per epoch in the after run. Train loss is the latest value logged by the end of that epoch. Validation loss and accuracy are on the separate 15% validation split, not the test split.

| Epoch | Train loss | Validation loss | Validation accuracy |
|---|---|---|---|
| 1 | 1.344 | 1.266 | 0.439 |
| 2 | 1.251 | 1.204 | 0.439 |
| 3 | 1.185 | 1.133 | 0.439 |
| 4 | 1.048 | 1.080 | 0.561 |
| 5 | 0.946 | 1.021 | 0.585 |
| 6 | 0.849 | 0.961 | 0.610 |
| 7 | 0.742 | 0.913 | 0.610 |
| 8 | 0.724 | 0.895 | 0.610 |
| 9 | 0.642 | 0.888 | 0.683 |
| 10 | 0.618 | 0.873 | 0.634 |

The model sat on the all-question guess for the first 3 epochs and started to move off it at epoch 4.

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| C1 Overall accuracy | at least 0.70 | 0.585 | 0.463 | 0.610 | MISSED |
| C2 Lowest per-label F1 | at least 0.55 | 0.200 (share) | 0.250 (hot_take) | 0.400 (hot_take) | MISSED |
| C3 Largest label share in labels.csv | at most 65% | question 43.87% (118 of 269) | same, labels.csv does not change by seed | same | MET |
| C4 Staff agreement | at least 21 of 30 | 30 of 30 | same, one measurement | same | MET |
| C5 Accuracy of most-confident third minus least-confident third | at least 0.15 | 0.846 - 0.462 = 0.385 | 0.692 - 0.231 = 0.462 | 0.769 - 0.385 = 0.385 | MET |

Before vs after, averaged across the three seeds:

| Measure | Before | After | Difference |
|---|---|---|---|
| Accuracy | 0.439 | 0.553 | +0.114 |
| Macro F1 | 0.153 | 0.498 | +0.345 |
| F1 question | 0.610 | 0.681 | +0.071 |
| F1 analysis | 0.000 | 0.626 | +0.626 |
| F1 hot_take | 0.000 | 0.350 | +0.350 |
| F1 share | 0.000 | 0.333 | +0.333 |

**Did it help, and how do I know:** Yes, it got the model off the all-question guess, and every label now has an F1 above zero, but it still missed C1 and C2. Accuracy moved 0.146 across the three seeds (0.463 to 0.610), which is over 10 points, so with only 41 test posts this measure is unstable.

After confusion matrix, seed 42:

| true \ predicted | question | analysis | hot_take | share |
|---|---|---|---|---|
| **question** | 16 | 0 | 1 | 1 |
| **analysis** | 1 | 3 | 2 | 0 |
| **hot_take** | 5 | 0 | 4 | 1 |
| **share** | 3 | 0 | 3 | 1 |

The biggest off-diagonal number is 5 real hot_take posts called question, so the model still leans toward question on that pair.



---

## What's Still Broken

**C1 (accuracy at least 0.70) and C2 (every label F1 at least 0.55) are still missed.** The best seed got 0.610 accuracy and the lowest per-label F1 was 0.200, 0.250 and 0.400 across the seeds. Share and hot_take are the weak labels.

What I'd do next:

- Collect more hot_take and share examples. Share has 47 posts and hot_take has 63 in labels.csv, with only 7 and 10 of them in the test split.
- Relabel the share vs hot_take vs question boundaries using `data/hard_cases.md`. 16 of the 31 hard cases are on question pairs, so that is where the labels are fuzziest.
- Then train again and see if the weak labels come up.

Why I stopped: this unit allows one improvement, and I used it on the training length because the loss numbers pointed straight at it. More data and relabeling would be a second change.

**The gap between what I meant my labels to capture and what the model
learned:**

I meant share to be personal stories about the writer's own experience, but in the seed 42 matrix the model splits them between question (3) and hot_take (3) and only gets 1 of 7 right. So it probably learned surface cues like question marks and strong wording instead of whether the post is about the writer's own experience.



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
