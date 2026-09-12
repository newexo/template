# Template

This repository provides a minimal, opinionated starting point for creating new Python packages managed with Poetry. Its primary purpose is to offer a clean, lightweight structure that can be copied and adapted when beginning a new project, so that common configuration and layout decisions do not need to be repeated each time. The project defines a single top-level Python package named `template`, along with a corresponding `pyproject.toml` file that records package metadata, runtime requirements and development dependencies, and a small set of auxiliary files (such as data and test resources) intended to illustrate how such assets can be bundled with a package.

The repository is designed to support a typical modern Python workflow in which Poetry handles dependency management and packaging. It provides a dev group for testing and code quality (Pytest, Ruff, coverage, Vulture, deptry), installed by default, and an optional notebook group for interactive development and visualization (Jupyter, Matplotlib, Seaborn). It is not intended as a functional library in its own right; instead, it serves as a scaffold that can be renamed, extended and customized to match the needs of a specific project, ensuring that new packages begin from a consistent and well-structured baseline.

## Cloning the Template Repository

The template is hosted at
[https://github.com/newexo/template](https://github.com/newexo/template)
and is organized around a single default branch named `template`. To begin working with the repository, clone it to a local workstation using standard Git operations:

```bash
git clone https://github.com/newexo/template.git
cd template
```

This command retrieves the full contents of the repository and enters the project directory, providing a local copy of the template from which further modifications and project-specific development may proceed.

## Creating a New GitHub Repository and Pushing the Template

After cloning the template, the next step is to establish a new GitHub repository that will serve as the home for the project under development. This should be an empty repository created through the GitHub interface, without initialization files such as a README, license or `.gitignore`. An empty repository ensures that the initial push from the template proceeds without conflicts.

Once the new repository has been created, obtain its clone URL from the GitHub interface. With this URL in hand, the template can be transferred directly into the `main` branch of the new repository through a single Git command issued from within the local template directory:

```bash
git push <NEW_REPO_URL> template:main
```

This command pushes the local `template` branch to the `main` branch of the newly created repository, without altering or defining any Git remotes in the local clone. The new repository will then contain an exact duplicate of the template at the moment of the push.

## Cloning the Newly Created Project Repository

Once the template has been pushed to the `main` branch of the new GitHub repository, the local copy of the template has served its purpose. At this stage, it is advisable to work directly with the newly created repository rather than continuing within the original template directory. To do so, return to the parent directory, clone the new repository and enter its working directory:

```bash
cd ..
git clone <NEW_REPO_URL>
cd <NEW_REPO_NAME>
```

This procedure creates a clean working environment that reflects the state of the project as hosted on GitHub. All subsequent development should be performed within this freshly cloned repository, which now constitutes the canonical version of the project.

## Refactoring the Package Name in the New Repository

The template includes a single top-level Python package named `template`, which is intended as a placeholder rather than a permanent project identifier. After cloning the new repository, the next step is to refactor this package to reflect the actual name of the project. This process involves renaming both the directory that defines the package and any internal references to it.

The directory structure contains a folder named `template/` that serves as the importable package. This folder should be renamed to the project’s chosen package name. Most modern development environments provide tools for performing such renaming operations safely; however, these tools typically operate only on file paths and import statements. They do not automatically update configuration files.

In particular, the `pyproject.toml` file must be edited manually. The name
appears in two places. The distribution name lives under `[project]`:

```toml
[project]
name = "myproject"
```

and the importable package under `[tool.poetry]`:

```toml
[tool.poetry]
packages = [{ include = "myproject" }]
```

**Keep these two identical, and use underscores rather than hyphens.** PEP 621
permits a hyphenated distribution name, and `poetry new` generates one by
default, but the Makefile reads the distribution name and uses it as both a
coverage target and a directory path. A mismatch is not subtle — coverage
collapses to 0% and `make coverage` fails against its threshold — but keeping the
names identical avoids the problem entirely.

Failure to update the `packages` field will lead Poetry to search for a package
that no longer exists, resulting in installation errors or misconfigured
distributions. Inspect `pyproject.toml` carefully after refactoring, ensuring
every reference to `template` has been replaced.

## Creating a Development Environment and Installing Dependencies

Create an isolated Python environment before installing project dependencies. This prevents conflicts with system packages and keeps development reproducible. You may use `venv`, Conda or pyenv.

### Using venv

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install poetry
```

### Using Conda

```bash
conda create -n <ENV_NAME> python=3.11
conda activate <ENV_NAME>
pip install poetry
```

### Using pyenv

```bash
pyenv install 3.11
pyenv virtualenv 3.11 <ENV_NAME>
pyenv activate <ENV_NAME>
pip install poetry
```

### Installing Project Dependencies

After you activate the environment, install project dependencies using Poetry. The project defines two dependency groups:

**dev group**: Testing and code quality tools (pytest, ruff, coverage, vulture, deptry). Installed by default, because a fresh clone should be able to run `make check` immediately.

**notebook group**: Interactive development and visualization tools (jupyter, jupyterlab, matplotlib, seaborn). Marked `optional = true`, so it is installed only when asked for.

Install the runtime and dev dependencies:

```bash
poetry install
```

Add the notebook group when you need Jupyter or plotting:

```bash
poetry install --with notebook
```

Install runtime dependencies alone, without dev tooling:

```bash
poetry install --only main
```

A group is excluded from the default install only if it is declared
`optional = true` in `pyproject.toml`:

```toml
[tool.poetry.group.notebook]
optional = true

[tool.poetry.group.notebook.dependencies]
...
```

Without that stanza the group installs with every `poetry install`, and
`--with <group>` has no effect. Declare any heavy or situational group optional.

## Overview of the Project Structure

The project uses a standard layout for a Poetry-based Python package. The top-level directory contains the source package, its tests, supporting data, notebooks and the configuration files that define the development workflow. A typical structure is:

```
<PROJECT_ROOT>/
    <PACKAGE_NAME>/           # Main Python package
        __init__.py
        _version.py
        directories.py
        py.typed              # Marks the package as typed for consumers
        tests/
            test_directories.py
            test_example.py
            test_version.py
            test_data/
                ...
    data/                     # Repository-level data; sdist only, never a wheel
    notebooks/                # Jupyter notebooks for exploration or documentation
    scripts/                  # Development tooling and entry-point scripts
        import_boundaries.py
    .github/
        workflows/            # Continuous integration
        dependabot.yml        # Automated dependency updates
    pyproject.toml            # Project metadata, dependencies and tool config
    poetry.lock               # Dependency lockfile
    Makefile                  # Commands for formatting, linting, testing and coverage
    README.md                 # Project documentation
    LICENSE                   # Project license
```

The package directory sits at the repository root rather than under `src/`.
Recent versions of `poetry new` generate a `src/` layout; this template does not
follow that, because the package directory is where the tests live and a flat
layout keeps existing projects from having to relocate it. Note the consequence:
from the repository root, `import <PACKAGE_NAME>` resolves to the source tree
even when the package is also installed. `make test-wheel` changes directory
before running precisely to avoid that.

Running `make coverage-html` creates a directory named `htmlcov` in the project root. This directory contains an HTML report that summarizes test coverage and supports interactive inspection. Git usually ignores this directory because it serves only local development needs.

This structure separates the importable package from its tests and from supplementary materials. The `pyproject.toml` file defines all project metadata and dependencies. The Makefile provides a consistent interface for checks that support development quality, and the tests in the package directory help maintain correctness throughout the project lifecycle.

## Versioning and Package Initialization

The package exposes its version through variables defined in `__init__.py` and `_version.py`. After you rename the package, update both files to use the new package name.

In `__init__.py`, update the import:

```python
from <PACKAGE_NAME>._version import __version__
```

In `_version.py`, update the metadata lookup so that it matches the new package name:

```python
import importlib.metadata

__version__ = importlib.metadata.version("<PACKAGE_NAME>")
```

These changes ensure that the package defines a correct `__version__` attribute and that the metadata lookup succeeds after renaming.

## Directory Resolution Utilities

The template includes a module named `directories.py` that centralizes the logic for resolving absolute paths to important project locations. Rather than assembling paths manually or relying on assumptions about the current working directory, the module provides functions that locate the package directory, the project root, the data directories and the test directories. Each function returns a `pathlib.Path` — either the directory itself, or a fully qualified path when given a filename.

### Two kinds of data directory

Where data belongs depends on the project, so the module addresses both cases
and neither is the default:

| Function | Resolves to | Ships in a wheel | Use for |
|---|---|---|---|
| `directories.data()` | `<repo>/data/` | No | Data that must never be packaged: large files, private material, generated output |
| `directories.package_data()` | `<package>/data/` | Yes | Reference data that belongs to the library and must be readable after installation |

Poetry copies only files inside the package directory into a wheel. A repository-level
`data/` directory can reach a source distribution through `include` in
`pyproject.toml`, but never a wheel. Consequently `directories.data()` and
`directories.base()` are meaningful in a source checkout and not in an installed
package; if your code must read its data after `pip install`, put that data in
`<package>/data/` and reach it with `directories.package_data()`.

### Example Usage

The following example illustrates how to import the module and construct the absolute path to a file located in the project’s `data/` directory:

```python
from <PACKAGE_NAME> import directories

# Construct the path to a file named "example.csv" inside the data directory
filepath = directories.data("example.csv")

with open(filepath, "r") as f:
    contents = f.read()

print(contents)
```

This pattern avoids hard-coded paths and ensures that file resolution remains consistent regardless of the user’s current working directory or the environment in which the code is executed.

## Import Conventions

Imports belong at the top of the module. Two situations justify departing from
that, and each has one correct form.

### Default

All imports at module top, grouped standard library, third-party, first-party.
Ruff enforces placement and ordering; `make format` sorts them.

### Optional dependencies

A package declared in an optional dependency group may be absent at runtime.
Import it at the top inside a guard and fail at the point of use, naming the
group to install:

```python
try:
    import yaml
except ImportError:
    yaml = None


def load(path):
    if yaml is None:
        raise RuntimeError("pyyaml required: poetry install --with <group>")
```

This keeps every dependency visible in one place at the top of the file.

### Expensive imports

Defer an import into the function that needs it only when the module is slow to
import and is needed on some code paths but not others. Measure before deciding:

```bash
python -X importtime -c "import mlflow" 2>&1 | tail -1
```

Representative costs, for calibration:

```
pathlib, json        4-5 ms
yaml, dotenv        15-17 ms
bs4                    55 ms
matplotlib            108 ms
pdfplumber            158 ms
seaborn               546 ms
mlflow               1918 ms
```

Below 100 ms, import at the top regardless. At or above 100 ms, defer only if
the code path is conditional, and give the reason inline:

```python
def log_run(metrics):
    import mlflow  # deferred: ~1.9 s import, only used when tracking is on
```

### Both optional and expensive

Defer, and convert the `ImportError` into a message naming the group:

```python
def convert(path):
    try:
        from docling.document_converter import DocumentConverter
    except ImportError as exc:
        raise RuntimeError("docling required: poetry install --with docling") from exc
```

### Not acceptable

- Deferring an import to work around a circular import. Fix the cycle instead.
- Deferring standard library or inexpensive imports.
- Suppressing placement warnings rather than using one of the forms above.

### Isolate optional dependencies behind a boundary

A conditional import is a cost, not a solution. Before writing one, ask whether
the dependency belongs behind an interface.

An optional dependency should be imported by exactly one library module. That
module owns the dependency: it defines the interface the rest of the code
depends on, implements that interface, and exposes a factory. Callers receive an
implementation by injection and never import the dependency themselves.

```python
# providers.py -- the only module that imports any model SDK
class LLMProvider(Protocol):
    def generate(self, prompt: str) -> str: ...


class AnthropicProvider(BaseLLMProvider):
    def _client(self):
        import anthropic  # optional dependency, owned here

        return anthropic.Anthropic(...)


def create_provider(config) -> LLMProvider: ...


# every other module
def summarise(text, provider: LLMProvider):
    return provider.generate(text)
```

`make import-boundaries` enforces this. It checks only packages declared in
groups marked `optional = true` — core dependencies are deliberately out of
scope, since spreading `pandas` across ten modules is normal while spreading an
optional service client across ten modules is a missing boundary. Entry points
(`main.py`, `cli.py`, `__main__.py`, `app.py`, and the `scripts/`, `bin/` and
`notebooks/` directories) are exempt, because wiring implementations together is
what an entry point is for.

When a boundary already exists and callers bypass it, route them through it
rather than adding another guarded import.

### Declaration follows use

If library source imports a package, it must be declared as a runtime dependency
or in an optional group — never as a development dependency. `make deps-check`
verifies this.

## Testing the Built Package

The wheel ships the test suite, so the installed package can be verified rather
than only the source tree:

```bash
make test-wheel
```

This builds a wheel, installs it into a throwaway virtualenv, and runs
`pytest --pyargs <PACKAGE_NAME>.tests` from outside the repository. Tests that
assert on repository layout (`base()`, `data()`) detect that they are not running
from a checkout and skip. Continuous integration runs this on every push, which
catches packaging mistakes that a source-tree test run cannot see.

## Dead Code and Dependency Hygiene

```bash
make deadcode     # unused functions, classes, variables, unreachable code
make deps-check   # imported but undeclared, or declared in the wrong group
```

`make deadcode` is advisory rather than a gate. A library's public API is
uncalled by construction, so Vulture reports it as dead; read the output rather
than trusting it.

For a project that already carries dead code, baseline it once:

```bash
make deadcode-baseline
```

Commit the resulting `deadcode-whitelist.py`. `make deadcode` picks it up
automatically once it exists, so existing dead code stops blocking work while
newly dead code still surfaces.

Use the target rather than running Vulture by hand: it tolerates Vulture's exit
code 3, and it formats the output, which otherwise ends with a trailing blank
line that `ruff format --check` rejects.

## Makefile-Based Workflow

The Makefile provides a simple interface for common development tasks and runs all tools inside the Poetry environment. After you create and activate a development environment and install dependencies, issue the following commands from the project root:

| Command                  | Description                                                        |
|--------------------------|--------------------------------------------------------------------|
| `make test`              | Run the test suite.                                                |
| `make format`            | Apply safe lint fixes, then format, with Ruff.                     |
| `make format-check`      | Verify formatting without rewriting files. Used by CI.             |
| `make lint`              | Run Ruff lint checks.                                              |
| `make check`             | Formatting check, lint and tests. Does not modify files.           |
| `make coverage`          | Run tests with coverage enforcement.                               |
| `make coverage-html`     | Create an HTML coverage report.                                    |
| `make import-boundaries` | Verify optional dependencies stay isolated behind one module.      |
| `make deps-check`        | Verify imported packages are declared, and in the right group.     |
| `make deadcode`          | Report unused code. Advisory, not a gate.                          |
| `make deadcode-baseline` | Baseline existing dead code so only new dead code surfaces.        |
| `make test-wheel`        | Build a wheel and run the shipped tests against the installed one. |

`make check` deliberately does not reformat. Run `make format` to fix what is
fixable, then `make check` to verify.

These commands support routine quality checks and keep the workflow consistent across local development and continuous integration.

The coverage threshold is defined in the Makefile. Projects should adjust this value to reflect their own testing standards.
