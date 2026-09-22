# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pip install -e .

pytest                        # run the full suite
pytest tests/test_simulator.py           # run one test file
pytest tests/test_simulator.py::test_classic_kata_sequence   # run one test

python -m mars_rover --width 5 --height 5 --start-x 1 --start-y 2 --start-direction N LMLMLMLMM
# or, once installed: mars-rover --width 5 --height 5 --start-x 1 --start-y 2 --start-direction N LMLMLMLMM
```

There is no lint/format tooling configured in this repo (no ruff/black/flake8 config present).

## Architecture

The package (`mars_rover/`) is a small, immutable-value-object simulator with one file per concern:

- `direction.py` — `Direction` enum (N/E/S/W) plus pure functions `turn_left`, `turn_right`, `movement_delta`. No state.
- `planet_map.py` — `Position` (frozen dataclass, `x:y` string form) and `PlanetMap` (frozen dataclass with `width`/`height`, validates positive dimensions, exposes `is_within_bounds`).
- `rover.py` — `Rover` (frozen dataclass of `position` + `direction`) with methods that return *new* `Rover` instances (`turned_left`, `turned_right`, `moved_to`) rather than mutating state. `next_position()` computes where a move would land without applying it.
- `commands.py` — `Command` enum (`M`/`L`/`R`) and `parse_commands(raw: str) -> list[Command]`, raising `InvalidCommandError` on unknown letters.
- `simulator.py` — `run_mission(planet_map, rover, raw_commands) -> Rover`: the orchestration entry point. Parses commands, applies turns unconditionally, and for a move, checks bounds *before* moving, raising `OutOfBoundsError` (which carries the last valid `rover` and the rejected `attempted_position`) and leaving the rover's position untouched. **A rejected move aborts the whole mission** — it does not skip just that command and continue.
- `cli.py` / `__main__.py` — argparse-based CLI wrapper (`mars-rover` console script) around the library; converts library exceptions to a printed `Erreur : ...` message and exit code 1.

Everything is built around frozen dataclasses / enums and functions that return new values, so there's no hidden mutable state to track — each transformation step is a pure function from one immutable value to the next.

## Design workflow (intent → spec → build)

This repo uses a custom two-phase design process encoded as skills in `.claude/skills/`:

- `intent/` (`/intent`) drafts and validates `intent/<feature>/intent.md` — the problem, proposed outcome, users, and open questions — before any design work starts.
- `spec/` (`/spec <path-to-intent.md>`) turns an **accepted** intent (merged to `main`) into `intent/<feature>/spec.md`: numbered requirements (`EX-NN`) with scenarios, a proposed design, open reservations, and a generation-context section recording exactly which skill versions/commits were used. It never writes code or a build plan, and it never decides open questions on its own — it defers to the Product Owner and records their decisions with author/date/justification.

**Important:** `intent/mars-rover-simulator/spec.md` describes a target that the current `mars_rover/` implementation does not yet match. The accepted spec calls for a *web* interface (not a CLI), an obstacle-based map using emoji symbols (🟩/🌳 and 🟫/🪨, freely mixed), and blocked moves that leave the rover in place and **continue** executing the remaining commands rather than raising and aborting. The present code is a bounded rectangular map with no obstacles, a CLI, and `OutOfBoundsError` that aborts the mission on the first illegal move. When working on this codebase, check whether a change should follow the existing code's current behavior or the newer accepted spec, and don't assume the two agree.
