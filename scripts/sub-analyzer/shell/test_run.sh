#!/bin/bash

SIMULATOR=icarus
TARGET_SYS=or1200-ref-generic

# Exit on error
set -e

# Redirect STDERR to STDOUT
exec 2>&1

ROOT=../../

# Compile test
make all -C test

# Run simulation
fusesoc --cores-root=${ROOT}/fusesoc sim --sim=${SIMULATOR} ${TARGET_SYS} --elf-load=test/test.elf

# Get logs
echo $(pwd)
cp build/${TARGET_SYS}_0/sim-${SIMULATOR}/tb-general.log test/simulation.log
