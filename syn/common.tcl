elaborate or1200_top -architecture verilog -update
current_design or1200_top
uniquify

create_clock -name clk -period 10 [list "clk_i"]

link
# compile -map_effort high -area_effort high
compile_ultra -area_high_effort_script -no_autoungroup
# compile_ultra -timing_high_effort_script
# compile

# Reports
set REPORT_PATH out/syn/$TARGET
redirect $REPORT_PATH/check-timing.log   {check_timing}
redirect $REPORT_PATH/check-design.log   {check_design}
redirect $REPORT_PATH/constraints.log    {report_constraints -all_violators -verbose}
redirect $REPORT_PATH/paths-max.log      {report_timing -path end  -delay max -max_paths 200 -nworst 2}
redirect $REPORT_PATH/full-paths-max.log {report_timing -path full -delay max -max_paths 5   -nworst 2}
redirect $REPORT_PATH/paths-min.log      {report_timing -path end  -delay min -max_paths 200 -nworst 2}
redirect $REPORT_PATH/full-paths-min.log {report_timing -path full -delay min -max_paths 5   -nworst 2}
redirect $REPORT_PATH/refs.log           {report_reference}
redirect $REPORT_PATH/area.log           {report_area -hierarchy}

# Add NAND2 size equivalent report to the area report file
set nand2_area [get_attribute [get_lib_cell NangateOpenCellLibrary/NAND2_X1] area]
redirect -variable area {report_area}
regexp {Total cell area:\s+([^\n]+)\n} $area whole_match area
set nand2_eq [expr $area/$nand2_area]
set fp [open $REPORT_PATH/area.log a]
puts $fp ""
puts $fp "NAND2 area: $nand2_area"
puts $fp "NAND2 equivalent cell area: $nand2_eq"
close $fp

# Finally
check_design
