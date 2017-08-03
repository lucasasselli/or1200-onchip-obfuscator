#!/bin/bash

# Exit on error
set -e

# Redirect STDERR to STDOUT
exec 2>&1

# Remove build directory
rm -rf build

# Compile test
make clean -C test
