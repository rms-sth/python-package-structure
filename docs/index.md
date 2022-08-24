# `my_module` User Guide

!!! info

    This user guide is purely an illustrative example that shows off several features of 
    [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) and included Markdown
    extensions.

## Installation

First, [install Poetry](https://python-poetry.org/docs/#installation):

=== "Linux/macOS"

    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```

=== "Windows"

    ```powershell
    (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
    ```

Then install the `my_module` package and its dependencies:

```bash
poetry install
```

Activate the virtual environment created automatically by Poetry:

```bash
poetry shell
```

## Quick Start

To use `my_module` within your project, import the `factorial` function and execute it like:

```python
from my_module.libs.tasks import create_tasks

assert create_tasks() is True
```
