// synopsys translate_off
`include "timescale.v"
// synopsys translate_on
`include "or1200_defines.v"
`include "obf_defines.v"

module obf_lut_top(
    index,
    ppc,
    key,
    out_sub,
    out_imm
);

input [`OBF_IGU_WIDTH-1:0] index;
input [`OBF_PPC_WIDTH-1:0] ppc;
input [`OBF_KEY_WIDTH-1:0] key;
output [`OBF_LUT_OUT_WIDTH-1:0] out_sub;
output [`OBF_LUT_OUT_WIDTH-1:0] out_imm;

//////////////////////////////////////////////////
// LUT 0
//////////////////////////////////////////////////

wire [`OBF_LUT_ADDR_WIDTH-1:0] lut0_ptr;
wire [`OBF_LUT_ADDR_WIDTH-1:0] lut0_addr = lut0_ptr + ppc;
wire [`OBF_LUT_OUT_WIDTH-1:0] lut0_out_sub;
wire [`OBF_LUT_OUT_WIDTH-1:0] lut0_out_imm;

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
