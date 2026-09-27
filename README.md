# The Unofficial Guide

<!-- Replace this line with your name and which corpus you picked. -->

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

This is a question-answering system built on the `city_guides` corpus. The corpus is a set of Markdown travel guides covering various towns in a fictional region, and travel information relating to them. It is built to answer practical, specific questions a visitor might ask, like when to visit a particular town, or where to find a meal late at night. The way it works is by splitting each guide into topic-sized chunks, it embeds these, and retrieves the closest matches for a given question. There is a relevance gate that checks how close the best match is before deciding whether to answer at all. 

## Chunking Strategy

**Chunk size: 150-711**
**Overlap: 100**

Each section already answers one kind of question on its own. So the chunks follow the headers instead of a character count. Measured across all 14 guides, the sections run 23 to 711 characters with a median around 285, so no section needs to be cut to fit.

The 150-character minimum handles the shortest pieces after splitting, which are the headers. On their own they are too short to answer anything, so they are merged into the section that follows.

Overlap exists so a thought cut in half by a fixed window still appears whole in one chunk. 

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

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
