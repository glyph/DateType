# DateType

## Purpose

DateType is a workaround for two issues in the typeshed:

1. Using `datetype`, [a `datetime` won't type-check as a
   `date`](https://github.com/python/mypy/issues/9015) - it still inherits at
   runtime (the implementation is not changed since the implementation is not
   changed) but it doesn't inherit at type-time.

2. [there are separate types for naive and aware
   `datetime`s](https://github.com/python/mypy/issues/10067).

It is a type-checking-time wrapper for `datetime` that doesn't change the
implementation besides adding a couple of factory functions

## Usage

Primarily, `datetype` exports a set of `Protocol` types, PEP-8 renames of the
types from `datetime`:

- `datetype.Date`
- `datetype.Time[ZoneInfo]`
- `datetype.DateTime[ZoneInfo]`

To translate 
