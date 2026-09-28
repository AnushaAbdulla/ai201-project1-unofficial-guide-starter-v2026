# The Unofficial Guide

**Anusha Abdulla** · Corpus: `city_guides`

---

# Unit 1

## What This Does

This is a question-answering system built on the `city_guides` corpus. The corpus is a set of Markdown travel guides covering various towns in a fictional region, and travel information relating to them. It is built to answer practical, specific questions a visitor might ask, like when to visit a particular town, or where to find a meal late at night. The way it works is by splitting each guide into topic-sized chunks, it embeds these, and retrieves the closest matches for a given question. There is a relevance gate that checks how close the best match is before deciding whether to answer at all. 

## Chunking Strategy

**Chunk size: 174-759 characters (94 chunks, average 319), split on Markdown headers**
**Overlap: none in practice (100 characters, only used if a section goes over 900)**

Each section already answers one kind of question on its own. So the chunks follow the headers instead of a character count. Measured across all 14 guides, the sections run 23 to 711 characters with a median around 285, so no section needs to be cut to fit.

The 150-character minimum handles the shortest pieces after splitting, which are the headers. On their own they are too short to answer anything, so they are merged into the section that follows. In Unit 2 I made it so that each chunk also starts with its guide's town name, because "## Getting there" on its own doesn't say which town it's about. That's why the final chunks run 174-759 characters rather than the raw 23-711.

## Sample Chunks

======================================================================
Chunk 1  |  source: guide_accessibility.md#0  |  produced by: chunker.py::split_documents
======================================================================
# Getting around the region with limited mobility

An honest assessment rather than a promotional one. Some of these places are
difficult and it is better to know in advance.

======================================================================
Chunk 2  |  source: guide_corry_vale.md#5  |  produced by: chunker.py::split_documents
======================================================================
## Where to stay

Perhaps thirty beds in the entire valley, spread across two pubs and a handful of farmhouse rooms. In summer these are booked months ahead. Camping is permitted on two marked fields and nowhere else.

======================================================================
Chunk 3  |  source: guide_givens_mill.md#2  |  produced by: chunker.py::split_documents
======================================================================
## Getting around

Everything is on one street along the river. The mill is at one end and the church at the other, eight minutes apart. The riverside path continues in both directions for as far as you want to walk.

======================================================================
Chunk 4  |  source: guide_kestrelford.md#4  |  produced by: chunker.py::split_documents
======================================================================
## What to see

The market square on a Saturday morning is the main event and has run continuously since the 1400s. The parish church has a 13th-century tower you can climb for £2. The old trackbed walk runs six miles to the next village along an easy gradient and is the best half-day here.

======================================================================
Chunk 5  |  source: guide_pellew_sands.md#6  |  produced by: chunker.py::split_documents
======================================================================
## When to go

June and September for the beach without the crowds. July and August are busy and the town is at its most itself, for better and worse. Winter is bleak, largely closed, and has a following among people who like that sort of thing.



## Sample Answer

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->

**Question:** Which town is the most accessible?

**Answer:**

```
According to guide_accessibility.md, Thornby Wells is the easiest (most accessible) town in the region because it is flat, compact, and everything is within three minutes of everything else.
```

**My relevance cutoff:** 0.6

<!-- The number you set in config.py, and how you got there.

     You ran five questions your corpus covers and the five in OUT_OF_SCOPE
     that it clearly doesn't, and wrote down the best distance for each. What
     did those two groups look like? Where was the gap? Put the actual numbers
     here — the table below wants all ten rows.

     Milestone 4. -->

| Question | In corpus? | Best distance |
|---|---|---|
| Which town is the most accessible? | yes | 0.494 |
| What is the best time to visit Elder Ness? | yes | 0.370 |
| What is the best way to travel to Kestrelford? | yes | 0.451 |
| Where can I eat late at night? | yes | 0.525 |
| Which town has the best nightlife? | yes | 0.557 |
| What is the capital of Mongolia? | no | 0.887 |
| How do I change the oil in a diesel engine? | no | 0.897 |
| Who won the 1994 World Cup? | no | 0.903 |
| What is the recommended dosage of ibuprofen for a headache? | no | 0.836 |
| How do I write a for loop in Rust? | no | 0.853 |

## How I Used AI

