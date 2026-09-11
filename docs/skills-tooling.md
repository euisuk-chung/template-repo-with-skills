# 공용 스킬 도구 상세

Codex와 Claude Code가 하나의 저장소 스킬셋을 공유하도록 구성한 도구의 상세 설명입니다.
실제 스킬은 `.agents/skills`에서만 관리하고, Claude Code가 발견할 수 있도록
`.claude/skills`에는 중앙 원본을 읽는 텍스트 어댑터를 생성합니다.

심볼릭 링크를 사용하지 않으므로 Windows의 Developer Mode나 Git `core.symlinks` 설정
없이 Linux와 Windows에서 같은 구조로 동작합니다.

## 구조

```text
.agents/skills/                 # 스킬 원본(Single Source of Truth)
├── CATALOG.md                  # 자동 생성되는 그룹별 스킬 목록
└── <skill-name>/
    ├── SKILL.md                # 지침 (영어)
    ├── scripts/                # 실행 코드와 환경 파일 (pyproject, uv.lock, .venv)
    ├── references/             # 필요할 때만 읽는 참고 문서
    └── assets/                 # 템플릿·정적 파일
.agents/skills.lock             # 자동 생성되는 스킬 해시·공용 스킬 출처
.claude/skills/                 # 자동 생성되는 Claude 텍스트 어댑터
scripts/sync_skills.py          # 어댑터·카탈로그·lock 생성 및 검증
scripts/update_shared_skills.py # 템플릿에서 공용 스킬 갱신
```

Codex는 `.agents/skills`를 직접 탐색하므로 `.codex/skills`는 두지 않습니다.
Claude Code는 `.claude/skills/<skill-name>/SKILL.md`를 탐색하고, 어댑터 본문에
적힌 저장소 루트 기준 경로를 따라 중앙 스킬을 읽습니다.

## 스킬 그룹과 출처

두 하네스 모두 `skills/<name>/SKILL.md` 평면 구조만 탐색하므로 하위 폴더로 묶지
않습니다. 대신 frontmatter의 `metadata`로 논리 그룹과 출처를 표시하고, 동기화
스크립트가 `.agents/skills/CATALOG.md`를 그룹별로 생성합니다.

| 필드 | 값 | 의미 |
| --- | --- | --- |
| `metadata.group` | `writing`, `visual`, `workflow`, `repo`, 또는 새 이름 | 카탈로그 그룹 |
| `metadata.origin` | `shared` | 템플릿 저장소가 관리하고 `update_shared_skills.py`로 갱신 |
| `metadata.origin` | `local` | 이 저장소 전용. 공용 스킬과 같은 이름은 사용 불가 |

## 스킬 추가

`.agents/skills/<skill-name>/SKILL.md`를 만듭니다. **스킬은 항상 영어로 작성합니다.**
한국어 텍스트를 다루는 스킬은 판단에 필요한 한국어 용어·조사·예문만 남기고 영어
설명을 병기합니다.

```markdown
---
name: my-skill
description: Describe precisely when this skill should be used.
metadata:
  group: repo
  origin: local
---

# My skill

Write the instructions here.
```

스킬 디렉터리명과 `name`은 같아야 하며 소문자, 숫자, 하이픈만 사용합니다.
`name`은 한 줄 YAML scalar로 작성합니다. `description`은 영어 한 줄 또는 YAML block
scalar(`>`/`|`)를 사용할 수 있습니다. Claude 전용 옵션(`argument-hint`,
`disable-model-invocation`, `allowed-tools`, `user-invocable`, `model`)과 스펙 필드
(`license`, `compatibility`)는 허용되며 어댑터에 그대로 전달됩니다. 그 외 키는 거부됩니다.

