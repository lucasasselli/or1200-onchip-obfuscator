sh rm -rf ./build/work
define_design_lib WORK -path ./build/work
remove_design -designs
set search_path [list . /software/synopsys/syn_current/libraries/syn /software/dk/nangate45/synopsys ]
set link_library [list "*" "NangateOpenCellLibrary_typical_ecsm_nowlm.db" "dw_foundation.sldb" ]
set target_library [list "NangateOpenCellLibrary_typical_ecsm_nowlm.db" ]
set synthetic_library [list "dw_foundation.sldb" ]
