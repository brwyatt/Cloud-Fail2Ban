#!/bin/bash

echo "Preparing artifact dirs"
mkdir -p build/python

echo "Installing Python module dependencies"
grep -ivEe '^boto(3|core)[=<>]' requirements.txt | pip install -r /dev/stdin --target build/python

echo "Installing Python module"
pip install --no-dependencies --target build/python .