외부 YAML 패키지 없이 검증하기 위해 지원 문법을 제한합니다. `metadata`는 두 칸
들여쓰기의 평면 문자열 mapping이고, 주석은 허용합니다. 문자열에는 따옴표를 권장하며
콜론+공백, 숫자·날짜·불리언처럼 보이는 값은 따옴표로 감쌉니다. 작은따옴표 또는 JSON
호환 큰따옴표를 사용할 수 있습니다. 리스트·alias·추가 중첩·scalar의 줄 연장은 지원하지
않습니다. `allowed-tools`도 리스트 대신 한 줄 문자열로 씁니다. 불리언 옵션 두 개
(`disable-model-invocation`, `user-invocable`)만 따옴표 없는 `true`/`false`를 받습니다.

그다음 생성물을 갱신합니다.

```shell
python3 scripts/sync_skills.py     # Linux/macOS
py -3 scripts/sync_skills.py       # Windows PowerShell
```

`.claude/skills`, `CATALOG.md`, `skills.lock`은 직접 편집하지 않습니다.
`.agents/skills` 아래를 바꾼 뒤에는 동기화 명령을 다시 실행하고 함께 커밋합니다.
pre-commit 훅 `sync-skills-check`가 커밋 전에 `--check`를 실행합니다.

## 다른 저장소에서 공용 스킬 사용

1. 템플릿으로 새 저장소를 만들고 `scripts/bootstrap_template.py`로 초기화합니다.
2. 저장소 전용 스킬은 `origin: local`로 추가합니다.
3. 템플릿의 공용 스킬이 바뀌면 다음으로 갱신합니다.

```shell
python3 scripts/update_shared_skills.py --ref v1.0.0        # 태그 또는 브랜치
python3 scripts/update_shared_skills.py --source ../template-repo-with-skills
python3 scripts/update_shared_skills.py --dry-run           # 변경 예정 파일만 표시
```

갱신 스크립트는 `origin: shared` 스킬, 스킬 도구(`scripts/sync_skills.py`,
`scripts/update_shared_skills.py`, 두 테스트 파일, `validate-skills.yml`, 스킬 README)를
덮어쓰고, `_notes/**/README.md`는 없을 때만 생성합니다. `local` 스킬, 스킬 안의 `.venv`
같은 로컬 환경, 프로젝트 파일(`pyproject.toml`, `ci.yml`, 루트 README)은 건드리지
않습니다. 출처 URL·ref·커밋은 `.agents/skills.lock`의 `shared_source`에 기록됩니다.

갱신은 임시 작업본에서 **새 sync 도구**로 생성과 `--check`를 완료한 뒤 실제 파일에
반영합니다. 사전 검증 실패 시 대상 파일은 바뀌지 않으며, 반영 중 잡힌 쓰기 오류는
기존 파일 내용과 권한을 복구합니다. 전원 차단·프로세스 강제 종료·지속적인 디스크 오류까지
보장하는 트랜잭션은 아닙니다. 동기화/업데이트 도중 다른 프로세스가 같은 파일을 수정하지
않게 하세요. 복구 자체가 실패하면 해당 경로를 오류로 보고하므로 백업과 Git 상태를 확인하세요.

`--dry-run`도 임시 작업본에서 새 도구를 실행해 검증하며 생성물 변경까지 표시합니다.
따라서 **신뢰하는 source만** 사용하세요. 새 metadata 문법을 이전 updater가 읽지 못하는
버전 전환은 대상 수정 없이 실패하며, 별도 도구 마이그레이션이 필요합니다.
로컬 디렉터리 source는 `--ref`를 적용하지 않고 미커밋 내용까지 복사합니다.
이때 기록된 commit은 HEAD 정보일 뿐, 복사된 전체 내용을 재현하는 식별자는 아닙니다.

하위 저장소에서 공용 스킬을 직접 고치면 `--check`가 lock 불일치를 보고합니다. 변경은
템플릿 저장소에 반영한 뒤 태그를 올리고 다시 갱신하세요.

## 검증

