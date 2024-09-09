#!/bin/sh

set -x

echo Checking and formatting with black...
black --check src

echo Python type checking...
mypy src/tg --warn-redundant-casts --warn-unused-ignores \
    --no-warn-no-return --warn-unreachable --strict-equality \
    --ignore-missing-imports --warn-unused-configs \
    --disallow-untyped-calls --disallow-untyped-defs \
    --disallow-incomplete-defs --check-untyped-defs \
    --disallow-untyped-decorators

echo Checking import sorting...
isort -c src/tg/*.py

echo Checking unused imports...
flake8 --select=F401
