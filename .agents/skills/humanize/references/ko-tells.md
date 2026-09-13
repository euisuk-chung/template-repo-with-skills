# Korean AI Tells: detection & rewriting reference

A field guide to the patterns that make Korean prose read as LLM-generated, with a fix for each.
The taxonomy and most thresholds come from the open-source Korean humanizer epoko77-ai/im-not-ai
(v2.7 taxonomy, validated against 60 pre-2022 human documents and 180 AI documents across three
models), plus KatFishNet (Park et al., ACL 2025), 국립국어원 translationese papers (김순영·김한식 2012),
devswha/patina, and Korean writing-community pattern lists. Each entry is: **what it is → how to fix
it → example.** Korean particles, endings, and samples stay in Korean because they are the thing being
detected; the explanation is English.

**Contents**
0. How to weigh tells, and what the data changed (read first)
A. 번역투 (translation-ese)
B. 영어 병기·용어 (English glosses and jargon)
C. 구조 (structure), led by antithesis chains
D. AI 관용구 (signature phrases)
E. 리듬 (rhythm and sentence length)
F. 명사화·수식 (nominalisation and modifiers)
G. 완곡·서법 (hedging and modality)
H. 접속사 (connectives)
I. 형식명사·당위 (bound nouns and obligation)
J. 시각 장식 (visual decoration)
K. 챗봇 잔재 (chatbot residue)
L. 사람 글의 표지 (human markers to preserve)
M. 표지가 아닌 것 (not tells)
N. 재작성 중 주입 금지 (things a rewrite tends to inject)

**Do NOT touch (never a tell):** proper nouns, product/model/org names; numbers, dates, units; quoted
speech with a speech verb (말했다·밝혔다·~에 따르면); statutory text; math/chem/stat notation; standard
English technical abbreviations (API, LLM, GPU, MCP); real section titles in academic or report formats
(Ⅱ., (3), 1.2 등). Never add a fact, name, number, date, or source that isn't already in the text. Do not
force-translate standard loanwords (prompt → "지시문" ✗, token → "표식" ✗, agent → "대리인" ✗).

> **Register warning.** Examples below use 한다체 for brevity. Output must **follow the source text's
> register** (합쇼체 / 해요체 / 한다체). Never copy the register of an example. Never upgrade '-했-' to
> '-하였-'. Never erase spoken endings (~인데요 / ~거든요 / ~한 겁니다).

---

## 0. How to weigh tells, and what the data changed

**Severity.** `S1` = one occurrence is near-certain AI; fix it. `S2` = one or two are fine; fix at
three or more in a paragraph, or when clustered with other tells. Count a cluster once.

**What the corpus measurements changed.** Several expressions that *look* like translation-ese are
used more by people than by models. Treat these as **preserve by default**, and act only on dense
repetition in one paragraph:

| Expression | Human vs AI (per 1,000 어절 or sentences) | Rule |
|---|---|---|
| ~에 대해(서) | humans 3× more | fix only at 3+ in a paragraph |
| ~를 통해 | humans 2× more | fix only at 3+ in a paragraph; keep one or two |
| ~을 위해 | humans more | fix only when dense |
| ~한 것이다 / ~일 것이다 | humans 2× more | fix only at 3+ consecutive |
| 이는 ~ / 이 점에서 | humans more (except one model) | preserve; straighten some at 3+ per paragraph |
| 또한 / 따라서 / 즉 (sentence-initial) | model-dependent; humans often more | fix only at 3+ in one paragraph, remove about half |
| ~할 수 있다 / ~로 보인다 (hedges) | not a discriminator | never convert to assertion; vary form at 4+ |
| 혁신적 / 획기적 (hype) | weak signal (1.3×) | fix because it concretises, not because it proves AI |

**The strong, model-independent signals** (fix these first):

| Pattern | Human vs AI | Where |
|---|---|---|
| Antithesis chains "A가 아니라 B" / "A인가, B인가" | 9 to 12× more in AI | C-1 |
| Paragraph *ending* on obligation "~해야 한다" | 7× | I-3 |
| Absence of any 100자+ sentence | 11× | E-1 |
| Comma right after a connective ending (-고, / -며,) | 4.8× | C-5 |
| Cleft "필요한 것은 / 문제는 / 핵심은 ~이다" | 10× | D-6 |
| Generic policy verbs 확대·강화·개선·마련 | 3.4× | F-4 |
| "~적 N" chains | 1.6× | F-3 |
| Sentence-initial "향후/앞으로" in the closing third | human 0 | D-9 |
| "단순한 X를 넘어 Y" | human 0 | A-11 |
| Sensory-predicate evaluation "진단은 서늘하다" | human 0 | D-12 |

**Structure over vocabulary.** The current-generation lexical tell is not hard Sino-Korean (제고·도모
show no gap) but convergence on *plain generic* words (다양한·핵심·효과적으로·구조·기준). Spend the
change budget on shape: chains, closers, paragraph-final obligation, rhythm.

