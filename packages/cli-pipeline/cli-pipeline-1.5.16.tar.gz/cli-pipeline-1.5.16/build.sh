#!/bin/bash

mypy cli_pipeline/__init__.py

# --no-cache
pip install --ignore-installed -e .

pipeline version
