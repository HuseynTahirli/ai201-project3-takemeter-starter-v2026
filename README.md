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

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy |  |  |  |
| Macro F1 |  |  |  |
| F1 — `label_one` |  |  |  |
| F1 — `label_two` |  |  |  |

**What I predicted before I looked:**
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->

**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

| true \ predicted |  |  |  |
|---|---|---|---|
| **** |  |  |  |
| **** |  |  |  |
| **** |  |  |  |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->



---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** ___ / 30 = ___%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**1.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**2.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**What the pattern in my disagreements tells me:**



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->



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
