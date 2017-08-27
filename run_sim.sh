#!/bin/bash
SIMULATOR=modelsim
TARGET_SYS=or1200-obf-generic
ELF_PATH=hello
ELF_FILE=main.elf

# Compile target software
make -C sw/$ELF_PATH

# Build target system
fusesoc --cores-root=fusesoc sim --sim=$SIMULATOR --build-only $TARGET_SYS --elf-load sw/$ELF_PATH/$ELF_FILE

# Run simulation
cd build/${TARGET_SYS}_0/sim-$SIMULATOR
vsim -do fusesoc_run.tcl
