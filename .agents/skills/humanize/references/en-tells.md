# English AI Tells: detection & rewriting reference

A field guide to the patterns that make English prose read as LLM-generated, with a fix for each.
Sources: Wikipedia's *Signs of AI writing* (WikiProject AI Cleanup), the open-source humanizer skills
(blader, jooray, avectats), and frequency studies of LLM vocabulary (Kobak et al. 2025, Juzek & Ward
2025, Liang et al. 2024, Reinhart et al. 2025). Each entry is: **what it is → how to fix it → example.**

**Contents**
0. How to weigh tells (read first)
A. Structural staging (strongest)
B. Inflation and promotion
C. Vocabulary fingerprints (era-stamped)
D. Attribution, hedging, and knowledge-gap filler
E. Connectives and paragraph shape
F. Formatting and markup residue
G. Punctuation
H. Discourse-level habits (long pieces)
I. Chatbot residue
J. Human markers to preserve
K. Not tells (do not flag)

**Do NOT touch (never a tell):** proper nouns, product/model/org names; numbers, dates, units; text
inside quotation marks (direct quotes); titles; legal/statutory citations; math/chem/stat notation;
standard technical abbreviations (API, LLM, GPU, HTTP); a passage that *discusses* a phrase rather than
using it. Never add a fact, name, date, statistic, or source that isn't already in the text.

---

## 0. How to weigh tells

- **Strong alone** (`S1`): one sighting justifies an edit. These are almost all *structural*: a
  not-X-but-Y contrast, a one-line closer, a staged run-up, a phantom rebuttal, a stated takeaway,
  chatbot residue, forensic markup.
- **Needs company** (`S2`): edit when it recurs or sits next to other tells. Most vocabulary, a single
  em dash, a single "Additionally", a triad, passive voice, curly quotes.
- **Count a cluster once.** A bolded aside set off by an em dash inside a rule-of-three list is one
  strong tell, not three. Fix the sentence once.
- **Structure outlasts vocabulary.** Word habits rotate with each model release and are being absorbed
  into ordinary human speech. Paragraph shape, staging, and closers persist. When in doubt, spend your
  change budget on shape, not on swapping words.
- **Fix the shape, not the phrase.** Swapping "delve" for "explore" one word at a time leaves the
  sentence's machine shape intact and plants a new fingerprint. Restate the point plainly instead.

## A. Structural staging — S1

- **A-1 [S1] "Not (just) X, but (also) Y" and its relatives.** "It isn't merely a tool; it's a
  philosophy." Variants: reversed "Y rather than X"; split across sentences ("This does not mean X. It
  means Y."); staccato "Not X. Not Y. Not Z."; "Stop thinking X. Start thinking Y."; "X is dead. Y is
  the future."; the clipped negative tail ("..., no guessing."). All correct a belief nobody held.
  → Delete the rejected half and state the positive claim once. Keep a contrast only when the negative
  half corrects something the reader actually believes.
  *"It's not about the prompt. It's about the context."* → *"Context controls the output."*
- **A-2 [S1] One-line closers and dramatic fragments.** "That is the real win." "Read that again." "Let
  that sink in." "Every. Single. Day." Rows of fragments ("No aesthetic prior. No nostalgia.").
  → Cut a closer that repeats the paragraph. Merge fragment rows into a sentence with a specific claim.
  End on the last concrete fact instead.
- **A-3 [S1] Sayings that sound deep.** "the real question is", "at its core", "what really matters",
  "the heart of the matter", "X is the Y of Z", "X is not a tool but a mirror", "the language/currency/
  architecture of", "This advantage has a date / a shelf life".
  → Replace with the plain observation, or cut.
  *"Symmetry is the language of trust."* → *"Symmetric layouts feel more predictable to users."*
- **A-4 [S1] Staged run-up.** "Let's dive in", "Let's break this down", "Here's what you need to know",
  "Here's the thing", "The thing is", "Honestly?", "Look,", "Real talk", "Plot twist:", "What if I told
  you", self-answered "Question? Answer." pairs, and the colon-reveal ("The best part: it learns.").
  → Delete the run-up; open on the content. "Honestly" mid-sentence is ordinary; the standalone opener
  is the tell.
- **A-5 [S1] Arguing with no one.** "This isn't about", "I'm not saying", "To be clear", "Don't get me
  wrong", "Some might say... but", "A tempting approach would be", "You might think... but".
  → Cut the phantom objection; keep the claim. Usually a leftover from an earlier draft.
