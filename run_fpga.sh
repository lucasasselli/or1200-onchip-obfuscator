#!/bin/bash
function finish {
    echo "Stopping OpenOCD..."
    kill $PID_OPENOCD 2> /dev/null
}
trap finish EXIT

# Program FPGA
fusesoc --cores-root=fusesoc pgm de10_lite

# Start openocd
openocd -f interface/altera-usb-blaster.cfg -f or1k-dev.tcl & < /dev/null
PID_OPENOCD=$!

sleep 2

# Start GDB
or1k-elf-gdb -ex "target remote :50001"
