# Configuration
OUT_DIR=out

# DO NOT MODIFY AFTER THIS LINE
SIMULATOR=modelsim-gui
TARGET_NAME=obf

ELF_SET=false

# Parse arguments
while getopts ":s:t:e:" opt; do
    case $opt in
        s)
            SIMULATOR=$OPTARG
            ;;
        t)
            TARGET_NAME=$OPTARG
            ;;
        e)
            ELF_FILE=$OPTARG
            ELF_SET=true
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

# Check mandatory inputs

if [ "$ELF_FILE" == false ]; then
    echo "You must specify a .elf file!" >&2
    exit 1
fi

if [ ! -f "$ELF_FILE" ]; then
    echo "Specified .elf file doesn't exist" >&2
    exit 1
fi

# Get elf info
ELF_DIR=$(dirname $ELF_FILE)
ELF_FULLNAME=$(basename $ELF_FILE)
ELF_NAME=${ELF_FULLNAME%.*}

# Print info and set stuff
case $TARGET_NAME in
    obf)
        TARGET_SYS=or1200-obf-generic
        echo "RUNNING TEST ON OBFUSCATOR"
        ;;
    ref)
        TARGET_SYS=or1200-ref-generic
        echo "RUNNING TEST ON REFERENCE"
        ;;
    *)
        echo "Invalid target: $TARGET_NAME" >&2
        exit 1
        ;;
esac

# Compile target software
make clean -C $ELF_DIR
make $ELF_FULLNAME -C $ELF_DIR

# Start simulation
if [ "$SIMULATOR" = "modelsim-gui" ]; then
    # Modelsim GUI
    SIMULATOR=modelsim # Cheap but easy
    fusesoc --cores-root=fusesoc sim --build-only --sim=modelsim $TARGET_SYS --elf-load $ELF_FILE
    cd build/${TARGET_SYS}_0/sim-modelsim
    vsim -do fusesoc_run.tcl 
else
    # Any other
    fusesoc --cores-root=fusesoc sim --sim=$SIMULATOR $TARGET_SYS --elf-load $ELF_FILE
fi

if [ ! "$SIMULATOR" == "verilator" ]; then
    # Move generated output to output folder
    RES_DIR=build/${TARGET_SYS}_0/sim-${SIMULATOR}
    OUT_DIR=${OUT_DIR}/${ELF_NAME}

    RES_EXEC_FILE=${RES_DIR}/tb-executed.log
    OUT_EXEC_FILE=${OUT_DIR}/${TARGET_NAME}_${ELF_NAME}.exec

    RES_OUT_FILE=${RES_DIR}/tb-output.log
    OUT_OUT_FILE=${OUT_DIR}/${TARGET_NAME}_${ELF_NAME}.out

    # If doesn't exist create output folder
    if [ ! -d $OUT_DIR ]; then
        mkdir $OUT_DIR
    fi

    # Remove homonyms
    rm $OUT_EXEC_FILE > /dev/null 2>&1 
    rm $OUT_OUT_FILE > /dev/null 2>&1 

    # Remove useless lines from ex file
    while read LINE
    do
        if [[ $LINE == *"EXECUTED"* ]]; then
            echo ${LINE#EXECUTED: } >> $OUT_EXEC_FILE
        fi
    done < $RES_EXEC_FILE

    mv $RES_OUT_FILE $OUT_OUT_FILE
fi

exit 0
