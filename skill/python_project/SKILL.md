---
name: python_project
description: Use when creating a new Python project, package or command-line script, or when adding a pyproject.toml, an entry point or a CLI to existing Python code. Applies the user's skeleton - pyproject.toml (setuptools) + jsonargparse CLI, editable install.
---

# Python project skeleton

Follow this skeleton when creating or structuring a Python project. Adapt names, keep the shape.

## Rules

- Packaging: a single `pyproject.toml` (setuptools backend). No `setup.py`, no `setup.cfg`, no `requirements.txt` unless asked.
- CLI: `jsonargparse.CLI` on a typed function (or class). Never `argparse`, `click` or `sys.argv` parsing.
- Every command is exposed through `[project.scripts]`, pointing to a `main()` function.
- Project and package names use underscores, never hyphens (`my_tool`, not `my-tool`).
- Install for development with `python -m pip install -e .`.

## File structure

```
my_project/
├── pyproject.toml
└── my_package/
    ├── __init__.py
    ├── greetings.py      # CLI module: typed function + main()
    └── core.py           # logic, importable without the CLI
```

## pyproject.toml

```toml
[build-system]
requires = ["setuptools", "setuptools-scm"]
build-backend = "setuptools.build_meta"

[project]
name = "my_project"
version = "1.0.0"
dependencies = ["jsonargparse"]

[project.scripts]
greetings = "my_package.greetings:main"
```

If the project root holds more than one top-level directory (tests, data, samples, ...), setuptools fails with
`error: Multiple top-level packages discovered in a flat-layout`. Then list the packages explicitly:

```toml
[tool.setuptools]
packages = ["my_package"]

[tool.setuptools.package_data]
"my_package" = ["*.png"]
```

## CLI module with jsonargparse

`CLI` builds the arguments from the function signature: type hints give types, defaults make arguments optional,
the docstring gives the help text.

```python
from jsonargparse import CLI


def greetings(name: str, polite: bool = False):
    """Greet someone.

    Args:
        name: who to greet.
        polite: use a formal greeting.
    """
    print(f"{'Good day' if polite else 'Hello'}, {name}.")


def main():
    CLI(greetings)


if __name__ == '__main__':
    main()
```

```
$ greetings Friend
Hello, Friend.
$ greetings --help
```

Keep the logic in plain functions (`core.py`); the CLI function only wires arguments to them.

### Short aliases (`-n` for `--name`)

jsonargparse has no built-in short aliases (see omni-us/jsonargparse#840). Use a parser subclass.
The argument must have a default value to become an option (`--name`) instead of a positional.

```python
from jsonargparse import CLI, ArgumentParser


def greetings(name: str = ''):
    print(f'Il mio nome è {name}.')


class AliasingParser(ArgumentParser):
    def add_argument(self, *args, **kwargs):
        if args == ('--name',):
            args += ('-n',)
        return super().add_argument(*args, **kwargs)


def main():
    CLI(greetings, parser_class=AliasingParser)


if __name__ == '__main__':
    main()
```

```
$ greetings -n Nessuno
Il mio nome è Nessuno.
```

## Install

```bash
python -m venv .venv              # optional
source .venv/bin/activate         # Windows: .venv\Scripts\activate
python -m pip install -e .        # . = directory containing pyproject.toml
```
