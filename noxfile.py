from pathlib import Path
from tempfile import NamedTemporaryFile

import nox
from nox_poetry import Session, session

nox.options.error_on_external_run = True
nox.options.reuse_existing_virtualenvs = True
nox.options.sessions = ["fmt_check", "lint", "type_check", "test", "docs"]


@session(python=["3.10"])
def test(s: Session) -> None:
    s.install(".", "pytest", "pytest-cov")
    s.run(
        "python",
        "-m",
        "pytest",
        "--cov=my_module",
        "--cov-report=html",
        "--cov-report=term",
        "tests",
        *s.posargs,
    )


# For some sessions, set venv_backend="none" to simply execute scripts within the existing Poetry
# environment. This requires that nox is run within `poetry shell` or using `poetry run nox ...`.
@session(venv_backend="none")
def fmt(s: Session) -> None:
    s.run("isort", ".")
    s.run("black", ".")


@session(venv_backend="none")
def fmt_check(s: Session) -> None:
    s.run("isort", "--check", ".")
    s.run("black", "--check", ".")


@session(venv_backend="none")
def lint(s: Session) -> None:
    # Run pyproject-flake8 entrypoint to support reading configuration from pyproject.toml.
    s.run("pflake8")


@session(venv_backend="none")
def type_check(s: Session) -> None:
    s.run("mypy", "src", "tests", "noxfile.py")


# Environment variable needed for mkdocstrings-python to locate source files.
doc_env = {"PYTHONPATH": "src"}


@session(venv_backend="none")
def docs(s: Session) -> None:
    s.run("mkdocs", "build", env=doc_env)


@session(venv_backend="none")
def docs_serve(s: Session) -> None:
    s.run("mkdocs", "serve", env=doc_env)


# # this will be replaced by github action or invoke task.
# @session(venv_backend="none")
# def docs_github_pages(s: Session) -> None:
#     s.run("mkdocs", "gh-deploy", "--force", env=doc_env)


# # this will be replaced  by github action.
# @session(venv_backend="none")
# def docs_github_pages(s: Session) -> None:
#     latest_tag = subprocess.check_output(
#         "git describe --tags `git rev-list --tags --max-count=1`", shell=True
#     )
#     latest_tag = latest_tag.decode("utf-8").split("\n")[0]
#     # s.run("mkdocs", "gh-deploy", "--force", env=doc_env)
#     # latest_tag = subprocess.call(
#     #     f"mike deploy --push --update-aliases {latest_tag} latest",
#     #     shell=True,
#     # )
#     s.run("mike", "deploy", "--push", "--update-aliases", "{latest_tag}", "latest", env=doc_env)


# Note: This reuse_venv does not yet have affect due to:
#   https://github.com/wntrblm/nox/issues/488
@session(reuse_venv=False)
def licenses(s: Session) -> None:
    # Generate a unique temporary file name. Poetry cannot write to the temp file directly on
    # Windows, so only use the name and allow Poetry to re-create it.
    with NamedTemporaryFile() as t:
        requirements_file = Path(t.name)

    # Install dependencies without installing the package itself:
    #   https://github.com/cjolowicz/nox-poetry/issues/680
    s.run_always(
        "poetry",
        "export",
        "--without-hashes",
        f"--output={requirements_file}",
        external=True,
    )
    s.install("pip-licenses", "-r", str(requirements_file))
    s.run("pip-licenses", *s.posargs)
    requirements_file.unlink()