1. 
     I asked Claude "Here are five acceptance criteria for a retrieval system. For each one, tell me exactly how you would test it using only what the sentence says. The last two are not so good suggest improvements".

     I showed me what it would expect the system to show and how to test which was super straightforward, but then it suggested checking source hallucinations and excessive detail.

2. 
     I asked Claude "Where in this repo does the prompt live?"

     It returned a file name, a line number, and an explination of what exsited based on comments.



<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2


## Run Log — Before


| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Answer is complete without excess detail | 4 of 5 | 4/5 | 4/5 | 3/5 | MISSED |
| 5. Named sources are correct, not just present | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |

1. Which town is the most accessible? — run 1
     
     Answer: Based on the documents, Thornby Wells is described as the easiest town in the region for getting around with limited mobility. 
     
     Source: guide_accessibility.md

2. Should I take cash or card to elder ness? — run 1

     Answer: Cash is still useful at markets and in the smaller villages, and Elder Ness has one shop which is closed on Sundays and after 5pm. 
     
     Source: guide_eating.md

3. What is the best way to travel to Kestrelford? — run 1

    Answer: Based on the provided documents, you can travel to Kestrelford by bus (running roughly hourly on weekdays, every two hours on Saturdays, and not on Sundays from Brightwater), on foot along the old railway trackbed (which now serves as a walking route), or by driving (taking 55 minutes, with the last eight miles on a single-track road). 
     
     Source: guide_kestrelford.md

4. Where can I eat late at night? — run 1

    Answer: Based on the provided documents, kitchens across the region stop serving at 9pm and often earlier, and everything in Halden Bay closes by 9pm. 
     
     Source: guide_eating.md

5. What should I do in Marchwood? — run 1

    Answer: Based on the provided documents, you can visit the city museum, which is free and has an excellent industrial floor, and check out the covered market that has operated since 1863 (best visited on a weekday morning). You can also take a canal walk from Northgate to the old lock (which takes 40 minutes) and eat in the Northgate district, where about thirty restaurants are located. 
     
     Source: guide_marchwood.md
 


## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

Note: Hello! I did rewrite my questions before beginning the experiments. This was done under the guidance of a mentor (TF? I forgot the acronym) during class. Thank you!

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunk contains the answer | MET | Every chunk contained the answer to the question. The code I wrote to check and the answers it was checking against was insufficient, however the answer was correctly present in the chunk intended.  |
| 2 | Every answer names a source | MET | Every answer named a source whether embeded in the sentence or declared at the end of a response.  |
| 3 | Gate stops out-of-corpus questions | MET | None of the out-of-corpus questions were answered all were refused outright. |
| 4 | Answer is complete without excess detail | MISSED | Some answers provided excessive detail. While I rewrote and changed some questions this was not sufficient as the model was sometimes unclear on how much information the user required.  |
| 5 | Named sources are correct, not just present | MET | All sources were named and correct in every single response. |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

All four misses are on criterion 4 (answer is complete without excess detail), but they come from two different causes. These Before runs used the starter's `chunker.py::fallback_split` (fixed 800-character windows, 120 overlap), because I hadn't rebuilt the index after writing my own chunker.

**Miss 1–3: "Where can I eat late at night?" (all three runs) — chunking → retrieval, then generation.**
I first thought the corpus had no direct answer, but it does: `guide_marchwood.md` says Marchwood "keeps later hours than anywhere else in the region — kitchens serve until 10:30pm, and until midnight on Fridays and Saturdays." The fixed 800-character window put that sentence in chunk `guide_marchwood.md#1`, which starts mid-sentence in the transport section ("til midnight. A day ticket…"), then covers "Eat and drink", then runs into "What to see". Because that one chunk mixes transport, food, and sights, it ranked 13th, and only the top 5 are retrieved. What was retrieved instead was `guide_eating.md`'s line "Outside Marchwood, kitchens across the region stop serving at 9pm", which only answers the question by implication. The grounding prompt tells the model "Do not guess", so it repeated the negative part ("kitchens stop at 9pm") and never named Marchwood as the place that stays open.