**Never judge on one metric.** A 2020 human essay was flagged as AI on comma rate alone. A single
indicator is never evidence; look for clusters.

## A. 번역투 (translation-ese)

- **A-1 [S2, preserve by default] "~에 대해(서)".** → At 3+ in a paragraph, some become the object
  particle or topic. ("X에 대해 논의한다" → "X를 논의한다") Otherwise leave it; people write this.
- **A-2 [S2, preserve by default] "~를 통해/통하여".** → At 3+ in a paragraph, spread across "~로",
  "~해서", "~함으로써"; keep one or two.
- **A-3 [S1] "~에 있어(서)".** → "~에서", "~를 볼 때". ("교육에 있어서" → "교육에서")
- **A-4 [S2] "~라는 점에서" repeated.** → "~서", "~라는 이유로", "~이기 때문에".
- **A-5 [S2] "~와 관련하여 / 관련된", "~에 기반하여 / 바탕으로".** → "~에", "~의", "~로", "~를 보고".
- **A-6 [S1] Light-verb calques: have/make/take/give + noun.** → Restore the adjective or verb.
  ("강한 경쟁력을 가지고 있다" → "경쟁력이 강하다"; "회의를 가졌다" → "회의를 했다"; "결정을 내렸다" 는
  자연스러움, 두지 말 것 없음)
- **A-7 [S1] Double passive "~되어진다 / ~지게 된다".** → Active, or one passive. ("판단되어진다" →
  "판단된다")
- **A-8 [S2] Agent-marked passive "~에 의해"; automatic passives "만들어지다 / 이루어지다".** → Make
  the agent the subject. ("AI에 의해 생성된" → "AI가 만든"; "합의가 이루어졌다" → "합의했다")
