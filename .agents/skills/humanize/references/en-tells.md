# English AI Tells — detection & rewriting reference

A field guide to the patterns that make English prose read as LLM-generated, with a fix for each. The
taxonomy follows the patterns catalogued by Wikipedia's *Signs of AI Writing* (WikiProject AI Cleanup)
and the conventions that community and downstream tools have converged on. Each entry is: **what it is →
how to fix it → example.**

**Severity:** `S1` = strong tell, fix on sight. `S2` = fix when it recurs or clusters.

**Do NOT touch (never a tell):** proper nouns, product/model/org names; numbers, dates, units; text
inside quotation marks (direct quotes); legal/statutory citations; math/chem/stat notation; standard
technical abbreviations (API, LLM, GPU, HTTP). Never add a fact, name, date, statistic, or source that
isn't already in the text — specificity comes from the source, not the rewrite.

---

## A. Promotional tone & inflated significance — S1

The single most consistent AI tell: text that reads like marketing copy, inflating importance where a
human would just state the fact.

- **A-1 [S1] Puffery vocabulary.** "rich cultural heritage", "enduring legacy", "stands as a testament
  to", "plays a vital/pivotal/crucial role", "boasts", "renowned", "breathtaking", "nestled".
  → Delete the inflation or replace with the plain fact.
  *"The museum stands as a testament to the city's rich cultural heritage."* → *"The museum holds the
  city's main folk-art collection."*
- **A-2 [S1] Significance editorializing.** "It's important to note that…", "It's worth noting…", "This
  underscores/highlights the importance of…", "This marks a significant milestone."
  → Cut the frame; state the point directly, or delete if it added nothing.
  *"It's important to note that the results were mixed."* → *"The results were mixed."*
- **A-3 [S2] Hype adjectives.** "revolutionary", "groundbreaking", "cutting-edge", "game-changing",
  "unprecedented", "seamless", "robust", "powerful", "vibrant", "ever-evolving".
  → Replace with a concrete detail, or drop. Keep only if the source backs the claim with specifics.

## B. Vocabulary fingerprints — S1

Words LLMs reach for far more often than people do. Not banned for humans, but their density is the tell.

- **B-1 [S1] Overused verbs/nouns.** delve, tapestry, realm, landscape, testament, showcase, underscore,
  leverage, harness, foster, unlock, elevate, navigate (figurative), spearhead, garner, myriad,
  plethora, beacon, testament, cornerstone, interplay.
  → Swap for the plain word: *delve into* → *look at / dig into*; *leverage* → *use*; *foster* →
  *encourage / build*; *a myriad of* → *many*; *navigate the landscape of* → *deal with*.
- **B-2 [S2] "-ing" participial padding.** Trailing clauses that add nothing: "…, ensuring optimal
  results.", "…, allowing for greater flexibility.", "…, highlighting its importance.", "…, making it a
  popular choice."
  → Delete the tail, or make it a real clause with a subject. *"…cutting costs, ensuring long-term
  savings."* → *"…cutting costs, which saves money over time."* (only if true) or just *"…cutting costs."*

## C. Signature constructions — S1

- **C-1 [S1] "Not (just) X, but (also) Y."** "It's not just about the music, it's about the movement."
  "This isn't merely a tool; it's a philosophy." AI loves correcting a misconception no one held.
  → Rewrite as a direct statement. *"It's not just a database, it's a way of thinking about data."* →
  *"The tool changes how you think about your data, not only where you store it."* — or simpler, assert
  the real point once.
- **C-2 [S1] Rule of three.** Three parallel items/adjectives used as a rhetorical reflex: "fast,
  reliable, and scalable"; "the good, the bad, and the ugly"; tricolon after tricolon.
  → Keep the list only if all three items carry real, distinct information. Otherwise cut to the ones
  that matter, or convert to prose. Break the parallelism when it's decorative.
- **C-3 [S2] False range / "from X to Y".** "Applications range from healthcare to finance to
  education." Sounds specific, says "lots of things."
  → Replace with the actual set if known, or a plain quantifier. *"…used across many industries."* or
  name the real ones from the source.

## D. Vague attribution & weasel sourcing — S1

- **D-1 [S1] Unnamed authorities.** "studies show", "experts say", "research suggests", "it is widely
  believed", "many argue", "critics contend" — with no citation.
  → If the source names who, keep the name. If it doesn't, either drop the claim's authority framing and
  state it plainly, or flag that a source is needed. Do **not** invent a source.