- **A-6 [S1] Performed rigor and candor.** "It's worth being precise here", "to be fair", "in fairness",
  "the honest answer is", "one caveat up front", "worth flagging", "it bears repeating", "in one
  specific way", "there is a precise reason for this".
  → Delete the announcement and keep what follows. Never swap one certificate of honesty for a
  better-worded one.
- **A-7 [S2] Rule of three.** "fast, reliable, and scalable"; three parallel examples; three bolded
  categories per section; tricolon after tricolon.
  → Keep three only when all three carry distinct information. Otherwise cut to what matters, or let
  the list be the length its content is, including lists of two.
- **A-8 [S2] Hedged-enumeration openers.** "There are several factors to consider", "There are a few
  ways to", "It depends on a number of factors", "Generally speaking".
  → Give the specific answer first.
- **A-9 [S2] False agency.** "the data tells us", "the numbers reveal", "the evidence demands", "the
  market rewards", "history teaches us".
  → Say what the data shows. Do not invent an actor to fill the slot.
- **A-10 [S2] Repeated sentence openings.** Three sentences in a row starting with the same subject or
  frame ("She noted... She noted... She filed...").
  → Merge or vary. Do not ban the repeated word itself; deliberate anaphora ("She came. She saw.") is
  human.

## B. Inflation and promotion — S1

- **B-1 [S1] Significance and legacy inflation.** "stands/serves as a testament to", "plays a
  vital/pivotal/crucial role", "marks a significant milestone", "underscores/highlights the importance
  of", "reflects broader", "setting the stage for", "key turning point", "indelible mark", "deeply
  rooted", "evolving landscape".
  → Keep the fact, drop the significance claim.
  *"Established in 1989, marking a pivotal moment in regional statistics."* → *"Established in 1989."*
- **B-2 [S1] Puffery vocabulary.** "rich cultural heritage", "enduring legacy", "boasts", "renowned",
  "breathtaking", "nestled", "in the heart of", "vibrant", "profound", "diverse array", "commitment to",
  "natural beauty".
  → Plain fact or delete. Newer models are subtly positive rather than superlative; watch for warm
  adjectives with no supporting detail.
- **B-3 [S2] Hype adjectives.** "revolutionary", "groundbreaking", "cutting-edge", "game-changing",
  "unprecedented", "seamless", "robust", "powerful", "transformative", "holistic", "innovative",
  "ever-evolving".
  → Concrete detail from the source, or drop.
- **B-4 [S1] Canned notability and media coverage** (2025+ models). "independent coverage", "featured
  in Vogue, Wired, and other outlets", "trade publications", "profiled in", "active social media
  presence", "over N followers".
  → The tell is focus on the *sources* rather than what they said. Name the claim the source made, or
  cut.
- **B-5 [S1] "-ing" riders.** Trailing participial clauses that add evaluation, not information:
  "..., highlighting its importance.", "..., ensuring optimal results.", "..., reflecting the region's
  natural beauty.", "..., fostering collaboration.", "..., allowing for greater flexibility."
  LLMs use these 2 to 5 times more than people (Reinhart et al.).
  → Delete the tail, or make it a real clause with a subject, only if it states something true from
  the source.
- **B-6 [S2] Send-off endings.** "the future looks bright", "exciting times ahead", "a step in the right
  direction", "continues to thrive", "Despite these challenges, ...".
  → Cut the paragraph. End on the last concrete fact.
- **B-7 [S2] Ornamental intensifying adverbs.** "markedly", "strikingly", "significantly", "notably",
  "undeniably", "seamlessly", "meticulously" with no number behind them.
  → Delete, or keep the measured ones ("approximately", "modestly") when they carry information.

## C. Vocabulary fingerprints (era-stamped) — S2

Density is the tell, not any single word. A formal word outside these lists is not a tell by itself.
Word lists go stale: date-stamp your suspicion.

- **C-1 [S2] Still current (mid-2024 onward):** emphasizing, enhance, highlighting, showcasing,
  underscore (verb), pivotal, crucial, robust, vibrant, valuable, testament, tapestry (abstract),
  fostering, align with, bolstered, enduring, intricate, meticulous(ly), commendable, comprehensive,
  landscape (abstract), realm, interplay, leverage, harness, unlock, elevate, navigate (figurative),
  spearhead, garner(ed), myriad, plethora, cornerstone, beacon, palpable, camaraderie, surpassing,
  advancements, remarked, tragically, impacting, quietly, deep dive, gate/gated (figurative), utilize,
  streamline, empower, synergy, embark, unpack.
  → Swap for the plain word *and* check the sentence shape around it: *leverage* → *use*; *foster* →
  *build*; *showcasing* → *showing*; *remarked* → *said*; *surpassing* → *exceeding*; *a myriad of* →
  *many*; *navigate the landscape of* → *deal with*.