- **A-9 [S2] Passive progressive "~되고 있다 / ~지고 있다" (is being ~ed).** Humans 1.4 vs AI 3.4;
  active "~하고 있다" shows no gap. → At 3+ in a paragraph, some become a trend assertion ("심화되고
  있다" → "심해졌다 / 심해지는 중이다"). Isolated uses stay.
- **A-10 [S1] Pronouns 그/그녀/그것/그들/이는 with no antecedent.** The tell is not frequency (humans
  use pronouns 2.5× more) but a pronoun whose referent is not in the previous two sentences (AI 6×
  more). → No candidate: restore the noun phrase (if unrecoverable, leave and flag). One candidate:
  drop the pronoun (zero anaphora). Two or more: repeat the noun. Never swap one pronoun for another;
  no deletion quota. ("존은 피곤했다. 그는 앉았다. 그는 한숨을 쉬었다." → "존은 피곤했다. 자리에 앉아 한숨을
  쉬었다.")
- **A-11 [S2, human 0] Range-raising "단순한 X를 넘어 Y".** → "X만이 아니라 Y다", or drop the 넘어
  phrase. ("개인의 취미를 넘어 도시 설계에 대한 관심으로" → "개인 취미만이 아니라 도시 설계에 대한 관심으로")
- **A-12 [S2] Evaluative predicate "~은/는 명확하다 / 분명하다" (It is clear that).** → Assert the
  proposition; carry confidence with the adverb 분명히 if needed. Keep when it closes a real argument.
  ("정책이 실패했다는 것은 명확하다" → "정책은 실패했다")
- **A-13 [S2] Groundwork formula "발판·토대·초석·교두보를 마련하다/놓다/다지다", "지평·활로를 열다".**
  → Say what it actually enables; if the text doesn't say, flatten only ("발판을 마련한다" → "여건이
  갖춰진다"). Never invent the path. Completed past facts ("딥러닝의 토대를 놓은 벤지오") stay.
- **A-14 [S2] "더 이상 ~ 아니다 / 않다" (no longer) as redefinition skeleton.** → "이제", or a verb of
  change ("~로 옮겨 갔다"). Do not flip the negative into a positive assertion.
- **A-15 [S2] Abstract subject + all-purpose verb (보여준다 / 제공한다 / 가져온다 / 시사한다).** →
  Concrete subject or direct statement. Causatives → "X 때문에 / 덕분에 / 로 인해"; suggest/show/indicate
  → "~에 따르면 ~이다". ("1997년 금융위기는 노동시장에 급격한 변화를 가져왔다" → "1997년 금융위기로 노동시장은
  급격히 바뀌었다")
- **A-16 [S2] Long pre-nominal modifier (3+ phrases) or triple-nested relative clause.** → Split, or
  trail an appositive clause. ("사고를 일으킨 화학물질을 생산한 회사에서 일했던 한 남자를 만났다" → "한 남자를
  만났는데, 그 남자는 …")
- **A-17 [S2] Stacked particles "~에서의 / ~으로의 / ~에의 / ~으로부터의".** Plain "~의" is excluded.
  → Unpack. ("긴장으로부터의 해방" → "긴장에서 벗어남"; "설문지에의 응답" → "설문 답변")
- **A-18 [S2] Noun stacking with particles dropped.** → Restore 의/가/를 and a verb. ("AI 기술 발전 속도
  가속화" → "AI 기술의 발전 속도가 빨라지고 있다") Do not batch-convert into "~해야 한다".
- **A-19 [S2] Sentence-initial "그리고" linking plain narrative (English *and*).** → Compress with
  -고/-며/-면서. ("그는 보고했다. 그리고 자리에 앉았다." → "그는 보고하고 자리에 앉았다.")
- **A-20 [S2] Other calques.** "~중 하나" ("가장 빠른 도구 중 하나입니다" → "손꼽히게 빠릅니다"); "~을
  제공합니다" ("다양한 기능을 제공합니다" → "여러 기능을 쓸 수 있다"); "다음과 같습니다" → "이렇다"; "~하게
  만들어 준다" ("설치를 쉽게 만들어 줍니다" → "설치가 쉬워진다"); dummy subject "그것은 / 이것은 ~이다";
  "당신" as direct address; "~하는 경향이 있다" (tend to); "~하는 것이 가능하다" → "~할 수 있다"; "~라는
  사실에 기인하여" → "~때문에"; "현 시점에서 볼 때" → "지금"; "~기에는 너무 ~하다" (too ~ to) → "워낙 ~해서".
- **A-21 [S2] Inanimate plural "-들" on abstract nouns.** → Delete, or distribute with 여러·다양한·갖가지·
  저마다. ("새로운 아이디어들과 방법들" → "여러 남다른 생각과 방법") Weak evidence; fix only when it clusters.
- **A-22 [S2] Connective flattening: cause or sequence rendered as mere enumeration -고/-며.** Models
  over-use -고/-며 for listing where the logic is causal or sequential. → Restore the relation: "리스크가
  커지고, 신뢰가 훼손되며, 충격이 발생한다" → "리스크가 커져 신뢰가 훼손되면서 충격이 발생한다". Also a
  sentence-initial clause forced into a topic subject ("~의 시행은 …로 이어져") → "~ 시행에 따라 …".

## B. 영어 병기·용어 (English glosses and jargon) — S2

- **B-1 [S2] Korean + parenthesised English on every mention.** → Gloss on first mention only.
- **B-2 [S2] Marketing buzzwords (seamless, robust, leverage, 인사이트, 임팩트, 시너지, 모멘텀, 페인
  포인트).** → Paraphrase in Korean (seamless → 끊김 없는; robust → 튼튼한; leverage → 활용하다; insight
  → 통찰/시사점). Keep standard technical terms (API, SDK, prompt, token, embedding, agent, pipeline).
- **B-3 [S2] "~라고 알려진 / ~로 일컬어지는" (known as, so-called).** → Just the term, gloss once.
  ("'AGI'라고 알려진 범용 인공지능" → "범용 인공지능(AGI)")

## C. 구조 (structure) — S1~S2

- **C-1 [S1 at 2+] Antithesis chains.** "A인가, B인가", "A가 아니라 B", "단순히 A가 아니라 B", "A라기보다
  B", "~것이 아니라", "~것은 아니다", "X는 단순히 A가 아니다. B다" (redefinition, clusters in the first
  15% of AI text). **The strongest measured tell in Korean** (9 to 12×, all models). The real
  discriminator is *chained uniformity*: adjacent sentences all in the same mold. → Keep ONE. Turn the
  rest into asymmetric prose: one side long, one short; split; make one side a question and the other
  a statement. Never reduce to zero when the text had many (that is annihilation, also a tell). Never
  plant a new antithesis elsewhere while fixing.
  Examples that worked:
  "기술은 도구이고, 사람은 주체다. 데이터는 연료이며, 알고리즘은 엔진이다." → "기술은 도구다. 사람이 그
  도구를 쥔다. 데이터가 있어야 알고리즘이 돌아간다."
  "중요한 것은 속도가 아니라 방향이며, 양이 아니라 질이다." → "속도보다 방향이 중요하다. 양은 그다음 문제다."
  "기계는 답을 주지만, 질문은 주지 않는다." → "기계는 답을 준다. 질문은 여전히 사람 몫이다."
- **C-2 [S2] Three or more consecutive bullets in a column, essay, or report.** → Prose. ("- 속도가 빠르다
  / - 비용이 저렴하다 / - 확장성이 높다" → "속도는 빠르고 비용도 낮다. 무엇보다 확장 여지가 크다.") Keep a
  list only where enumeration carries meaning.
- **C-3 [S1] Emoji as list markers, headings, emphasis.** → Delete in column or report genres. Keep only
  in SNS or product copy that already had them.
- **C-4 [S2] Ordinal scaffolding "첫째, 둘째, 셋째", "먼저 – 반면 – 결국", "1) 2) 3)".** Preserve by
  default; a natural three-item list is human. → At 4+ items reading like a metronome, melt one or two
  into prose, vary with 우선/다음으로/마지막으로, and unbalance item lengths on purpose.
- **C-5 [S1 at 6+, S2 at 3–5] Comma right after a connective ending** (-고, / -며, / -지만, / -면서, /
  -아서, / -는데,). Human 4% vs AI 20% of connective boundaries. → Delete the comma; if the sentence is
  too long, split with a period or move the comma to the main-clause boundary. **Never judge a text on
  this alone**; one human essay ran 83%. **Your rewrite must not add any** (see N).
- **C-6 [S2] Comma density.** Over half of sentences contain a comma (human 26% vs AI 61%); comma
  segments average 8+ 어절 (human 4.4). Japanese-style commas after 는/도 and after a sentence-initial
  adverb ("저는, 작년 가을부터, …"). → Fewer commas; restrict to main-clause boundaries and clear
  appositives; absorb into 연결어미 or split.
- **C-7 [S1] Colon-subtitle headings "X: Y", "서론: 제조업의 미래", "X: A에서 B로".** → One noun phrase;
  at most one per document. Real section titles in academic or report formats stay.
- **C-8 [S2] Schematic headings "도입 / 본론 / 결론"; a summary line right under every heading ("이
  섹션에서는 ~를 다룬다"); heading count out of proportion to text (H2–H4 in a 500-character section).**
  → Remove in prose genres; concretise in reports. Real section titles are inviolable.
- **C-9 [S2] Every paragraph opens with a topic sentence, then restates it.** → Start some paragraphs
  with a scene, a number, a quote, or a question. Drop the restatement.
- **C-10 [S2] Fractal summary and scaffold.** "이번 글에서는 ~를 살펴보겠습니다 / 알아보겠습니다" at the
  start, "지금까지 ~를 살펴보았습니다" at the end; "그렇다면 해답은 무엇일까요? 바로 ~입니다." rhetorical
  question with instant answer; "~(으)면 어떨까요?"; "상상해 보세요". → Delete the scaffold; open on the
  content; answer without staging the question.
- **C-11 [S2] Three-step expansion formula.** "개인 → 기업 → 사회 전체"; "단기적으로는 ~, 중기적으로는 ~,
  장기적으로는 ~". → Keep the level the text actually argues; cut the reflexive ladder.
- **C-12 [S2] Arrow chains "기획 → 개발 → 테스트 → 배포" in prose.** → A sentence.

## D. AI 관용구 (signature phrases) — S1 by default

Removal target only. **Never generate any of these while rewriting** (a real complaint: living speech
"얼마나 대단했냐면 —" was replaced with "기록적인 성과를 거두었다·괄목할 만한·~로 평가된다").

- **D-1 [S1] Wrap-up lexicon.** 결론적으로 / 요약하면 / 종합하면 / 정리하자면 / 궁극적으로 / 요컨대;
  "~라고 할 수 있다 / ~라고 볼 수 있다"; "~라 하겠다 / ~라 할 것이다"; "~에 다름 아니다". → Delete; the last
  paragraph is already the conclusion. "~라고 할 수 있다" → "~이다" only if the text already treats it as
  fact; otherwise "~로 보인다" (same hedge strength).
- **D-2 [S1] Inflated significance.** 시사하는 바가 크다 / 주목할 만하다 / 매우 중요하다 / 간과할 수 없다 /
  무시할 수 없다 / 의미심장하다 / 그 의미가 적지 않다 / ~에 방점을 찍는다 / ~의 지평을 연다 / ~라는 사실은
  부인할 수 없다. → Prefer deflating to deleting: keep the judgment at plain strength ("시사하는 바가 크다"
  → "의미가 있다") or replace with the concrete reason from the text ("X 없이는 Y가 성립하지 않는다").
  Delete the whole sentence only when nothing but inflation remains, and say so in the change report.
- **D-3 [S1] List lead-ins.** 크게 세 가지로 나눌 수 있다 / 다음과 같은 특징을 가진다 / 다음과 같이 요약할 수
  있다. → Delete; start with the content.
- **D-4 [S2] Hype vocabulary.** 혁신적 / 획기적 / 전례 없는 / 압도적 / 막강한 / 폭발적 / 파격적 / 대대적 /
  선도적 / 차별화된 / 독보적; "~의 가능성을 열어준다", "~의 새로운 장을 열다", "~시대가 도래했다", "판도를
  바꾸다", "게임 체인저", "~의 패러다임". Weak as an AI discriminator, but the fix concretises. → A number or
  fact from the text; 혁신적 → "처음 시도한 / 이전과 다른". No fact available → plain adjective or delete.
- **D-5 [S2] Personified abstract subjects.** "두 지능의 충돌이 질문을 던집니다", "시대가 부른다", "데이터가
  말해준다", "시장이 보상한다", "숫자가 증명한다". → A person or organisation as subject ("엔지니어들은",
  "두 회사의 경쟁은"), or a weaker verb (던집니다 → 남습니다/생깁니다). One symbolic use in a title is fine.
  Genuine agentless events and software actions are not targets.
- **D-6 [S1] Cleft and focus formulas.** "필요한 것은 / 중요한 것은 X이다"; "문제는 / 핵심은 / 관건은 / 답은
  ~이다 / ~는 점이다 / ~데 있다"; comparative ladder "더 심각한 것은 ~다"; two-step "문제는 X다. 답은 Y다."
  Human 0.09 vs AI 0.92. → Subject–predicate: "필요한 것은 방향이다" → "방향이 필요하다"; "문제는 양측이 합의에
  이르는 경우가 거의 없다는 점이다" → "양측은 합의에 이르는 일이 거의 없다".
- **D-7 [S2] Closing formulas.** "~할 때입니다 / ~시점입니다 / ~할 순간입니다"; "~를 고민해야 할 시점이다";
  "~에 대한 성찰이 필요하다"; "~가 중요하다" as a bland last line. → A concrete verb assertion; at most
  once per document.
- **D-8 [S2] Transformation slogan "X에서 Y로", "'무엇을'에서 '어떻게'로".** → Direct assertion; at most
  once per document.
- **D-9 [S2, human 0] Causal wrap-ups.** "결국 ~로 이어진다", "~에 직결된다", logical-summation 결국
  (humans use 결국 only narratively: "결국 회사를 나갔다"); inverted "~하는 이유다" (This is why) at a
  paragraph end; sentence-initial "향후 / 앞으로 / 중장기적으로" in the closing third with no concrete time
  or condition. → Write the actual causal path from the text ("상권 매출이 줄고 일자리가 사라진다"), or
  "그래서 ~다"; 결국 at most once. For 향후/앞으로, delete the time word or use a real one already in the
  text ("2027년 이후", "금리가 내려갈 경우"). Never fabricate a date.
- **D-10 [S2] Content-free counter slot.** A standalone "그러나 과제도 남아 있다 / 한계도 분명하다 / 아쉬운
  점도 있다", the both-sides closer "빛과 그림자가 공존하는 만큼 균형 잡힌 시각이 중요하다", and the
  unconditional bright ending "앞으로의 발전이 기대된다 / 무한한 가능성 / 더 나은 미래를 향한 첫걸음 /
  흥미진진한 여정". → Delete the signpost and put the real issue first ("다만 야간 작업 안전 기준이 아직
  없다"). A content-bearing "안전 기준 정비도 과제로 남아 있다" is fine. Cut the bright ending; end on the
  last concrete fact.
- **D-11 [S2, essays only] Reflective adverbs at the ending.** "어쩌면 ~일 것이다", "~하자 비로소", "천천히
  ~이 됐다". → Remove the adverb; write concretely.
- **D-12 [S2] Generative metaphors in argument prose.** Families: 경제 질량 (잠식·흡수·짓누르다·삼키다),
  회계 (청구서가 날아온다·성적표·대가를 치르다), 농경 (과실·씨앗·뿌리내리다), 건축 (청사진·주춧돌·문턱), 무게
  (어깨에·짊어지다), 신호 (신호탄·적신호·경고등), 거울·그림자; definitional equations "X는 Z의 언어/통화/
  건축물/DNA/엔진/심장박동이다"; **sensory-predicate evaluation** "1부의 진단은 서늘하다", "3부의 경고는
  아프다" (human 0); a running metaphor whose root appears 3+ times ("쥐다" ×4). → Literalize, don't
  delete: 잠식한다 → "점유율을 뺏는다" (not "사라진다", which shifts intensity); 서늘하다 → "정곡을 찌른다";
  "침묵은 권력의 언어다" → "침묵에는 권력 관계가 드러난다". Running metaphor: keep the single best
  occurrence, flatten the rest. Keep a metaphor that *is* the thesis. Frozen idioms (열쇠를 쥐다·양날의
  검·기로에 서다) are not a signal.
- **D-13 [S2] Time-cliché openers.** "오늘날 급변하는 시대에", "요즘 빠르게 변화하는 세상에서는", "4차 산업혁명
  시대를 맞이하여", "21세기 들어", "~의 시대가 도래하면서"; historical-analogy parade "인쇄술이 그랬고,
  인터넷이 그랬고…". → Open on the content.
- **D-14 [S2] Sajaseong-eo and translated flattery as ornament.** 일석이조·온고지신·백미 dropped in for
  gravity; "심층적으로 들여다보면", "통찰력 있는". → Plain words.

## E. 리듬 (rhythm and sentence length) — S2

- **E-1 [S2, 11×] No long sentence anywhere.** The real signal is not uniform 30–50자 sentences but the
  *absence* of any 100자+ sentence (AI 8 vs human 91 per 1,000 sentences). → Without adding content,
  build one 80–100자+ sentence per few paragraphs by joining neighbours with -며/-고/-는데/-면서/-자, a
  관형절, or a 조건절, and drop in one or two 10–15자 sentences.
- **E-2 [S2] All simple S–V sentences (단문 일변도).** "AI는 빠르게 발전한다. 기업은 따라가야 한다. 시간이
  없다." → Join two or three: "AI가 빠르게 발전하는 가운데 기업은 따라가야 한다. 시간은 없고 데이터는 핵심이며,
  인재마저 부족하다." Aim for roughly 60% simple, at least 30% complex.
- **E-3 [S2] Same ending four or more in a row** ("~이다. ~이다. ~이다."), "~다" streak (AI skews 1.8×),
  "~습니다" monotony (5+), automatic progressive "~고 있다" mapped from English -ing. → Vary: ~다 / ~았다 /
  명사형 종결 / ~기 마련이다 / ~ㄹ 것이다 / ~인 셈이죠 (spoken) / ~거든요 (spoken, only if the register has
  it). "읽고 있다" → "읽는다" where simple tense carries the meaning. Don't fix by planting "~인 셈이다"
  repeatedly (that is its own tell, I-2).
- **E-4 [S2] Every paragraph 3–4 sentences.** → Mix one-sentence and six-sentence paragraphs. Let
  section depth vary.
- **E-5 [S2, dialogue and spoken genres only] Honorific-level mixing in one text.** "도와주시겠습니까?" then
  "도와줘?"; a ~합니다 paragraph followed by a ~한다 paragraph. → Pick one level and hold it. Formal
  single-register reports are exempt; there the problem is the reverse (E-3).

## F. 명사화·수식 (nominalisation and modifiers) — S2

- **F-1 [S2] Degree adverbs 매우·정말·굉장히·대단히·극히; auto-inserted manner adverbs 효과적으로·성공적으로·
  적극적으로·체계적으로·전략적으로.** → Delete about 90%; a number instead where the text has one. Spoken
  author voice ("정말 그랬다니까") stays.
- **F-2 [S2] Synonym double modifiers and noun pairs.** "중요하고 핵심적인 역할", "새롭고 혁신적인 접근",
  "지속적이고 꾸준한 노력"; "~로서의 역할과 기능", "~의 의미와 가치". → Keep one.
- **F-3 [S2, 1.6×] Sino-Korean nominalisation stacks (-성/-적/-화) and "~적 N" chains** ("전략적 함의",
  "기술적 안정성", "에이전트적 자율성"); calqued -tion/-ment nouns. → Verb or adjective root. ("근본적
  관점에서 구조적 변화가 필연적이다" → "구조가 근본부터 바뀐다"; "전략적 함의" → "전략 함의"; "정책의 시행" →
  "정책 시행") Halve the density; don't zero it.
- **F-4 [S2, 3.4×] Convergence on generic policy verbs and nouns.** 확대·강화·개선·확보·마련·집중·유지·구축·
  지원 (+해야 한다); abstract-object "설계/재설계" ("관계를 설계", English *design* valency); "구조", "기준"
  as catch-all nouns; "다양한 / 폭넓은 / 광범위한 / 수많은"; "핵심적인 역할을 수행한다". Hard bureaucratic
  Sino-Korean (제고·도모·박차) shows **no** gap; the tell is the plain generic word. → Concrete action:
  "지원을 확대해야" → "지원 대상을 넓히거나 예산을 늘려야"; "관계를 설계" → "관계를 맺다"; "비용 구조" →
  "임대료와 인건비 부담"; "다양한 분야에서" → name the fields if the text does, else "여러 분야에서". **Do not
  multiply "~해야 한다" while unpacking.**
- **F-5 [S2] "N 능력" chains 3+** ("사고 능력", "추론 능력", "장기 문맥 유지 능력"). → Verbify: "잘 사고한다",
  "워크플로우를 얼마나 잘 처리하는지". At most two per document.
- **F-6 [S2] Demonstrative overuse 이러한·그러한·해당 + repeated explicit subject** ("이 서비스는… 이
  서비스는…"). → Drop the obvious subject (Korean allows it); use 이/그 or nothing.
- **F-7 [S2] Chained superficial analysis "~하며, ~하고, ~하며"** ("다양성을 보여주며, 조화를 상징하고,
  활성화에 기여하며"). → Split into sentences with concrete verbs, or cut the evaluative links.

## G. 완곡·서법 (hedging and modality) — preserve by default

Obligation ("~해야 한다") and speculation ("~일 수 있다", "~로 보인다") are **meaning, not style**. The
number of hedge and obligation markers must be the same before and after the rewrite. The only allowed
operations are varying the *form* at the same strength, or moving a sentence.

- **G-1 [S2] Repeated conjectural endings "~로 보인다 / ~로 판단된다 / ~라고 여겨진다 / ~인 듯하다".** →
  At 4+ of the same form, vary it at equal strength: ~로 보인다 / ~인 듯하다 / ~로 해석된다 / 아직 단정하기는
  이르다. Never convert to assertion. **Polarity guard**: "~되지 않을 수 있다는 걱정이 있습니다" rewritten as
  "~되지 않을까 우려됩니다" flipped a worry into a hope in a real business email. If negation is present,
  verify the polarity twice; if unsure, leave it.
- **G-2 [S2] Stacked hedges "~할 가능성이 있을 수 있다", "~로 보여질 수 있다".** → Exactly one hedge, same
  polarity and confidence. "가능성이 있을 수 있어" → "가능성이 있어" upgrades a hedge to a promise; that is
  forbidden. Negotiation, contract, and reply emails where stacked hedging *is* the stance are exempt.
- **G-3 [S2] Balance lexicon "양쫽 모두 / 장점도 있지만 / 신중하게 / 균형" at 4+; "A이기도 하고 B이기도
  하다", "~면서도 ~하다" balanced-sentence reflex.** Weak evidence. → Take the side the text takes, compare
  concretely, or make it conditional ("X일 때는 A, Y일 때는 B").
- **G-4 [S2] Fake nuance and fake humility.** "사실 좀 더 미묘한 문제인데", "공정하게 보자면", "물론 이것은
  하나의 관점일 뿐입니다", "정답은 없겠지만, 분명한 것은". → Delete the announcement; keep what follows.

## H. 접속사 (connectives) — conservative

- **H-1 [S2] Sentence-initial 또한 / 따라서 / 즉 / 나아가 / 아울러 / 게다가 / 더욱이 / 이와 더불어 / 이에 따라 /
  이러한 맥락에서.** Evidence is model-dependent (one model 16× human, others *below* human). → Only when
  3+ appear in one paragraph, remove about half in that paragraph. Never a document-wide purge. Never
  bare-delete a link that carries logic; let sentence order carry it, or use a plainer one.
- **H-2 [S2] 하지만 / 그러나 opening every paragraph.** → Cut half or more; alternate with 그런데, or
  none.
- **H-3 [S2] Meta openers "이는 ~ / 이 점에서 / 이 관점에서 보면 / 이 말은 ~라는 뜻이다".** Normal Korean
  discourse (humans use more). → Preserve; straighten some only at 3+ in a paragraph.
- **H-4 [S2] 즉 / 다시 말해 / 바꿔 말하면 used to repeat the same point.** → Cut the restatement; 즉 at most
  twice per document. "왜냐하면 ~ 때문이다" as a calque → "~때문이다" or "~이기 때문에".

## I. 형식명사·당위 (bound nouns and obligation) — S1~S2

- **I-1 [S2, preserve by default] "~한 것이다 / ~일 것이다".** Humans use it 2× more. → Only at 3+
  consecutive, turn some into plain "~다".
- **I-2 [S1] Bound-noun emphasis and wrap-ups.** "주목할 점은 ~라는 점이다", "X은 ~라는 점에 있다", "~다는
  것이다 / ~다는 뜻이다" closers, "~인 셈이다" repeated (human 0 vs AI 7). → Direct statement "X는 ~다".
  At most two combined closers per document.
- **I-3 [S1, 7×] Paragraphs that end on obligation.** "~해야 한다 / ~할 필요가 있다 / ~이 요구된다 / ~이
  강조된다 / ~바람직하다" as the last sentence of two or more paragraphs (the first one is exempt). This
  is the signal; raw density is not. → **The only allowed action is to move the obligation sentence
  earlier in its paragraph** so the paragraph ends on a fact. Forbidden: merging two obligations,
  deleting the marker, changing modality, nominalising ("~하는 것이 과제다"), subordinating. Marker count
  before == after.
- **I-4 [S2] Nominal proposals "혁신이 필요하다 / 변화가 필요하다".** → Say who does what. But **do not
  end every sentence in "~해야 한다"** while unpacking (measured: 3 obligation markers became 8). If
  nominal endings are the skeleton of a list, keep them; vary with "~하는 일이 남았다 / ~가 먼저다".
- **I-5 [S2] Agentless verdict "~다는 분석이다 / 평가다 / 관측이다" with no source anywhere.** → If a
  source is named nearby, it's normal journalism; keep. Otherwise strip the shell to a direct statement.
  Never invent a source ("전문가들은 / 일각에서는 / 업계 관계자에 따르면" with nothing behind it is the same
  problem: state it plainly or flag "출처 확인 필요").

## J. 시각 장식 (visual decoration) — S2

- **J-1 [S2] Bold on the key word of every sentence; inline-header bullets "- **사용자 경험:** 설명".** →
  In columns and reports, remove almost all body bold.
- **J-2 [S2] Quotation-mark emphasis 5+** ('옥석 가리기'·'금융 슈퍼앱'·'데이터 피로감'); 「」 corner brackets
  in Korean. → Real quotations only; first mention at most.
- **J-3 [S2] Dash (—) asides.** → Commas, parentheses, or separate sentences; at most one or two per
  document. **Dashes already in the source as living speech ("얼마나 ~냐면 —") stay.**
- **J-4 [S2] Repeated parenthetical gloss "(이는 ~을 의미한다)".** → Absorb into the body or delete.

## K. 챗봇 잔재 (chatbot residue) — S1, strip before anything else

"물론입니다!", "다음은 ~입니다:", "요청하신 내용을 정리하면", "도움이 되셨길 바랍니다", "추가 질문이 있으시면",
"제 지식은 ~까지입니다", "~년 기준으로 최신 정보와 다를 수 있습니다", "구체적인 정보는 제한적이나"; flattery
"좋은 질문이십니다!", "정말 핵심을 찌르는 질문이네요", "정확하게 짚어주셨는데요"; teacher mode "쉽게 말해서
~라고 이해하시면 됩니다", "간단히 설명드리자면"; corporate frame "당사는 / 저희는 ~드립니다" where the text
isn't corporate. → Delete entirely. These are chat framing, not part of the text.

## L. 사람 글의 표지 (human markers to preserve)

Measured as human-only or human-heavy. Their presence is evidence a person wrote it. Never strip them,
and never inject fake versions.

- Speaker self-intervention: "솔직히 말하면", "모르겠지만", "내가 보기에", "잘은 모르지만" (human 13 docs vs
  AI 0). Note this is the **opposite** of English, where "Honestly?" as a standalone opener is a tell.
- Sentence-initial "또," (humans; AI writes "또한"). "당시" (human 10 vs AI 0). "힘들다" (5 vs 0).
  Benefactive "~해 주다".
- A concrete person, case, or scene threading the text; a time or place anchor in the first sentence
  ("2019년 봄, 대전에서…"). If the text has one later, it may be *moved* to the opening; never invented.
- Local emotional spikes: mockery, an exclamation, a rhetorical jab ("지나가던 소도 웃을 일이다").
- Spoken endings ~인데요 / ~거든요 / ~한 겁니다 / ~잖아요; contractions ("안 해요" over "하지 않습니다");
  short exclamations; a dash used for a spoken beat.
- Irregular spacing of bound nouns and auxiliaries ("할수있다", "것같다"): AI spacing is unnaturally
  consistent. Don't "correct" an author's spacing habits unless asked.
- Repetition of a plain word instead of synonym cycling (이 도시 / 이 지역 / 해당 지자체 / 이곳 is the AI
  habit).
- Everyday "~에 대해", "~를 통해", "~것이다", "~을 위해" at ordinary density. See section 0.

## M. 표지가 아닌 것 (not tells)

- Perfect 맞춤법 by itself. Formal register by itself. A single connective. A single "~에 대해".
- Frozen idioms (열쇠를 쥐다, 양날의 검, 기로에 서다). Hard bureaucratic Sino-Korean (제고, 도모) in a
  document that is bureaucratic.
- A three-item list. One antithesis. Hedges appropriate to the claim. Commas in one paragraph.
- Quoted speech, titles, proper names, and any passage discussing an expression rather than using it.
- Text the author says predates late 2022.

## N. 재작성 중 주입 금지 (things a rewrite tends to inject)

Measured on humanizer output itself. Check the *rewrite* for these before returning:

- Commas after connective endings (16 of 28 light rewrites added some). Count before and after.
- New antitheses "A가 아니라 B" planted elsewhere while removing one (documents with antithesis went
  12 → 14 in one batch).
- 결국 / "~하는 이유다" / "~로 이어진다" used to tidy an ending (2 → 4, 0 → 2).
- "더 이상 A가 아니라 B" as a redefinition.
- "~해야 한다" multiplied while unpacking nominal proposals (3 → 8).
- Any D-series cliché (기록적인 성과, 괄목할 만한, 주목받았다, 의미가 크다, 지금이야말로 ~할 때입니다).
- Register upgrade ('-했-' → '-하였-'), erased spoken endings, literary embellishment.
- A new hedge or a lost hedge; a new obligation or a lost one.
- A fabricated date after 향후/앞으로, a fabricated source after a verdict, a fabricated specific
  replacing a vague claim.

---

## Self-check (after rewriting)

1. Proper nouns, numbers, dates, quotations: identical, character for character.
2. Nothing invented: no fact, source, date, specific, or opinion that wasn't in the source.
3. Nothing dropped: each sentence's core content nouns survive at least once (particles and endings may
   change). A whole-sentence deletion is disclosed in the report.
4. Modality preserved: hedge and obligation marker counts equal before and after; no polarity flip.
5. Register and genre unchanged; human markers (section L) preserved.
6. Nothing from section N was injected.
7. The dominant tells diagnosed are gone, not merely thinned. Antitheses reduced, not annihilated.
8. Change rate roughly 10–30% (up to ~40% for tell-dense text). Above 50%: roll back and redo.

## Internal grading (never shown to the user)

Use only to decide whether to recommend a stronger second pass. Do not print grade letters or codes in
the report; translate them into plain words such as "이제 자연스럽다" or "아직 조금 AI 티가 남았다".

- Clean: 0 strong tells, ≤2 weak tells, 10–25% change, all self-check items pass.
- Mostly clean: 0 strong tells, ≤4 weak tells, most self-check items pass.
- Needs another pass: 1–2 strong tells remain or several self-check items fail → offer a stronger rewrite.
- Stop and disclose: 3+ strong tells or >50% change → roll back and redo, or tell the user a human review
  is needed.
