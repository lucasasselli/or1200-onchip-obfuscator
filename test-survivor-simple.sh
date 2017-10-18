#!/bin/bash
ELF_FILE=$1
ELF_DIR=$(dirname $ELF_FILE)
ELF_FULLNAME=$(basename $ELF_FILE)
ELF_NAME=${ELF_FULLNAME%.*}
SIMULATOR=verilator
SAMPLES="0 25 50 100 125 150 175 200 225 250"

set -e

# Run reference
echo "-> Running reference simulation..."
./run-sim.sh -e $ELF_FILE -t ref -s $SIMULATOR -l &> /dev/null

# Run obfuscator
for i in $SAMPLES; do
    echo "--------------------------------------------------"
    echo "                    Test $i"
    echo "--------------------------------------------------"

    echo "-> Running obfuscator simulation..."
    ./run-sim.sh -e $ELF_FILE -t obf -s $SIMULATOR -f $i -l &> /dev/null

    # echo "-> Checking code correctness..."
    # obf-outcheck.py build/or1200-ref-generic_0/sim-icarus/tb-executed.log build/or1200-obf-generic_0/sim-icarus/tb-executed.log

    echo "-> Looking for trojans..."
    obf-trojanfind.py out/${SIMULATOR}_${ELF_NAME}/ref_${ELF_NAME}.exec out/${SIMULATOR}_${ELF_NAME}/obf_${ELF_NAME}_$i.exec 5 10 5
done