- **C-2 [S2] 2023 to mid-2024 markers (fading, still worth fixing):** delve, delves, delving, boasts,
  garner, intricacies, "In today's fast-paced world", "In today's digital age".
- **C-3 [S1] Phrase-level fingerprints** (GPTZero multipliers vs. human text): "play a significant role
  in shaping" (182x), "provide a valuable insight" (182x), "notable works include" (120x), "left an
  indelible mark" (111x), "today's fast-paced world" (107x), "aims to explore" (50x), "In recent
  years", "At the intersection of", "Now more than ever", "Here's the kicker", "Whether you're X or Y",
  "When it comes to", "I recently had the pleasure", "keen interest" (cover letters), "Bridging the gap
  between", "Navigate the complexities of", "Foster a culture of", "Move the needle".
  → Restate plainly. *"notable works include"* → *"best known for"*.
- **C-4 [S2] Copula avoidance.** "serves as", "stands as", "functions as", "operates as", "represents
  a", "refers to", "boasts/features/offers/maintains a"; elaborate forms "ventured into politics as a
  candidate", "began his career as".
  → Use *is / are / has / was*. *"Gallery 825 serves as the exhibition space."* → *"Gallery 825 is the
  exhibition space."*
- **C-5 [S2] Vague association.** "associated with", "in connection with", "connected to", "linked to",
  "tied to" where a real relationship exists.
  → Name the relationship the source gives ("was the CEO"). If the source doesn't say, leave it vague;
  don't invent.