**Miss 4: "Which town is the most accessible?" (run 3) — generation.**
Retrieval was fine: the top chunk, `guide_accessibility.md#0`, has the answer. But the sentence naming Thornby Wells sits in one paragraph with every supporting detail — flat, compact, free parking, central station, level pump room and gardens. The grounding prompt limits length ("Two or three sentences is usually enough") but not scope — it never says to answer only what was asked. With caching off, each run is a fresh sample, and in run 3 the model packed the whole paragraph into its answer instead of just naming the town. Runs 1 and 2 had the same chunk and the same prompt and stayed short, so this is the prompt allowing excess detail, not requiring it.

## The Improvement

**What I changed:**
Switched chunking from `chunker.py::fallback_split` (fixed 800-character windows) to `chunker.py::split_documents` (one chunk per `##` section), indexed as variant `headers`, and ran the same five questions against it: `python run_eval.py --variant headers --label after`.

**Why I picked it:**
It targets misses 1–3: the late-night answer ranked 13th because the fixed window mixed Marchwood's transport, food, and sights into one chunk, so a chunk containing only Marchwood's "Eat and drink" section should sit much closer to a question about eating and make it into the top 5. It doesn't target miss 4, which is a generation problem — that would need a prompt change, and I kept this to one change so I could tell what it did.

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 3/5 | 3/5 | 3/5 | MISSED |
| 2. Every answer names a source | 5 of 5 | 3/5 | 3/5 | 3/5 | MISSED |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Answer is complete without excess detail | 4 of 5 | 1/5 | 2/5 | 2/5 | MISSED |
| 5. Named sources are correct, not just present | 4 of 5 | 3/5 | 3/5 | 3/5 | MISSED |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

No, it made things worse. Before, only criterion 4 was missed; after, criteria 1, 2, 4, and 5 are all missed, and two questions that used to work (Kestrelford, cash or card) now fail every run. I know it was the chunking and not the model because I checked where the chunk containing each answer ranked in both indexes (`store.py::search` with `top_k` set to all 94 chunks), and only the top 5 are sent to the model.

**Why: splitting at headers cut each section off from the name of its town.** In every guide, the town name only appears in the `# Title` line at the top. With fixed 800-character windows, the title and the first sections landed in the same chunk. With header splitting, the title and intro became their own chunk, and every section after it no longer mentions which town it's about.

- **Kestrelford.** The "Getting there" chunk (no railway, buses from Brightwater, 55-minute drive) starts "No railway station…" and never says "Kestrelford". It dropped from **1st to 75th** of 94. The model got general road notes from `guide_regional_transport.md` and `guide_walking.md` instead, and said the documents don't mention the best way to travel there.
- **Cash or card.** Every guide's "Practical notes" section is word-for-word identical ("Cash is still useful at the market… cards are accepted almost everywhere now"). Without the town name, the search can't tell Elder Ness's copy from any other: Elder Ness's own ranked 10th, and the top 5 included the identical Brightwater, Kestrelford and Corry Vale copies. The model most likely couldn't tie any of them to Elder Ness, so it refused all three runs.
- **Late night.** This is the miss the change was meant to fix, and it only half worked. Marchwood's "Eat and drink" section is now its own chunk and moved from **13th to 8th**, still outside the top 5. The question doesn't name a town, so Marchwood's food section looks like every other town's food section — the top 5 were the "Eat and drink" sections of Pellew Sands, Kestrelford, Corry Vale and Elder Ness. Meanwhile, the "Outside Marchwood… 9pm" line that at least hinted at the answer dropped from 2nd to 6th, so the model got nothing useful and refused.

**One thing got better:** the accessibility answer was short and complete in all three runs (the Before run 3 had excess detail). The right chunk was retrieved in both versions (1st before, 4th after), so I can't attribute this to the chunking change. It may just be run-to-run variation in how the model writes.

**Takeaway:** header splitting was the right idea for this corpus, since the sections are self-contained. But it needs the town name carried into each chunk. That's the next change I'd make.

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->
     The reason it's broken here is because the title/town name is cut off in all the chunks! This means the model can find information but not tie it to a certain city.

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->

     I wouldn't rewtite criteria yet. I think criteria 5 is weak, but the real issue here is likely still my chunking and judging code. 
     
## How I used AI:

This unit I asked AI to show me where my certain answers were showing up in the chunk rankings. With this information I looked and noticed I wasn't using my own chunks yet. 