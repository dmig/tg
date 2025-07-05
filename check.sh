#!/bin/sh

set -x

echo Checking formatting...
rye fmt --check src

echo Lint code...
rye lint src

echo Python type checking...
mypy src/tg --warn-redundant-casts --warn-unused-ignores \
    --no-warn-no-return --warn-unreachable --strict-equality \
    --ignore-missing-imports --warn-unused-configs \
    --disallow-untyped-calls --disallow-untyped-defs \
    --disallow-incomplete-defs --check-untyped-defs \
    --disallow-untyped-decorators
