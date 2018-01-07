// synopsys translate_off
`include "timescale.v"
// synopsys translate_on
`include "or1200_defines.v"
`include "obf_defines.v"

module obf_keydec(
    clk,rst,
    key,
    go,
    obf_en,
    lut_sel
);

input clk;
input rst;
input key;
input go;
output obf_en;
output lut_sel;


`ifdef OBF_CTRL_COUNTER
    // Simple counter

    reg [7:0] rnd;

    always @(posedge clk or `OR1200_RST_EVENT rst) 
    begin
        if (rst == `OR1200_RST_VALUE) begin
            // Reset
            rnd <= 0;
        end
        else begin
            if(ctrl_go) begin
                rnd <= rnd + 1;
            end
            else begin
                rnd <= rnd;
            end
        end
    end
`else
    // Pseudo-random

    wire [7:0] rnd;

    obf_rndgen obf_rndgen_i(
        .clk(clk),
        .rst(rst),
        .en(ctrl_go),
        .out(rnd)
    );
`endif

// sub_freq is a fusesoc parameter
assign obf_en = (rnd <= `sub_freq) ? 1'd1 : 1'd0;

endmodule