```shell
python3 scripts/sync_skills.py --check
python3 -m unittest discover -s tests -p "test_*_skills.py"
```

스킬 도구는 표준 라이브러리만 사용하므로 uv 환경 없이 시스템 Python으로도 실행됩니다.
`uv run pytest`는 같은 테스트를 프로젝트 테스트와 함께 실행합니다.

검사는 다음 항목을 확인합니다.

- 중앙 스킬의 필수 frontmatter(`name`, `description`, `metadata.group/origin`)와
  디렉터리명, 허용되지 않은 frontmatter 키, `description`의 한글 포함 여부
- 중앙 루트·스킬 디렉터리·어댑터 경로가 심볼릭 링크인지 여부
- 누락되거나 오래된 Claude 어댑터, 삭제된 중앙 스킬에서 남은 어댑터,
  `.claude/skills`에 수동으로 작성된 `SKILL.md`
- `CATALOG.md`와 `skills.lock`이 현재 스킬 내용과 일치하는지(드리프트)
- `_notes` 작업 문서의 파일명 규칙 `<yymmdd-hhmm>-<topic-slug>.md`

GitHub Actions의 `validate-skills.yml`은 같은 검사와 테스트를 Ubuntu와 Windows에서,
Python 최소 지원 버전 `3.10`과 최신 `3.x`로 실행합니다.

### 해시와 로컬 생성물

PNG를 포함한 정적 에셋은 Git·업데이트·해시 대상입니다. 스킬 내부의 로컬 미리보기는
`_generated/` 폴더에 출력하세요. `.venv`, 캐시, `_generated` 등 제외 디렉터리는
순회하지 않으며 복사·삭제하지 않습니다. 그 밖의 경로에서 symlink나 Windows reparse
point가 발견되면 거부합니다. 파일과 디렉터리가 서로 충돌하는 갱신도 사전에 거부합니다.

해시는 파일을 POSIX 경로의 바이트 순서로 정렬해 계산하므로 대소문자를 구분하지 않는
파일시스템에서도 같은 값이 나옵니다. UTF-8 텍스트로 확인된 다음 형식의 CRLF/CR은
LF로 정규화합니다. `md`, `txt`, `py`, `sh`, `ps1`, `json`, `yaml`, `yml`, `toml`, `lock`,
`html`, `css`, `js`, `ts`, `svg` 및 `.gitignore`, `.gitattributes`, `.editorconfig`입니다.
디코딩할 수 없거나 NUL이 포함된 파일, 다른 확장자와 바이너리는 원시 바이트를 사용합니다.
정규화는 해싱에만 적용하며 원본 파일을 재작성하지 않습니다. 이전 해시 규칙의 lock은
한 번 sync하여 갱신해야 할 수 있습니다.

## 운영 원칙

- 실제 지침, 스크립트, 참고 문서, 에셋은 모두 `.agents/skills/<skill-name>/`
  아래에 둡니다. 실행 코드와 환경 파일은 `scripts/`, 문서는 `references/`에 둡니다.
- `.claude/skills`에는 생성된 어댑터 외의 스킬을 두지 않습니다.
- 요구사항 인터뷰·결정 기록은 `_notes/grills`, 작업·리뷰 지침서는 수신 대상에 따라
  `_notes/handoffs/to_codex`, `to_claude`, `to_human`에 저장합니다.
- 개인 설정과 자격 증명은 커밋하지 않습니다.
- 하네스별 고유 기능을 사용하면 다른 하네스에서 무시되거나 다르게 작동할 수
  있으므로, 공용 스킬은 기본 `name`/`description`과 Markdown 지침을 중심으로
  작성합니다.
- Claude Code 전용 `$ARGUMENTS`, 명령 주입, 컨텍스트 옵션은 중앙 본문에서 직접
  실행되지 않습니다. 공용 스킬 본문은 하네스 독립적인 파일 읽기와 일반 지침을
  사용합니다.
