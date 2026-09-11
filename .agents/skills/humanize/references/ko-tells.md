# Korean AI Tells — detection & rewriting reference

A field guide to the patterns that make Korean prose read as LLM-generated, with a fix for each.
The taxonomy borrows the ten categories used by the open-source Korean humanizer
(epoko77-ai/im-not-ai), condensed and reworded for a single editing pass. Each entry is:
**what it is → how to fix it → example.** Korean particles, endings, and sample sentences are kept
in Korean because they are the thing being detected; the surrounding explanation is English.

**Severity:** `S1` = strong tell, fix on sight. `S2` = fix when it recurs or clusters.

**Do NOT touch (never a tell):** proper nouns, product/model/org names; numbers, dates, units; text
inside double quotation marks (direct quotes); statutory text; math/chem/stat notation; standard
English technical abbreviations (API, LLM, GPU, MCP). Never add a fact, name, number, or source that
isn't already in the text. Do not force-translate standard loanwords (prompt → "지시문" ✗,
token → "징표" ✗).

> **Register warning.** The examples below use the plain 한다체 form for brevity. The output must
> **always follow the source text's register** (합쇼체 / 해요체 / 한다체). Never copy the register of an
> example.

---

## A. Translation-ese (번역투) — S1~S2

Traces of English sentence structure carried into Korean. The most common and strongest Korean tell.

- **A-1 [S1] Overused "~에 대해(서)" ("about/regarding").** → Use the object particle directly.
  ("X에 대해 논의한다" → "X를 논의한다")
- **A-2 [S2] "~를 통해/통하여" ("through") three or more times in a paragraph.** → Spread some of them
  across "~로", "~해서", "~함으로써"; keep one or two.
- **A-3 [S1] "~에 있어(서)" ("in terms of").** → "~에서", "~를 볼 때". ("교육에 있어서" → "교육에서")
- **A-4 [S2] Repeated "~라는 점에서" ("in that").** → "~서", "~라는 이유로", "~이기 때문에".
- **A-5 [S2] "~와 관련하여/관련된" ("in relation to").** → "~에", "~의", "~를 두고".
- **A-6 [S2] Overused "~에 기반하여/바탕으로" ("based on").** → "~로", "~를 근거로".
- **A-7 [S1] Literal have/make/take/give + noun ("가지고 있다" and similar).** → Restore the adjective
  or verb. ("강한 경쟁력을 가지고 있다" → "경쟁력이 강하다")
- **A-8 [S1] Double passive "~되어진다/~지게 된다".** → Active voice or a single passive.
  ("판단되어진다" → "판단된다")
- **A-9 [S2] Agent-marked passive "~에 의해" ("by").** → Make the agent the subject.
  ("AI에 의해 생성된" → "AI가 만든")
- **A-10 [S2] Overused "~할 수 있다" ("can").** → State plain facts as assertions.
  ("높일 수 있다" → "높인다")
- **A-11 [S2] Overused purpose clause "~을 위해" ("in order to").** → "~려고", "~도록", "~위한".
- **A-15 [S2] Abstract subject + all-purpose verb (보여준다/제공한다/가져온다).** → Restore a concrete
  subject. Literal cognition verbs (suggest/show/indicate → "시사한다/보여준다") become "~에 따르면 ~이다".
- **A-16 [S1] "그/그녀/그것/그들" three or more times in a paragraph (literal English pronouns).** → Drop
  more than half (zero anaphora) or use a noun phrase.
