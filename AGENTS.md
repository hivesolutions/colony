# AGENTS.md file

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

- Increment (look at `CHANGELOG.md` for semver changes) the `version` value in `setup.py`.
- Update the version value in `src/colony/res/colony.json`.
- Add a new single line entry as a list in the `src/colony/res/colony.log.json` with a simple description of the change in line with the previous changes structure.
- Move all the `CHANGELOG.md` Unreleased items that have at least one non empty item the into a new section with the new version number and date, and then create new empty sub-sections (Added, Changed and Fixed) for the Unreleased section with a single empty item.
- Create a commit with the following message `version: $VERSION_NUMBER`.
- Push the commit.
- Create a new tag with the value fo the new version number `$VERSION_NUMBER`.

## License

Hive Colony Framework is licensed under the [Apache License, Version 2.0](http://www.apache.org/licenses/).
