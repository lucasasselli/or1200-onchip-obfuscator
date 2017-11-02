#!/bin/bash
ELF_FILE=$1
ELF_DIR=$(dirname $ELF_FILE)
ELF_FULLNAME=$(basename $ELF_FILE)
ELF_NAME=${ELF_FULLNAME%.*}
SIMULATOR=verilator

set -e

get_lines(){
    wc -l $1 | awk {'print $1'}
}

get_tcc(){
    echo "$1" | grep -oP '(?<=cycles = )[0-9]+' 
}

# Run reference
echo "-> Running reference simulation..."
RAW_RUN=$(./run-sim.sh -e $ELF_FILE -t ref -s $SIMULATOR -l)
REF_RUN=$(get_tcc "$RAW_RUN")
REF_LENGTH=$(get_lines out/${SIMULATOR}_${ELF_NAME}/ref_${ELF_NAME}.exec)

# Run obfuscator
j=0
for i in {0..255..5}; do
    echo "--------------------------------------------------"
    echo "                    Test $i"
    echo "--------------------------------------------------"

    echo "-> Running obfuscator simulation..."
    RAW_RUN=$(./run-sim.sh -e $ELF_FILE -t obf -s $SIMULATOR -f $i -l)
    OBF_RUN[$j]=$(get_tcc "$RAW_RUN")
    OBF_LENGTH[$j]=$(get_lines out/${SIMULATOR}_${ELF_NAME}/obf_${ELF_NAME}_$i.exec)
    j=$((j+1))
done


echo "\"Ref. length\",\"Ref. cycles\"" > time_cache_${ELF_NAME}.csv
echo ${REF_LENGTH}","${REF_RUN} >> time_cache_${ELF_NAME}.csv
echo "\"Ref. length\",\"Ref. cycles\"" >> time_cache_${ELF_NAME}.csv
for i in "${!OBF_RUN[@]}"
do
    echo ${OBF_LENGTH[$i]}","${OBF_RUN[$i]} >> time_cache_${ELF_NAME}.csv
done
