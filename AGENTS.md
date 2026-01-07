# AGENTS.md file

## Python Virtual Environment (venv)

The Python virtual environment for this repository is typically located in `.venv`.

## Formatting

Always format the code before commiting using, making sure that the Python code is properly formatted using:

```bash
pip install black
black .
```

## Testing

To run the custom suite of unit test for Colony use the following sequence of commands that will install dependencies
and run the appropriate test suite (last command).

Try to run the unit tests whenever making changes to the codebase, before commiting new code.

```bash
pip install -r requirements.txt
pip install -r extra.txt
python setup.py test
```

## Style Guide

- Always update `CHANGELOG.md` according to semantic versioning, mentioning your changes in the unreleased section.
- Write commit messages using [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).
- Never bump the internal package version in `setup.py`. This is handled automatically by the release process.
- Python files use CRLF as the line ending.
- The implementation should be done in Python 2.7+ and compatible with Python 3.13.
- No type annotations should exist in the `.py` files and if the exist they should isolated in th `.pyi` files.
- The style should respect the black formatting.
- The implementation should be done in a way that is compatible with the existing codebase.
- Prefer `item not in list` over `not item in list`.
- Prefer `item == None` over `item is None`.
- The commenting style of the project is unique, try to keep commenting style consistent.

## Commit Messages

This project follows [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) with the following structure:

```text
<type>: <description>

<body>
```

### Commit Types

| Type       | Description                                             |
| ---------- | ------------------------------------------------------- |
| `feat`     | A new feature or functionality                          |
| `fix`      | A bug fix                                               |
| `docs`     | Documentation only changes                              |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `chore`    | Maintenance tasks, dependency updates, build changes    |
| `test`     | Adding or updating tests                                |
| `version`  | Version bump commits (reserved for releases)            |

### Guidelines

- Use lowercase for the type prefix.
- Use imperative mood in the description (e.g., "Add feature" not "Added feature").
- Keep the first line under 50 characters.
- Reference issue/PR numbers when applicable using `(#123)` at the end.
- For version releases, use the format `version: X.Y.Z`.
- Add an extra newline between subject and body.
- Make the body a series of bullet points about the commit.
- Be descriptive always making use of the body of the message.

### Examples

```text
feat: Add user authentication with OAuth 2.0 support (#138)
fix: Resolve race condition in database connection pool
docs: Add API endpoint documentation for v2 routes
refactor: Extract validation logic into reusable utility module
chore: Update dependencies to latest stable versions
test: Add integration tests for payment processing flow
version: 1.8.0
```

## Pre-Commit Checklist

Before committing, ensure that the following operations items check:

- [ ] Code is formatted with `black .`
- [ ] Tests pass: `python setup.py test`
- [ ] CHANGELOG.md is updated in [Unreleased] section
- [ ] No debugging print statements or commented-out code
- [ ] CRLF line endings are preserved
- [ ] No type annotations in .py files (use .pyi if needed)

## New Release

To create a new release follow the following steps:

- Make sure that both the tests pass and the code formatting are valid.
- Increment (look at `CHANGELOG.md` for semver changes) the `version` value in `setup.py`.
- Update the version value in `src/colony/res/colony.json`.
- Add a new single line entry as a list in the `src/colony/res/colony.log.json` with a simple description of the change in line with the previous changes structure.
- Move all the `CHANGELOG.md` Unreleased items that have at least one non empty item the into a new section with the new version number and date, and then create new empty sub-sections (Added, Changed and Fixed) for the Unreleased section with a single empty item.
- Create a commit with the following message `version: $VERSION_NUMBER`.
- Push the commit.
- Create a new tag with the value fo the new version number `$VERSION_NUMBER`.
- Create a new release on the GitHub repo using the Markdown from the corresponding version entry in `CHANGELOG.md` as the description of the release and the version number as the title.

## License

Hive Colony Framework is licensed under the [Apache License, Version 2.0](http://www.apache.org/licenses/).
