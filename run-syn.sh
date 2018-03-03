REPO_PATH=build/or1200-syn

# NOTE:
# Unfortuanately Fusesoc doesn't support design synthesis, thus we have to improvise!
# MacGyver would be proud...

# Obtain repository
if [ ! -d "$REPO_PATH" ]; then
    echo "-> Getting repository"
    git clone https://github.com/openrisc/or1200 $REPO_PATH
fi

# Synthesize?
while true; do
    read -p "Do you wish to synthesize again the reference? [y/n]" yn
    case $yn in
        [Yy]* ) SYNTH_REF=true;break;;
        [Nn]* ) SYNTH_REF=false;break;;
        * ) echo "Please answer yes or no.";;
    esac
done

# Original processor
if [ "$SYNTH_REF" = true ]; then
    rm -rf out/syn/ref
    mkdir -p out/syn/ref
    rm -rf build/work
    echo "-> Original processor synthesis"
    dc_shell-xg-t -f syn/run-ref-syn.tcl > out/syn/ref/syn.log
fi

# Modified processor
rm -rf out/syn/obf
mkdir -p out/syn/obf
rm -rf build/work
echo "-> Modified processor synthesis"
dc_shell-xg-t -f syn/run-obf-syn.tcl > out/syn/obf/syn.log
