# project-template

Project description.

<!-- template-only:start -->
> **이 저장소는 GitHub Template입니다.** Python 프로젝트 골격(uv, ruff, pytest,
> pre-commit, CI)과 Codex·Claude Code 공용 스킬셋이 준비되어 있습니다.
> **Use this template**로 저장소를 만든 뒤 한 번만 초기화하세요.
>
> ```shell
> python3 scripts/bootstrap_template.py my-project --description "한 줄 설명"
> ```
>
> 패키지 이름과 자리표시자를 치환하고 이 안내를 지운 뒤 스크립트는 스스로 삭제됩니다.
> 마지막으로 저장소 Settings에서 브랜치 보호와 필수 체크를 켜면 됩니다.
<!-- template-only:end -->

## 시작하기

```shell
uv sync                     # Python 환경과 의존성
uv run pre-commit install   # 커밋 훅
uv run pytest               # 테스트
```

린트와 포맷은 `uv run ruff check .`와 `uv run ruff format .`입니다.

## 구조

- `src/project_template/`: 패키지 코드
- `tests/`: pytest 테스트
- `scripts/`: 스킬 동기화·갱신 도구
- `.agents/skills/`: Codex·Claude Code 공용 스킬 원본
- `_notes/`: 에이전트 작업 기록 (README만 커밋)
- `docs/`: 상세 문서

## 더 읽기

- [docs/conventions.md](docs/conventions.md): 개발 명령, CI, 커밋 훅, 작업 기록, 문서 언어
- [docs/skills-tooling.md](docs/skills-tooling.md): 스킬 추가·갱신·검증
- [AGENTS.md](AGENTS.md): 에이전트가 따르는 저장소 지침
