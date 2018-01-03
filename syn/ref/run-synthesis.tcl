# OpenRISC Synthesis Script

remove_design -designs

set CORE_PATH = ../../fusesoc/cores/or1200-ref/rtl/verilog
set SYS_PATH = ../../fusesoc/systems/or1200-ref-generic/bench/verilog/include

# Defines
analyze -library WORK -format verilog $SYS_PATH/or1200_defines.v
analyze -library WORK -format verilog $CORE_PATH/obf_defines.v

# ALU
analyze -library WORK -format verilog $CORE_PATH/or1200_alu.v

# FPU
# analyze -library WORK -format verilog $CORE_PATH/or1200_fpu_post_norm_div.v
# analyze -library WORK -format verilog $CORE_PATH/or1200_fpu_div.v
# analyze -library WORK -format verilog $CORE_PATH/or1200_fpu_pre_norm_div.v
# analyze -library WORK -format verilog $CORE_PATH/or1200_fpu_post_norm_mul.v
# analyze -library WORK -format verilog $CORE_PATH/or1200_fpu_mul.v
# analyze -library WORK -format verilog $CORE_PATH/or1200_fpu_pre_norm_mul.v
# analyze -library WORK -format verilog $CORE_PATH/or1200_fpu_post_norm_addsub.v
# analyze -library WORK -format verilog $CORE_PATH/or1200_fpu_addsub.v
# analyze -library WORK -format verilog $CORE_PATH/or1200_fpu_pre_norm_addsub.v
# analyze -library WORK -format verilog $CORE_PATH/or1200_fpu_arith.v
# analyze -library WORK -format verilog $CORE_PATH/or1200_fpu_post_norm_intfloat_conv.v
# analyze -library WORK -format verilog $CORE_PATH/or1200_fpu_intfloat_conv.v
# analyze -library WORK -format verilog $CORE_PATH/or1200_fpu_fcmp.v
# analyze -library WORK -format verilog $CORE_PATH/or1200_fpu.v

# Register File
analyze -library WORK -format verilog $CORE_PATH/or1200_mem2reg.v
analyze -library WORK -format verilog $CORE_PATH/or1200_reg2mem.v
#analyze -library WORK -format verilog $CORE_PATH/or1200_xcv_ram32x8d.v
#analyze -library WORK -format verilog $CORE_PATH/or1200_gmultp2_32x32.v
#analyze -library WORK -format verilog $CORE_PATH/or1200_dpram_256x32.v
#analyze -library WORK -format verilog $CORE_PATH/or1200_dpram_32x32.v
#analyze -library WORK -format verilog $CORE_PATH/or1200_tpram_32x32.v
analyze -library WORK -format verilog $CORE_PATH/or1200_dpram.v
analyze -library WORK -format verilog $CORE_PATH/or1200_rfram_generic.v
analyze -library WORK -format verilog $CORE_PATH/or1200_rf.v

# Pipeline
analyze -library WORK -format verilog $CORE_PATH/or1200_genpc.v
analyze -library WORK -format verilog $CORE_PATH/or1200_if.v
analyze -library WORK -format verilog $CORE_PATH/or1200_ctrl.v
analyze -library WORK -format verilog $CORE_PATH/or1200_operandmuxes.v
analyze -library WORK -format verilog $CORE_PATH/or1200_amultp2_32x32.v
analyze -library WORK -format verilog $CORE_PATH/or1200_mult_mac.v
analyze -library WORK -format verilog $CORE_PATH/or1200_sprs.v
analyze -library WORK -format verilog $CORE_PATH/or1200_lsu.v
analyze -library WORK -format verilog $CORE_PATH/or1200_wbmux.v
analyze -library WORK -format verilog $CORE_PATH/or1200_freeze.v
analyze -library WORK -format verilog $CORE_PATH/or1200_except.v
analyze -library WORK -format verilog $CORE_PATH/or1200_cfgr.v

# CPU
analyze -library WORK -format verilog $CORE_PATH/or1200_cpu.v

