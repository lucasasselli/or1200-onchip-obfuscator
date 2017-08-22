#!/bin/bash
SIMULATOR=modelsim
TARGET_SYS=or1200-obf-generic
TARGET_SW=hello

# Compile target software
make -C sw/$TARGET_SW

# Build target system
fusesoc --cores-root=fusesoc sim --sim=$SIMULATOR --build-only $TARGET_SYS --elf-load sw/$TARGET_SW/main.elf

# Run simulation
cd build/${TARGET_SYS}_0/sim-$SIMULATOR
vsim -do fusesoc_run.tcl
