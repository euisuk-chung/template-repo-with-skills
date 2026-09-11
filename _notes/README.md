# 작업 기록

공용 스킬로 작성한 프로젝트 작업 문서를 보관합니다. Claude와 Codex 모두 같은
경로를 사용하며, 스킬 원본은 `.agents/skills`에서 관리합니다.

- [grills](grills/README.md): `grill-me` 인터뷰로 확정한 요구사항·설계 결정 기록
- [handoffs](handoffs/README.md): `handoff`가 작성하는 수신 대상별 작업·리뷰 지침서

각 폴더의 `README.md`는 템플릿에 포함됩니다. 그 외 작업 문서와 첨부 파일은
`.gitignore`로 제외하며 로컬에만 보관합니다. 다른 환경의 세션이나 담당자에게
인계할 때는 필요한 문서와 입력 자료를 별도로 전달하세요.
자격 증명이나 민감한 개인정보는 기록하지 않습니다.

## 파일명 규칙

두 폴더 모두 `<yymmdd-hhmm>-<topic-slug>.md` 형식을 사용합니다. 이 규칙은 생성되는
작업 문서에 적용하며, 안내 문서인 `README.md`는 예외입니다.
`scripts/sync_skills.py --check`가 이 형식을 자동으로 검사합니다.

- 접두어는 문서를 처음 만든 시각(두 자리 연도·월·일, 24시간제 시·분)입니다. 갱신할 때
  파일명은 유지하고 문서 안의 `Updated`만 바꿉니다. 시간대는 문서 안에 적습니다.
- 슬러그는 영문 소문자·숫자를 단일 하이픈으로 연결합니다. 공백, 밑줄, 한글,
  연속 하이픈, 앞뒤 하이픈은 사용하지 않습니다.
- 주제를 짧고 구체적으로 표현합니다. 한국어 주제는 의미를 전달하는 영문으로
  이름을 짓고, 문서 제목과 본문은 한국어로 작성해도 됩니다.
- 작성자·하네스 이름을 파일명에 붙이지 않습니다.
- 같은 주제의 인터뷰와 인계 문서는 같은 슬러그를 사용합니다. 구현과 리뷰처럼
  별개 요청을 함께 보관할 때는 `search-filter-review`처럼 요청 목적을 덧붙입니다.
- 인계 문서는 수신 대상 폴더(`to_codex`, `to_claude`, `to_human`) 아래에 둡니다.
  폴더명은 고정이며, 파일명의 하이픈 규칙과 별개입니다.
- 생성 전에 기존 파일을 확인합니다. 같은 주제면 읽고 갱신하고, 이름이 겹치는
  다른 주제라면 `admin-search-filter`처럼 구별되는 범위를 이름에 넣습니다.
  `-2`, `-final`, `-latest`를 붙여 중복 파일을 만들지 않습니다.
- `readme`는 안내 문서용으로 예약합니다. Windows 호환을 위해 `con`, `prn`,
  `aux`, `nul`, `com0`~`com9`, `lpt0`~`lpt9`도 슬러그로 사용하지 않습니다.

예를 들어 검색 필터 작업은 다음 문서로 연결합니다.

```text
_notes/grills/260908-1430-search-filter.md
_notes/handoffs/to_codex/260908-1500-search-filter.md
_notes/handoffs/to_claude/260908-1600-search-filter-review.md
_notes/handoffs/to_human/260908-1600-search-filter-review.md
```

기본 형식은 정규식 `^\d{6}-\d{4}-[a-z0-9]+(?:-[a-z0-9]+)*\.md$`로 표현할 수 있습니다.
