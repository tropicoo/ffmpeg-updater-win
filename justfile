sync:
    uv self update
    uv sync -U --all-groups --all-extras

check:
    ty check .
    pyrefly check

fix:
    uv run ruff format .
    uv run ruff check --fix --unsafe-fixes .

build:
    uv build

s: sync
c: check
f: fix
b: build
u: s f
