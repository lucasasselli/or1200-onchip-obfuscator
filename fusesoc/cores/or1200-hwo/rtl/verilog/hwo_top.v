`include "or1200_defines.v"
`include "hwo_defines.v"

`include "hwo_igu.v" 



module hwo_top
(
    // Clock and reset
    clk, rst,

    // Primary in
    if_insn,
	 
    // Primary out
    io_insn, if_stall
);

input clk;
input rst;

input	[31:0]	if_insn;
output [31:0]	io_insn;

// Internal wires
wire [5:0]  f_in_opc;
wire [4:0]  f_in_D;
wire [4:0]  f_in_A;
wire [4:0]  f_in_B;
wire [15:0] f_in_I;
wire [24:0] f_in_N;

wire [`IGU_ADDR_WIDTH-1:0] i_insn;
reg [`HWO_PPC_WIDTH-1:0] i_ppc;

reg [`HWO_INSN_TYPE_WIDTH-1:0] insn_type;

// Primary fields
assign f_in_opc = if_insn[31:26];
assign f_in_D   = if_insn[25:21];
assign f_in_A   = if_insn[20:16];
assign f_in_B   = if_insn[15:11];
assign f_in_I   = if_insn[15:0];
assign f_in_N   = if_insn[25:0];

// Index generator unit
hwo_igu hwo_igu_i(
    if_insn,
    i_insn
);

// Detect instruction type
always @(f_in_opc) 
    begin

    // A type
    if(f_in_opc == `OR1200_OR32_ALU)
        insn_type = `HWO_INSN_TYPE_A;

    // F type
    else if(
        f_in_opc == `OR1200_OR32_SFXX || 
        f_in_opc == `OR1200_OR32_SFXXI
    )
        insn_type = `HWO_INSN_TYPE_F;

    // B type
    else if(
        f_in_opc == `OR1200_OR32_J || 
        f_in_opc == `OR1200_OR32_JAL ||
        f_in_opc == `OR1200_OR32_BF ||
        f_in_opc == `OR1200_OR32_BNF
    )
        insn_type = `HWO_INSN_TYPE_B;

    // I type
    else if(
        f_in_opc[5:4] == 2'b10 ||
        f_in_opc == `OR1200_OR32_MOVHI ||
        f_in_opc == `OR1200_OR32_RFE
    )
        insn_type = `HWO_INSN_TYPE_I;

    // N type
    else 
        insn_type = `HWO_INSN_TYPE_N;
end

// Pseudo-PC (PPC)
always @(posedge clk)
    if (rst) begin
        i_ppc <= `HWO_PPC_WIDTH'd0;
    end else if (enable) begin
        i_ppc <= i_ppc + 1;
    end
end


endmodule
