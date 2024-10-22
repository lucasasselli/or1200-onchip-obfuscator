# If you want to use the VJTAG TAP or the XILINX BSCAN,
# you must set your FPGA TAP ID here

set FPGATAPID 0x031050dd

# Choose your TAP core (VJTAG , MOHOR or XILINX_BSCAN)
if { [info exists TAP_TYPE] == 0} {
   set TAP_TYPE VJTAG
}

# Set your chip name
set CHIPNAME or1200

source [find target/or1k.cfg]

# Set the servers polling period to 1ms (needed to JSP Server)
poll_period 1

# Enable the target description feature
gdb_target_description enable

# Add a new register in the cpu register list. This register will be
# included in the generated target descriptor file.
# format is addreg [name] [address] [feature] [reg_group]
addreg rtest 0x1234 org.gnu.gdb.or1k.group0 system

# Override default init_reset
proc init_reset {mode} {
	soft_reset_halt
	resume
}

gdb_port 50001
telnet_port 4444

# Target initialization
init
echo "Halting processor"
halt

foreach name [target names] {
	set y [$name cget -endian]
	set z [$name cget -type]
	puts [format "Chip is %s, Endian: %s, type: %s" \
	      $name $y $z]
}

set c_blue  "\033\[01;34m"
set c_reset "\033\[0m"

puts [format "%sTarget ready...%s" $c_blue $c_reset]

