#!/bin/bash

#exit on error
set -e

# Redirect STDERR to STDOUT
exec 2>&1

cd $(dirname $0)
this_dir=${PWD}
root_dir=../../
cd - &>/dev/null

#compile utilities
cd ${root_dir}/sw/utils
make all
cd - &>/dev/null

#compile support libraries
cd ${root_dir}/sw/support
make all
cd - &>/dev/null

#compile program
cd ${this_dir}/test
make test-nocache
cd - &>/dev/null

#generate hex image
${root_dir}/sw/utils/bin2hex ${this_dir}/test/test-nocache.bin > ${root_dir}/sim/src/flash.in
