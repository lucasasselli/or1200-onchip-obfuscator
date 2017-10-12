#!/bin/bash
ELF_NAME=hello
ELF_PATH=sw/hello/hello.elf
SAMPLES="0 25 50 100 125 150 175 200 225 250"

set -e

# Run reference
echo "-> Running reference simulation..."
./run-sim.sh -e $ELF_PATH -t ref -s icarus -l &> /dev/null

# Run obfuscator
for i in $SAMPLES; do
    echo "--------------------------------------------------"
    echo "                    Test $i"
    echo "--------------------------------------------------"

    echo "-> Running obfuscator simulation..."
    ./run-sim.sh -e $ELF_PATH -t obf -s icarus -f $i -l &> /dev/null

    echo "-> Checking code correctness..."
    obf-outcheck.py build/or1200-ref-generic_0/sim-icarus/tb-executed.log build/or1200-obf-generic_0/sim-icarus/tb-executed.log

    echo "-> Looking for trojans..."
    obf-trojanfind.py out/hello/ref_${ELF_NAME}.exec out/hello/obf_${ELF_NAME}_$i.exec 5 10 10
done
