`include "obf_defines.v" 

module obf_ctrl(
    clk,rst,
    ctrl_key,
    ctrl_go,
    obf_en,
    lut_i
);

input clk;
input rst;
input ctrl_key;
input ctrl_go;
output obf_en;
output lut_i;

wire [7:0] rnd;

obf_rndgen obf_rndgen_i(
    .clk(clk),
    .rst(rst),
    .en(ctrl_go),
    .out(rnd)
);

assign obf_en = (rnd <= `sub_freq) ? 1'd1 : 1'd0;

endmodule
