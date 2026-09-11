# 저장소 규약

## 개발 명령

[uv](https://docs.astral.sh/uv/)가 Python 버전(`.python-version`)과 의존성(`uv.lock`)을
관리합니다. 다른 도구는 설치할 필요가 없습니다.

| 작업 | 명령 |
| --- | --- |
| 환경 생성·동기화 | `uv sync` |
| 린트 / 포맷 | `uv run ruff check .` / `uv run ruff format .` |
| 테스트 | `uv run pytest` |
| 커밋 훅 설치 | `uv run pre-commit install` |
| 훅 전체 실행 | `uv run pre-commit run --all-files` |
| 의존성 추가 | `uv add <package>` (개발용은 `uv add --group dev <package>`) |

`uv.lock`은 `pyproject.toml`과 함께 커밋합니다. `pyproject.toml`의 ruff 설정은
`.agents/`, `.claude/`, `_notes/`를 제외하므로 공용 스킬 파일은 포맷되지 않습니다.

## 커밋 훅

`.pre-commit-config.yaml`은 기본 정리 훅(줄 끝, 개행, YAML/TOML 문법, 대용량 파일),
ruff 검사·포맷, 그리고 `scripts/sync_skills.py --check`를 실행합니다. 스킬을 바꾸고
생성물을 갱신하지 않으면 커밋이 막힙니다.

## CI

- **CI** (`.github/workflows/ci.yml`): `main` push와 PR마다 ruff 검사·포맷 확인,
  Ubuntu/Windows × Python 3.10/3.12에서 pytest를 실행합니다. `uv sync --locked`를 쓰므로
  `uv.lock`이 `pyproject.toml`과 어긋나면 실패합니다.
- **Validate shared skills** (`.github/workflows/validate-skills.yml`): 스킬·작업 기록·
  스킬 도구 경로가 바뀔 때만 실행됩니다. 프로젝트 의존성 없이 시스템 Python만으로
  스킬 도구 테스트와 `sync_skills.py --check`를 Ubuntu/Windows에서 돌립니다.
- **Dependabot**: GitHub Actions와 uv 개발 의존성을 매월 묶음 PR로 갱신합니다.

## 작업 기록

에이전트가 작성하는 요구사항 인터뷰(`grill-me`)와 인계 지침서(`handoff`)는 `_notes/`
아래에 `<yymmdd-hhmm>-<topic-slug>.md`로 저장합니다. 각 폴더의 `README.md`만 커밋하고
나머지는 로컬에 남습니다. 규칙은 [_notes/README.md](../_notes/README.md)를 보세요.

## 문서 언어

에이전트가 읽는 파일(`AGENTS.md`, 스킬)은 영어로, 사람이 읽는 안내(`README.md`, `docs/`,
`_notes/**/README.md`)는 한국어로 씁니다.
