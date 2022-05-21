# DateType

## A Workaround

DateType is a [workaround for this
bug](https://github.com/python/mypy/issues/9015) to demonstrate that we could
have a type-checking-time wrapper for `datetime` that doesn't change (or almost
doesn't change) the implementation, but fixes up two very annoying behaviors of
the stdlib `datetime` module:

1. a `datetime` now won't type-check as a `date` - it still inherits at runtime
   (the implementation is, after all, not changed) but it doesn't inherit at
   type-time.

2. there are separate types for naive and aware `datetime`s.

There's a very small bit of implementation glue (concrete `@classmethod`s for
construction on the `Naive` and `Aware` types, and a few functions that do
runtime checks to convert to/from stdlib types).