- **C-6 [S2] Nominalization density.** Noun-heavy sentences ("the implementation of the optimization of
  the process") run 1.5 to 2x human rates.
  → Restore the verb: *"the implementation of"* → *"implementing"*.
- **C-7 [S2] Predicate hyphens.** "the report is high-quality", "the process is well-defined".
  → Drop the hyphen in predicate position; keep it attributive ("a high-quality report").

## D. Attribution, hedging, and knowledge-gap filler — S1~S2

- **D-1 [S1] Unnamed authorities.** "studies show", "experts say", "research suggests", "it is widely
  believed", "many argue", "critics contend", "industry reports", "observers have cited"; also
  exaggerating quantity ("scholars" when one is cited).
  → Keep a name if the source gives one. Otherwise state the claim plainly or flag that a source is
  needed. **Never** invent a source; a fabricated "2019 survey" is a defect even when it sounds more
  human. A missing citation alone is not a tell; most writing is unsourced.
- **D-2 [S2] Stacked hedges.** "may potentially", "could possibly", "some might say".
  → One hedge where uncertainty is real, calibrated to the evidence: direct statement for established
  facts, "may" for observational claims. Ordinary hedges ("perhaps", "tends to", "I think") are human
  habits, not tells. Watch the opposite failure too: flat assertions about uncertain things.
- **D-3 [S1] Knowledge-gap speculation.** "While specific details are limited", "not widely
  documented", "based on available information", "maintains a low profile", "likely grew up in",
  "it is believed that", "as of my last update".
  → Delete the disclaimer and the guess. If the text doesn't know, it doesn't say.
- **D-4 [S2] Balanced both-sides framing.** "On one hand... on the other", "While it's true that... it's
  also...", "benefits and challenges" as a reflex, "While X is important, Y is even more crucial".
  → Commit to the claim the text makes; keep balance only where the source genuinely balances.

## E. Connectives and paragraph shape — S1~S2

- **E-1 [S1] Connective pile-up.** Sentence-initial "Moreover,", "Furthermore,", "Additionally,", "In
  addition,", "Notably,", "Importantly,", "That said,", "That being said,", "Ultimately,", "Moving
  forward,". Rule of thumb: more than one connective opener in a paragraph, or the same one twice in a
  section.
  → Remove most and let sentence order carry the logic. Never bare-delete a transition that carries a
  real logical link; restructure or use a plainer one. Transitions in isolation are not a tell;
  "Although", "Thus", "Nevertheless", "Specifically" are fine.
- **E-2 [S2] Wrap-up paragraphs.** "In conclusion", "In summary", "Overall", "Ultimately" restating the
  body; "Conclusion" or "Future Outlook" sections in short pieces.
  → Delete, or replace with a last thought that adds something.
- **E-3 [S2] Formulaic paragraph shape.** Topic sentence, three supports, significance closer, every
  time; five-paragraph-essay shape on a 100-word answer.
  → Vary openings (a detail, a number, a plain claim). Drop the closers. Apply the **reshuffle test**:
  if swapping two paragraphs breaks nothing, they are interchangeable blocks; merge or reorder so each
  adds something the previous one didn't.
- **E-4 [S2] Treadmill.** Consecutive paragraphs that restate the same point louder.
  → Ask what each paragraph adds. Where the answer is "nothing, but louder", merge.
- **E-5 [S2] Heading restated in the first sentence** ("## Performance / Speed matters.").
  → Cut the one-liner.
- **E-6 [S2] Uniform sentence length.** Median 14 to 22 words with almost no variance: the metronome.
  → Vary *without adding content*: split one long sentence into short plus medium; merge two short
  neighbours. Let one sentence be louder than the others. A run of clipped fragments is itself a tell.

## F. Formatting and markup residue — S1~S2

- **F-1 [S1] Bullets where prose belongs.** Every section a list; inline-header bullets ("**Speed:**
  it's fast.").
  → Convert decorative bullets to prose. Keep lists only where enumeration is the point.
- **F-2 [S2] Bold and heading abuse.** Key words bolded in running text; Title Case headings; a top
  heading repeating the document title; headings containing only sub-headings; skipped heading
  levels; `---` between every section; "Awards and recognition" / "X and Y" section titles.
  → Remove decorative bold; sentence-case headings; delete the title heading and the dividers.
- **F-3 [S2] Decoration.** Emoji as bullets or heading ornaments (✅ runs 167x human rate), arrows (→),
  "≈", box-drawing characters, small tables for what should be a sentence.
  → Delete in anything that isn't a chat message.
- **F-4 [S1] Forensic residue.** `oaicite`, `contentReference`, `turn0search0`, `[cite: 1]`,
  `grok_card`, lenticular brackets 【】, `utm_source=chatgpt.com`, `[Your Name]`, `[Specific Topic]`,
  zero-width characters, mixed-script homoglyphs, stray `**`.
  → Strip to plain text. Normalize quotes to the document's own convention (curly quotes alone prove
  nothing; Word and macOS produce them).
- **F-5 [S2] Reasoning-chain leakage.** "Let me think", "Let's work through this", "Step 1:", "Now that
  we have established", "Breaking this down".
  → Delete; keep the result.

## G. Punctuation — S1~S2

- **G-1 [S1 when clustered, S2 alone] Em dashes.** Several per page, usually spaced, standing in for
  commas, colons, parentheses. Newer models suppress them, so their absence proves nothing, but a
  cluster still reads as machine cadence.
  → Convert most to commas, periods, colons, or parentheses. Keep one an author clearly placed for a
  beat. **A writing sample overrides this rule:** if the author uses dashes, keep them at about the
  same rate.
- **G-2 [S2] Colon-reveal.** "The real cost isn't the subscription: it's the hours."
  → Two plain sentences, or one direct claim.

## H. Discourse-level habits (long pieces, essays, emails) — S2

These come from narrative-level detection research (StoryScope, 2026) and matter most in pieces over a
few paragraphs. Fix by subtraction first. Skip this section for procedures, legal text, API references,
and templated reports, where explicitness and tidy closure are the specification.

- **H-1 The stated takeaway.** The last sentence tells the reader what the paragraph meant ("Which is
  really what good onboarding is about."). → Delete it. End on the last concrete thing.
- **H-2 The epilogue.** The piece ends, then adds a warm wrap-up paragraph. → Cut the last paragraph
  and read again.
- **H-3 The atmospheric opener.** "It was 7am and the office was still dark." → Open on the content.
- **H-4 Front-loaded shared context.** "As you know, we've been running the Q3 campaign since June..."
  → Assume shared history. Reference it, don't reconstruct it.
- **H-5 The body report.** Emotion as physical sensation ("my stomach dropped", "something tightened in
  my chest", "the room went quiet"). People write "I was annoyed." → Name the feeling in plain words,
  only where the register allows emotion at all.
- **H-6 The tidy resolution.** Every loose end tied, the writer always in control. → Don't manufacture
  closure. One open item or one stated doubt is allowed; don't add one that wasn't there.
- **H-7 Flat emphasis.** Nothing rises above anything else; every paragraph the same weight. → Let
  section depth vary. Some points get one sentence, some six.
- **H-8 Batch convergence.** When editing several pieces at once, diagnose the set: if all five open
  with a metric, the metric opener is the new "We're excited to share". → Rotate openers (the number,
  the ask, the correction, the blunt fact, the question, the thing that broke).

## I. Chatbot residue — S1

- **I-1 [S1] Talk aimed at a user.** "Great question!", "Certainly!", "Of course!", "You're absolutely
  right!", "Sure! Here's...", "I hope this helps!", "Let me know if you'd like...", "Would you like a
  more detailed breakdown?", "happy to", "feel free to".
  → Delete. Salutations and sign-offs on an actual letter predate chatbots; leave those.
- **I-2 [S1] Manufactured aphorism endings.** A quotable one-liner tacked on to feel profound ("Because
  in the end, data is just people.").
  → Cut unless the author clearly wrote it and it earns its place.
- **I-3 [S1] Sycophancy and servility.** "What a thoughtful question", "I completely understand your
  concern", "I am committed to", "Could you kindly".
  → Delete.

## J. Human markers to preserve

Empirically more common in human writing (Wikipedia's human-writing list, Reinhart et al.). Stripping
these is not de-AI-ing; it removes evidence a person wrote it.

- Simple *is / has / there is / it has a* constructions.
- Plain verbs: *wrote* not *authored*, *used* not *utilized*, *tried* not *attempted*, *died* not *passed
  away*, *moved* not *relocated*.
- Superlatives and definite claims: *one of the best*, *the only*, *the first*.
- Everyday hedges and intensifiers: *very*, *perhaps*, *tends to*, *I think*, *kind of*.
- Slightly wordy idioms: *in order to*, *the fact that*, *as a result of*, *all of the*, *a part of*.
- **Agentless passive voice.** LLMs use it at about half the human rate. "Convert to active" is not a
  humanizing edit; leave passives alone unless a sentence is genuinely unclear.
- A specific, odd detail; a dated or era-bound reference; mixed feelings left unresolved; a genuine
  aside or self-correction; a sentence starting with *And* or *But*; one short emphatic sentence.
- Repetition of a plain word instead of synonym cycling (older models rotated synonyms; humans repeat).
- British vs. American spelling as found. Don't normalize.

## K. Not tells (do not flag)

- Perfect grammar. Mixed casual and formal register. "Bland" or "robotic" prose in general. Formal or
  academic vocabulary in general: the correlation is with *specific* words, not with formality. Don't
  flatten *ostensibly* or *constituent*.
- Transition words in isolation. One em dash. One "Additionally". Curly quotes.
- Unsourced content. Markdown by itself (developers, Obsidian, Reddit).
- A watched phrase inside a quotation, a title, a proper name, or a passage about the phrase.
- Text the author says predates November 2022.
- Real alternatives in a design doc or tutorial (that is not "arguing with no one").
- Useful limits and disclaimers that answer a question the reader actually has.

---

## Self-check (after rewriting)

1. Numbers, dates, names, quotes: identical to source.
2. Nothing invented: no new fact, source, specific, or opinion the writer didn't express.
3. Nothing dropped: every supported claim survives. Triad merges, hedge cuts, and bold-list-to-prose
   conversions drop claims most often; recheck those spots.
4. Register and genre unchanged; human markers from section J preserved; British/American as found.
5. No cliché added while removing others. No new uniform register imposed (every sentence short,
   every opener a metric).
6. The five survivors hunted: a not-X-but-Y contrast, a one-line closer, a dash cluster, a decorative
   triad, a bold label.
7. Change stayed roughly 10 to 30% (up to about 40% for tell-dense text). Past half: revert and redo.

## Internal self-assessment (never shown to the user)

Use this only to decide whether to offer a stronger second pass. Do NOT print letters or codes in the
change report; translate the judgment into plain words ("reads clean now" / "still a little AI-ish").

- Clean: no strong tells remain, ≤2 minor, change 10 to 25%, all self-checks pass.
- Mostly clean: no strong tells, ≤4 minor, most self-checks pass.
- Needs another pass: 1 to 2 strong tells remain or several self-checks fail. Offer a stronger redo.
- Stop and flag: 3+ strong tells remain or change >50%. Likely meaning drift; revert and redo, or tell
  the user it needs a human look.
