sync:
    uv self update
    uv sync -U --all-groups --all-extras

fix:
    uv run ruff format .
    uv run ruff check --fix --unsafe-fixes .

build:
    uv build

s: sync
f: fix
b: build
u: s f