- **A-18 [S2] Long pre-nominal modifier of three or more phrases (긴 관형절).** → Split the sentence or
  use a trailing appositive clause. ("정부가 발표한 새로운 규제를 담은 법안" → "법안이 나왔는데, 정부가
  발표한 새 규제를 담았다")
- **A-19 [S2] Stacked particles "~에서의/~으로의/~에의/~으로부터의".** → Unpack into a clause or phrase.

## B. Excess English glosses and jargon (영어 병기·용어 과다) — S2

- **B-1 [S2] Korean + parenthesised English on every mention ("~(Sovereign AI)" style).** → Gloss on
  first mention only; Korean alone afterwards.
- **B-2 [S2] Unexplained marketing buzzwords (seamless, robust, leverage).** → Paraphrase the marketing
  words in Korean; keep standard technical terms (API, prompt, token) in the original. No mechanical
  literal translation.

## C. Structure and formatting (구조·서식) — S1~S2

- **C-2 [S2] Three or more consecutive bullets in a column or report.** → Merge into prose; keep a list
  only where enumeration carries meaning.
- **C-5 [S1] Emoji overuse (list markers, headings, emphasis).** → Delete all of them in column or report
  genres.
- **C-7 [S2] The three-step formula "먼저 – 반면 – 결국" ("first – whereas – ultimately").** → Cut to one
  or two connectives or fold into the body.
- **C-8 [S1] Antithesis repeated three or more times ("A인가, B인가" / "A가 아니라 B").** → Keep one; turn
  the rest into plain declaratives.
- **C-9 [S2] Numbered inline lists "1) 2) 3)".** → Fold into the body or vary with "우선~", "다음으로~".
- **C-10 [S1] Repeated colon-subtitle headings "X: Y".** → Compress to a single noun phrase. Preserve real
  section titles in academic or report formats.
- **C-11 [S1] Comma right after a connective ending (-고/-며/-지만/-면서/-아서/-어서).** → Remove the
  comma (strong tell).

## D. Signature AI phrases (AI 특유 관용구) — S1

- **D-1 [S1] Wrap-up lexicon "결론적으로/따라서/이를 통해/그러므로/요약하면" ("in conclusion / therefore /
  through this / thus / to summarise").** → If more than three, keep one or two.
- **D-2 [S1] Inflated significance "시사하는 바가 크다/주목할 만하다/매우 중요하다" ("has great implications
  / is noteworthy / is very important").** → Delete, or replace with the concrete conclusion.
- **D-3 [S1] List lead-ins "크게 세 가지로 나눌 수 있다/다음과 같다" ("can be divided into three / is as
  follows").** → Delete the lead-in and start with the content.
- **D-4 [S1] Repeated hype vocabulary (혁신적/획기적/압도적/파격적/전례 없는).** → Replace with concrete
  numbers or facts.
- **D-5 [S2] Personified abstract subjects ("기술이 묻는다", "시대가 부른다").** → Use a person or
  organisation as subject.
- **D-6 [S2] Closing formula "~할 때입니다/~시점입니다/~할 순간입니다" ("now is the time to").** → A
  concrete verb assertion; at most once per document.
- **D-7 [S2] Transformation formula "X에서 Y로 / X을 넘어 Y로" ("from X to Y / beyond X to Y").** → Direct
  assertion; at most once per document.

## E. Uniform rhythm and sentence length (리듬·문장 길이 균일성) — S2

- **E-1 [S2] Uniform sentence length with no long/short contrast.** → Without adding content, mix in one
  short sentence and one longer sentence made by joining neighbours.
- **E-2 [S2] The same sentence ending four or more times in a row / automatic "~고 있다" (progressive).**
  → Vary the endings; reduce "~고 있다" to simple tense where possible. ("읽고 있다" → "읽는다")

## F. Excess nominalisation and modifiers (명사화·수식 과다) — S2

- **F-4 [S2] Stacked Sino-Korean nominalisation (-성/-적/-화) and literal English -tion/-ment.** → Restore
  the verb or adjective root. ("정책의 시행" → "정책을 시행하는 일", or in context "정책 시행")
- **F-5 [S2] "~적 N" abstract chains ("전략적 함의", "실천적 기반") three or more times.** → Noun + noun or a
  paraphrase. ("전략적 함의" → "전략 함의")

## G. Excess hedging (과도한 완곡) — S2

- **G-1 [S2] Overused conjectural endings "~로 보인다/~로 판단된다/~라고 여겨진다/~인 듯하다" ("appears /
  is judged / is considered / seems").** → Assert where assertion is possible.
- **G-2 [S2] Double or triple hedges "~할 가능성이 있을 수 있다".** → Keep one hedge.
- **G-3 [S2] Balance lexicon "양쪽 모두/장점도 있지만/신중하게/균형" four or more times.** → Take a side,
  compare concretely, or make it conditional.

## H. Connective overuse (접속사 남발) — S2

- **H-1 [S2] Sentence-initial connectives "또한/따라서/즉/나아가/게다가/더욱이" five or more times.** →
  Remove most; let the sentence flow carry the logic.
- **H-3 [S2] Meta openers "이는 ~/이 점에서/이 관점에서" ("this ~ / in this respect / from this
  perspective") three or more times.** → Fold into the body or delete.
- **H-4 [S2] Overused "즉" ("that is").** → Vary with "곧", "말하자면" or omit; at most twice per document.

## I. Excess bound nouns (형식명사·의존명사 과다) — S1~S2

- **I-1 [S2] "~한 것이다/~일 것이다" three or more times in a row.** → Turn some into the plain declarative
  "~다".
- **I-2 [S1] Bound-noun emphasis "주목할 점은 ~라는 점이다" ("the notable point is that").** → Direct
  statement "X는 ~다".
- **I-3 [S2] Closers "~다는 것이다/~다는 뜻이다" ("which means that").** → Direct ending "~다"; at most two
  combined.
- **I-4 [S2] Prescriptive closers "~해야 한다/~할 필요가 있다" ("must / needs to") five or more times.** →
  Concrete verb assertion, explicit subject, or a conditional.

## J. Visual decoration overuse (시각 장식 남용) — S2~S3

- **J-1 [S2] Bold on the key word of every sentence.** → In columns and reports, remove almost all body
  bold.
- **J-2 [S2] Scare quotes five or more times.** → Keep real quotations only; plain words elsewhere.
- **J-3 [S2] Dash (—) asides in every sentence.** → Break into commas, parentheses, or separate sentences.
  Preserve dashes that were in the source and living spoken touches (short exclamations, rhetorical
  questions).

---

## Prime directives (all categories)

1. **Meaning is inviolable.** Facts, numbers, proper nouns, quotations, and causal links survive
   character-for-character. Vague stays vague; no invented specificity.
2. **Removal-only.** Only subtract AI tells. Never plant a stock phrase that was not in the source
   ("기록적인 성과를 거두었다" and the like).
3. **Preserve register — both directions.** Formal stays formal, colloquial stays colloquial. Do not raise
   formality ('-했-' → '-하였-' is forbidden). Preserve living colloquial endings such as '~인데요/~거든요';
   they are evidence a person wrote it.
4. **No genre drift.** A column does not become an essay; an essay does not become literature.
5. **Locality.** Surgically edit only the spans carrying tells. Do not rewrite sound sentences wholesale.
6. **Natural over perfect.** Do not polish into literary prose. Aim for the median rhythm of an everyday
   Korean writer.

## Self-check (after rewriting)

1. Are proper nouns, numbers, dates, and quotations identical to the source, character for character?
2. Did any fact, source, or specificity appear that was not in the source?
3. Are register and genre unchanged? Were living colloquial markers preserved?
4. Was a new stock phrase planted while removing AI tells?
5. Are the dominant patterns you diagnosed actually gone (not merely weakened)?
6. Is the change rate roughly 10–30%? Above 50%: roll back and redo conservatively.

## Internal grading (never shown to the user)

Use only to decide whether to recommend a stronger second pass. Do not print grade letters or codes in
the report; translate them into plain words such as "이제 자연스럽다" ("reads naturally now") or "아직 조금
AI 티가 남았다" ("still a little AI-flavoured").

- Clean — 0 strong tells, ≤2 weak tells, 10–25% change, all 6 self-check items pass.
- Mostly clean — 0 strong tells, ≤4 weak tells, ≥5 self-check items pass.
- Needs another pass — 1–2 strong tells or ≤4 self-check items pass → offer a stronger rewrite.
- Stop and disclose — 3+ strong tells or >50% change → roll back and redo, or tell the user a human
  review is needed.
