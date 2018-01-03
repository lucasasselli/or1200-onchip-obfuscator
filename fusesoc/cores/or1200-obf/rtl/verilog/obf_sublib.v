// synopsys translate_off
`include "timescale.v"
// synopsys translate_on
`include "or1200_defines.v"
`include "obf_defines.v"

module obf_sublib(
    index,
    ppc,
    sel,
    out_sub,
    out_imm
);

input [`OBF_INDEX_BUS] index;
input [`OBF_PPC_BUS] ppc;
input [`LUT_SEL_BUS] sel;
output [`LUT_OUT_BUS] out_sub;
output [`LUT_OUT_BUS] out_imm;

//////////////////////////////////////////////////
// LUT 0
//////////////////////////////////////////////////

wire [`LUT_ADDR_BUS] lut0_ptr;
wire [`LUT_ADDR_BUS] lut0_addr = lut0_ptr + ppc;
wire [`LUT_OUT_BUS] lut0_out_sub;
wire [`LUT_OUT_BUS] lut0_out_imm;

obf_pt0 obf_pt0_i(
    index,
    lut0_ptr
);

obf_lut0 obf_lut0_i(
    lut0_addr,
    lut0_out_sub,
    lut0_out_imm
);

assign out_sub = lut0_out_sub;
assign out_imm = lut0_out_imm;

endmodule
