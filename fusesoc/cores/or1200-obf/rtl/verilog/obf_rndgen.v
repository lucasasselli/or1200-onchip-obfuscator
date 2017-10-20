// synopsys translate_off
`include "timescale.v"
// synopsys translate_on
`include "or1200_defines.v"
`include "obf_defines.v"

module obf_rndgen(
    clk, rst, 
    en, out
);

// Parameters
parameter SEED = 124;
parameter SIZE = 8;

input clk;
input rst;
input en;
output out;

wire feedback;

`ifdef OBF_RND8
    // Short period LFSR
    `define LFSR_WIDTH 8
    reg [`LFSR_WIDTH-1:0] lfsr;
    assign feedback = (lfsr[7] ^ lfsr[5] ^ lfsr[4] ^ lfsr[3]);
    assign out = lfsr;
`else
    // Long period LFSR
    `define LFSR_WIDTH 32
    reg [`LFSR_WIDTH-1:0] lfsr;
    assign feedback = (lfsr[31] ^ lfsr[21] ^ lfsr[1] ^ lfsr[0]);
    assign out = lfsr[SIZE-1:0];
`endif

always @(posedge clk or `OR1200_RST_EVENT rst)
begin
    if (rst == `OR1200_RST_VALUE) begin
        lfsr <= SEED;
    end
    else if (en)
        lfsr <= {lfsr[`LFSR_WIDTH-2:0],feedback};
    else
        lfsr <= lfsr;
end
endmodule
