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

After you activate the environment, install all project and development dependencies:

```bash
poetry install --with dev
```

This command configures the environment for development, testing and further extension of the project.

## Overview of the Project Structure

The project uses a standard layout for a Poetry-based Python package. The top-level directory contains the source package, its tests, supporting data, notebooks and the configuration files that define the development workflow. A typical structure is:

```
<PROJECT_ROOT>/
    <PACKAGE_NAME>/           # Main Python package
        __init__.py
        _version.py
        directories.py
        tests/
            test_directories.py
            test_example.py
            test_version.py
            test_data/
                ...
    data/                     # Optional data files included with the package
    notebooks/                # Jupyter notebooks for exploration or documentation
    pyproject.toml            # Poetry configuration
    poetry.lock               # Dependency lockfile
    Makefile                  # Commands for formatting, linting, testing and coverage
    README.md                 # Project documentation
    LICENSE                   # Project license
```

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

The Makefile provides a simple interface for common development tasks and runs all tools inside the Poetry environment. After you create and activate a development environment and install dependencies, issue the following commands from the project root:

| Command              | Description                          |
|----------------------|--------------------------------------|
| `make test`          | Run the test suite.                  |
| `make format`        | Format the code with Black.          |
| `make lint`          | Run Flake8 checks.                   |
| `make check`         | Run formatting, linting and tests.   |
| `make coverage`      | Run tests with coverage enforcement. |
| `make coverage-html` | Create an HTML coverage report.      |

These commands support routine quality checks and keep the workflow consistent across local development and continuous integration.

The coverage threshold is defined in the Makefile. Projects should adjust this value to reflect their own testing standards.
