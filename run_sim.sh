#!/bin/bash
DIR=$(pwd)
SIMULATOR=verilator
TARGET_SYS=or1200-obf-generic
ELF_PATH=$DIR/sw/or1k-mibench/automotive/basicmath
ELF_FILE=basicmath_large

# Compile target software
make -C $ELF_PATH

# Start simulation
fusesoc --cores-root=fusesoc sim --sim=$SIMULATOR $TARGET_SYS --elf-load $ELF_PATH/$ELF_FILE
