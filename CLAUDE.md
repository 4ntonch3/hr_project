# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```sh
# Install dependencies
pip install -r requirements.txt

# Run tests (requires PostgreSQL running)
pytest tests/

# Run a single test
pytest tests/path/to/test_file.py::test_function_name

# Lint and format checks (run all pre-commit hooks)
pre-commit run --all-files

# Apply ruff formatting
ruff format src/ tests/

# Start PostgreSQL via Docker
docker-compose up -d

# Apply migrations
python src/manage.py migrate

# Create user groups and permissions
python src/manage.py create_groups
```

## Architecture

This is a Django REST Framework project called **access_orchestrator** — a system that manages network access structures (Systems and Stands) by synchronizing them from an ELT (Extract-Load-Transform) data pipeline.

### Key data flow

1. External ELT process loads raw data into the `elt` app models (`ELTSystem`, `ELTStand`, `ELTDevice`, `FullELTVersion`).
2. `UpdateStructuresUseCase` (in `apps/network_access`) reads from the ELT models and upserts the canonical `System` and `Stand` models in `apps/network_access`.
3. `LoadObjectsUseCase` (in `apps/elt`) handles the initial ELT load phase.

### Apps

- **`apps/elt`** — raw ELT data: versioned snapshots of `ELTSystem`, `ELTStand`, `ELTDevice` tied to a `FullELTVersion`. Each entity has a `(ci, version)` unique constraint. `ELTStatus` tracks whether a version is ACTUAL / NOT_ACTUAL / UPDATE / ERROR.
- **`apps/network_access`** — canonical domain models: `System` (unique by `ci`) and `Stand` (unique by `ci`, FK to `System`). Stands store IPs as a PostgreSQL CIDR array via `netfields`.
- **`apps/users`** — custom `User` (extends `AbstractUser`) with a `Department` FK. Two groups (`STAND_ADMIN`, `ACCESS_ORCHESTRATOR_ADMIN`) with `get_network_interaction` / `create_network_interaction` permissions. `PermissionRequiredMixin` + `SimpleUserPermission` wires per-action permission checks onto DRF ViewSets.
- **`apps/core`** — shared utilities; currently only `BaseErrorSerializer`.

### Use cases

Use cases live under `apps/<app>/use_cases/<name>/app_layer/use_case.py` and expose a single `execute()` method. They are the only layer allowed to orchestrate cross-model logic.

### Settings

`access_orchestrator/settings/__init__.py` imports from `common.py` (and `drf.py`). The database is PostgreSQL (`test_database` / `test_app` / `123qwe` on localhost:5432 — matches `docker-compose.yml`). `DJANGO_SETTINGS_MODULE=access_orchestrator.settings` is set in `pytest.ini`.

### Testing

Tests are in `tests/` mirroring `apps/` structure. E2e tests use two pytest fixtures (`elt_objects`, `network_access_objects`) that accept dataclass containers of DTOs and persist them via repo helpers (`CreateELTObjectsRepo`, `CreateNetworkAccessObjectsRepo`). Test cases are declared as plain dicts and parametrized via `parametrize_from_dict`. Tests require a live PostgreSQL instance (no mocking of the DB layer).

### Linting

Two linters run in pre-commit:
- **ruff** — main linter + formatter (120 char line length, single quotes, all relative imports banned via `TID252`). Migrations excluded.
- **flake8** — checks class attribute ordering (`CCE`), complexity (`CCR`, `ECE`), and unused arguments (`U`). Tests and migrations excluded.

A `django-migrations --dry-run --check` hook blocks commits when migrations are missing.