- **D-2 [S2] Hedged non-claims.** "may potentially", "could possibly", "some might say", stacked hedges.
  → Keep one hedge at most where genuine uncertainty exists; otherwise assert.

## E. Transitions & connective overuse — S1

- **E-1 [S1] Generic transition openers.** Sentences/paragraphs starting with "Moreover,",
  "Furthermore,", "Additionally,", "In addition,", "Notably,", "Importantly,", "That said,".
  → Cut most of them. Good prose flows without a signpost on every sentence. Keep one only where it
  genuinely marks a turn.
- **E-2 [S2] "In conclusion / In summary / Overall / Ultimately" wrap-ups** that just restate what was
  already said.
  → Delete the summary paragraph, or replace with an actual last thought that adds something.

## F. Structure & formatting slop — S1~S2

- **F-1 [S1] Bullet-point overuse.** Prose chopped into bullets where sentences belong, or every section
  a list. In essays/columns/reports especially.
  → Convert decorative bullets to flowing prose. Keep lists only where enumeration is the point.
- **F-2 [S2] Inline-header / bold abuse.** Bold lead-in on every list item ("**Speed:** it's fast."),
  key words bolded in running text, title-case everywhere.
  → Remove decorative bold; keep emphasis rare and meaningful. Sentence-case normal headings.
- **F-3 [S2] Formulaic paragraph shape.** Every paragraph opens with a topic sentence and closes with a
  significance sentence.
  → Vary openings — start some paragraphs with a detail, a number, or a plain claim. Drop the closers.
- **F-4 [S2] Section summaries mirroring headings** and "Here's what we'll cover" scaffolding.
  → Cut the meta-scaffolding; let content stand.

## G. Punctuation tells — S1

- **G-1 [S1] Em-dash overuse.** The single most reliable punctuation signal. Em dashes (—) standing in
  for commas, colons, or parentheses, several per page.
  → Convert most to commas, periods, colons, or parentheses. A rare em dash for a genuine sharp aside is
  fine; the machine-gun cadence is the tell. **Do not** delete an em dash the author clearly placed for
  a real beat — but default to cutting when they cluster.
- **G-2 [S2] Curly-quote / markdown artifacts** left from generation (stray "**", smart quotes mixed
  with straight, escaped characters), and title-case headline everything.
  → Normalize to the document's own convention.

## H. Rhythm & sentence uniformity — S2

- **H-1 [S2] Uniform sentence length.** Every sentence 15–25 words, no short punch, no long build.
  → Introduce variation *without adding content*: split a long sentence into a short one plus a medium
  one; merge two short adjacent sentences into one longer line. Rhythm, not new words.
- **H-2 [S2] Balanced "on one hand… on the other" / "while it's true that… it's also…"** RLHF-style
  both-sides framing on everything.
  → Commit to the claim the text actually makes; keep balance only where the source genuinely balances.

## I. Chatbot residue — S1

- **I-1 [S1] Conversational openers/closers aimed at a user.** "Great question!", "Sure! Here's…",
  "I hope this helps!", "Let me know if you'd like…", "In today's fast-paced world…".
  → Delete entirely. These are chat framing, not part of the text.
- **I-2 [S1] Manufactured punchline / aphorism endings.** A neat, quotable one-liner tacked on to feel
  profound ("Because in the end, data is just people.").
  → Cut unless the author clearly wrote it and it earns its place.

---

## Self-check (after rewriting)

1. Numbers, dates, names, quotes — identical to source.
2. Nothing invented: no new fact, source, or specificity.
3. Register and genre unchanged; living voice preserved.
4. No cliché added while removing others.
5. Top diagnosed tells actually gone.
6. Change stayed ~10–30%. If it ballooned past ~50%, revert and redo conservatively.

## Internal self-assessment (never shown to the user)

Use this only to decide whether to offer a stronger second pass. Do NOT print letters or codes in the
change report — translate the judgment into plain words ("reads clean now" / "still a little AI-ish").

- Clean — no strong tells remain, ≤2 minor, change 10–25%, all self-checks pass.
- Mostly clean — no strong tells, ≤4 minor, 5/6 self-checks pass.
- Needs another pass — 1–2 strong tells remain or several self-checks fail → offer a stronger redo.
- Stop and flag — 3+ strong tells remain or change >50% → likely meaning drift; revert and redo, or tell
  the user it needs a human look.