# Memory Configurations
#analyze -library WORK -format verilog $CORE_PATH/or1200_spram_1024x32_bw.v
#analyze -library WORK -format verilog $CORE_PATH/or1200_spram_1024x32.v
#analyze -library WORK -format verilog $CORE_PATH/or1200_spram_1024x8.v
#analyze -library WORK -format verilog $CORE_PATH/or1200_spram_128x32.v
#analyze -library WORK -format verilog $CORE_PATH/or1200_spram_2048x32_bw.v
#analyze -library WORK -format verilog $CORE_PATH/or1200_spram_2048x32.v
#analyze -library WORK -format verilog $CORE_PATH/or1200_spram_2048x8.v
#analyze -library WORK -format verilog $CORE_PATH/or1200_spram_256x21.v
#analyze -library WORK -format verilog $CORE_PATH/or1200_spram_32_bw.v
#analyze -library WORK -format verilog $CORE_PATH/or1200_spram_32x24.v
#analyze -library WORK -format verilog $CORE_PATH/or1200_spram_512x20.v
#analyze -library WORK -format verilog $CORE_PATH/or1200_spram_64x14.v
#analyze -library WORK -format verilog $CORE_PATH/or1200_spram_64x22.v
#analyze -library WORK -format verilog $CORE_PATH/or1200_spram_64x24.v
#analyze -library WORK -format verilog $CORE_PATH/or1200_spram.v


# Instruction Cache
analyze -library WORK -format verilog $CORE_PATH/or1200_ic_ram.v
analyze -library WORK -format verilog $CORE_PATH/or1200_ic_tag.v
analyze -library WORK -format verilog $CORE_PATH/or1200_ic_fsm.v
analyze -library WORK -format verilog $CORE_PATH/or1200_ic_top.v

# Data Cache
analyze -library WORK -format verilog $CORE_PATH/or1200_dc_ram.v
analyze -library WORK -format verilog $CORE_PATH/or1200_dc_tag.v
analyze -library WORK -format verilog $CORE_PATH/or1200_dc_fsm.v
analyze -library WORK -format verilog $CORE_PATH/or1200_dc_top.v

# MMU
analyze -library WORK -format verilog $CORE_PATH/or1200_immu_tlb.v
analyze -library WORK -format verilog $CORE_PATH/or1200_immu_top.v
analyze -library WORK -format verilog $CORE_PATH/or1200_dmmu_tlb.v
analyze -library WORK -format verilog $CORE_PATH/or1200_dmmu_top.v

# Bus
analyze -library WORK -format verilog $CORE_PATH/or1200_iwb_biu.v
analyze -library WORK -format verilog $CORE_PATH/or1200_wbmux.v
analyze -library WORK -format verilog $CORE_PATH/or1200_wb_biu.v

# Other ...
analyze -library WORK -format verilog $CORE_PATH/or1200_qmem_top.v
analyze -library WORK -format verilog $CORE_PATH/or1200_sb_fifo.v
analyze -library WORK -format verilog $CORE_PATH/or1200_sb.v
analyze -library WORK -format verilog $CORE_PATH/or1200_du.v
analyze -library WORK -format verilog $CORE_PATH/or1200_tt.v
analyze -library WORK -format verilog $CORE_PATH/or1200_pm.v
analyze -library WORK -format verilog $CORE_PATH/or1200_pic.v

# Top Module
analyze -library WORK -format verilog $CORE_PATH/or1200_top.v

elaborate or1200_top -architecture verilog -update
current_design or1200_top
uniquify

create_clock -name clk -period 40 -waveform [list 0.0 20] [list "clk_i"]

link
compile -map_effort high -area_effort high

# Reports
sh rm -rf report
sh mkdir report
redirect ./report/timing.log         {check_timing}
redirect ./report/constraints.log    {report_constraints -all_violators -verbose}
redirect ./report/paths-max.log      {report_timing -path end  -delay max -max_paths 200 -nworst 2}
redirect ./report/full-paths-max.log {report_timing -path full -delay max -max_paths 5   -nworst 2}
redirect ./report/paths-min.log      {report_timing -path end  -delay min -max_paths 200 -nworst 2}
redirect ./report/full_paths-min.log {report_timing -path full -delay min -max_paths 5   -nworst 2}
redirect ./report/refs.log           {report_reference}
redirect ./report/area.log           {report_area -hierarchy}

# Add NAND2 size equivalent report to the area report file
set nand2_area [get_attribute [get_lib_cell NangateOpenCellLibrary/NAND2_X1] area]
redirect -variable area {report_area}
regexp {Total cell area:\s+([^\n]+)\n} $area whole_match area
set nand2_eq [expr $area/$nand2_area]
set fp [open "./report/area.log" a]
puts $fp ""
puts $fp "NAND2 area: $nand2_area"
puts $fp "NAND2 equivalent cell area: $nand2_eq"
close $fp
