"""Check that optional dependencies stay behind a boundary.

An optional dependency should be imported by at most one library module. That
module owns the dependency: it defines the interface the rest of the code uses,
implements it, and hands out instances. Everything else receives an
implementation by injection and never imports the dependency itself.

Scope is taken from the project's own declaration -- only packages in Poetry
groups marked `optional = true` are checked. Core dependencies are deliberately
out of scope: spreading pandas across ten modules is normal, spreading an
optional service client across ten modules is a missing boundary.

Entry points are exempt. Wiring concrete implementations together is what an
entry point is for.

Usage:  python scripts/import_boundaries.py [project_root]
Exit:   0 if every optional dependency is isolated, 1 otherwise.
"""

import ast
import os
import sys
import tomllib
from collections import defaultdict

ENTRY_FILES = ("main.py", "cli.py", "__main__.py", "app.py")
ENTRY_DIRS = ("scripts", "bin", "notebooks")

# Distribution name -> module name, where they differ.
ALIASES = {
    "beautifulsoup4": "bs4",
    "opencv-python": "cv2",
    "pillow": "PIL",
    "python-dotenv": "dotenv",
    "pyyaml": "yaml",
    "scikit-learn": "sklearn",
}


def module_name(distribution):
    key = distribution.lower()
    return ALIASES.get(key, key.replace("-", "_"))


def is_entry_point(relative_path):
    parts = relative_path.split(os.sep)
    return os.path.basename(relative_path) in ENTRY_FILES or parts[0] in ENTRY_DIRS


def optional_dependencies(root):
    with open(os.path.join(root, "pyproject.toml"), "rb") as handle:
        config = tomllib.load(handle)
    groups = config.get("tool", {}).get("poetry", {}).get("group", {})
    names = set()
    for group in groups.values():
        if not group.get("optional"):
            continue
        for distribution in group.get("dependencies", {}):
            if distribution != "python":
                names.add(module_name(distribution))
    return names


def imported_modules(path):
    try:
        with open(path, encoding="utf-8") as handle:
            tree = ast.parse(handle.read())
    except (OSError, SyntaxError):
        return
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                yield alias.name.split(".")[0]
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            yield node.module.split(".")[0]


def source_files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith((".", "__"))]
        for filename in filenames:
            if not filename.endswith(".py"):
                continue
            full = os.path.join(dirpath, filename)
            relative = os.path.relpath(full, root)
            if "tests" in relative.split(os.sep):
                continue
            yield full, relative


def check(root):
    watched = optional_dependencies(root)
    if not watched:
        print("No optional dependency groups declared; nothing to check.")
        return 0

    importers = defaultdict(lambda: {"library": set(), "entry": set()})
    for full, relative in source_files(root):
        for module in imported_modules(full):
            if module in watched:
                key = "entry" if is_entry_point(relative) else "library"
                importers[module][key].add(relative)

    violations = 0
    for module in sorted(watched):
        sites = importers[module]
        library = sorted(sites["library"])
        entry = sorted(sites["entry"])
        if len(library) <= 1:
            print(
                f"ok    {module}: {len(library)} library module, "
                f"{len(entry)} entry point(s)"
            )
            continue
        violations += 1
        print(f"LEAK  {module}: imported by {len(library)} library modules")
        for path in library:
            print(f"        {path}")

    if violations:
        print(
            f"\n{violations} optional dependency/dependencies are not isolated.\n"
            "Put the dependency behind one module that owns it and inject the\n"
            "result, or declare it non-optional if it is genuinely core."
        )
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(check(sys.argv[1] if len(sys.argv) > 1 else "."))
