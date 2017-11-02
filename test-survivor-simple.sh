#!/bin/bash
ELF_FILE=$1
ELF_DIR=$(dirname $ELF_FILE)
ELF_FULLNAME=$(basename $ELF_FILE)
ELF_NAME=${ELF_FULLNAME%.*}
SIMULATOR=verilator

set -e

# Run reference
echo "-> Running reference simulation..."
./run-sim.sh -e $ELF_FILE -t ref -s $SIMULATOR -l

# Run obfuscator
for i in {0..255..5}; do
    echo "--------------------------------------------------"
    echo "                    Test $i"
    echo "--------------------------------------------------"

    echo "-> Running obfuscator simulation..."
    ./run-sim.sh -e $ELF_FILE -t obf -s $SIMULATOR -f $i -l

    # echo "-> Checking code correctness..."
    # obf-outcheck.py build/or1200-ref-generic_0/sim-icarus/tb-executed.log build/or1200-obf-generic_0/sim-icarus/tb-executed.log

    echo "-> Looking for trojans..."
    obf-trojanfind.py out/${SIMULATOR}_${ELF_NAME}/ref_${ELF_NAME}.exec out/${SIMULATOR}_${ELF_NAME}/obf_${ELF_NAME}_$i.exec 3 10 10 -o surv_digital_${ELF_NAME}.csv
    rm out/${SIMULATOR}_${ELF_NAME}/obf_${ELF_NAME}_$i.* -r
done
