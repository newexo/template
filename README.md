# Template

This repository provides a minimal, opinionated starting point for creating new Python packages managed with Poetry. Its primary purpose is to offer a clean, lightweight structure that can be copied and adapted when beginning a new project, so that common configuration and layout decisions do not need to be repeated each time. The project defines a single top-level Python package named `template`, along with a corresponding `pyproject.toml` file that records package metadata, runtime requirements and development dependencies, and a small set of auxiliary files (such as data and test resources) intended to illustrate how such assets can be bundled with a package.

The repository is designed to support a typical modern Python workflow in which Poetry handles dependency management and packaging, while auxiliary tools such as Pytest, Black, Flake8, Jupyter, Matplotlib and Seaborn are used for testing, formatting, linting and exploratory analysis. It is not intended as a functional library in its own right; instead, it serves as a scaffold that can be renamed, extended and customized to match the needs of a specific project, ensuring that new packages begin from a consistent and well-structured baseline.

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

In particular, the `pyproject.toml` file must be edited manually to ensure that the package reference is consistent with the new name. The relevant portion of the file appears under the `[tool.poetry]` section:

```toml
packages = [{ include = "template" }]
```

If the package is renamed, for example, to `myproject`, this line must be updated accordingly:

```toml
packages = [{ include = "myproject" }]
```

Failure to update this field will lead Poetry to search for a package that no longer exists, resulting in installation errors or misconfigured distributions. Users should therefore inspect the `pyproject.toml` carefully after refactoring the package name, ensuring that all references to `template` have been replaced with the selected project name.

## Creating a Development Environment and Installing Dependencies

Once the repository has been refactored to reflect the new project name, development should proceed within an isolated Python environment. An isolated environment prevents conflicts with system-level packages and ensures that dependencies specified in the `pyproject.toml` are installed in a controlled and reproducible manner. Several environment managers may be used for this purpose, and the choice depends on the user’s preferred workflow.

### Using `venv`

Python’s built-in `venv` module provides a minimal, lightweight method for creating an isolated environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install poetry
```

After activation, installing Poetry inside the environment ensures that all subsequent dependency management remains isolated within the project.

### Using Conda

Users who prefer Conda may create an environment with a specified Python version and then install Poetry within it:

```bash
conda create -n <ENV_NAME> python=3.11
conda activate <ENV_NAME>
pip install poetry
```

### Installing Project Dependencies

After activating the environment—whether created with `venv` or Conda—dependencies for the new project, including development dependencies, may be installed with a single command:

```bash
poetry install --with dev
```

Poetry will resolve the dependency graph specified in the `pyproject.toml` and populate the environment accordingly. Once completed, the environment is fully prepared for development, testing and further extension of the project.

## Overview of the Resulting Project Structure

Once the repository has been cloned, renamed and configured within an isolated environment, the project assumes the form of a standard, Poetry-managed Python package. Although the specific directory names will reflect the chosen package name rather than the template placeholder, the overall structure remains consistent with conventional Python packaging practices. A representative layout appears as follows:

```
<PROJECT_ROOT>/
    <PACKAGE_NAME>/           # Main Python package (renamed from "template")
        __init__.py
        _version.py
        directories.py
        tests/
            test_directories.py
            test_example.py
            test_version.py
            test_data/
                ...
    data/                      # Optional data files distributed with the package
    notebooks/                 # Jupyter notebooks or exploratory computational work
    pyproject.toml             # Poetry configuration and project metadata
    poetry.lock                # Resolved dependency lockfile
    README.md                  # Project documentation (to be customized)
    LICENSE                    # License for the new project
```

This structure separates the importable Python package from ancillary materials such as test suites, data files, notebooks and documentation. The `pyproject.toml` functions as the authoritative specification for dependencies and project metadata, while the `poetry.lock` file captures the fully resolved environment to promote reproducibility. The inclusion of a dedicated test directory supports test-driven or test-supported development from the outset, and the `data` and `notebooks` directories provide convenient locations for supplementary assets that often accompany scientific or exploratory work.

## Versioning and Package Initialization

The template includes a simple mechanism for exposing the project’s version number directly within the Python package. This mechanism relies on two small files—`__init__.py` and `_version.py`—that work together to retrieve the version declared in the project’s metadata. After refactoring the package name, it is essential to verify that these files correctly reference the new package rather than the original template name.

The `__init__.py` file imports the version string from the internal module:

```python
from template._version import __version__
```

After renaming the package directory, the reference to `template` in this import statement must be updated to match the new package name. Modern refactoring tools may or may not adjust this import automatically, so it should always be reviewed manually.

The `_version.py` file retrieves the project’s version from the package metadata recorded by Poetry:

```python
import importlib.metadata

__version__ = importlib.metadata.version("template")
```

The string `"template"` must likewise be replaced with the new package name. If this change is omitted, attempts to import the version or install the package will result in errors, because Python will search for metadata associated with a package that no longer exists.

## Directory Resolution Utilities

The template includes a module named `directories.py` that centralizes the logic for resolving absolute paths to important project locations. Rather than assembling paths manually with repeated calls to `os.path.join` or relying on assumptions about the current working directory, the module provides functions that locate the package directory, the project root, the `data/` directory and the test directories. Each function can return either the directory itself or a fully qualified path when given a filename.

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

## Makefile-Based Workflow

The repository includes a `Makefile` intended to streamline routine development tasks. All commands are executed through Poetry, ensuring that tests, formatting and linting run inside the project’s configured environment. The Makefile defines targets for running the test suite, formatting the codebase and checking code style.

Once the development environment has been created and dependencies installed, the following commands may be issued from the project root:

| Command       | Action Performed                                                   |
|---------------|--------------------------------------------------------------------|
| `make test`   | Runs the full test suite with Pytest using the Poetry environment. |
| `make format` | Applies Black formatting across the project source tree.           |
| `make lint`   | Executes Flake8 to perform static analysis and style checking.     |
| `make check`  | Runs formatting, linting and tests in sequence.                    |

These commands provide a concise interface for routine quality assurance. In practice, `make check` is the most comprehensive option, as it formats the code, evaluates style compliance and executes tests in a single step.

