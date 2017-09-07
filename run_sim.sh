#!/bin/bash

# Configuration
TARGET_SYS=or1200-obf-generic
ELF_PATH=or1k-mibench/automotive/basicmath
ELF_FILE=basicmath_small.elf
# ELF_PATH=hello
# ELF_FILE=main.elf

# DO NOT MODIFY AFTER THIS LINE
SIMULATOR=modelsim-gui
SW_PATH=$(pwd)/sw

while getopts ":s:" opt; do
    case $opt in
        s)
            SIMULATOR=$OPTARG
            ;;
        \?)
            echo "Invalid option: -$OPTARG" >&2
            exit 1
            ;;
        :)
            echo "Option -$OPTARG requires an argument." >&2
            exit 1
            ;;
    esac
done

# Compile target software
make -C $SW_PATH/$ELF_PATH

# Start simulation
if [ "$SIMULATOR" = "modelsim-gui" ]; then
    # Modelsim GUI
    fusesoc --cores-root=fusesoc sim --build-only --sim=modelsim $TARGET_SYS --elf-load $SW_PATH/$ELF_PATH/$ELF_FILE
    cd build/${TARGET_SYS}_0/sim-modelsim
    vsim -do fusesoc_run.tcl 
else
    # Any other
    fusesoc --cores-root=fusesoc sim --sim=$SIMULATOR $TARGET_SYS --elf-load $SW_PATH/$ELF_PATH/$ELF_FILE
fi
