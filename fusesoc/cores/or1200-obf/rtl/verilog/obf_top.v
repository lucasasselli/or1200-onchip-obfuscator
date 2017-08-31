// synopsys translate_off
`include "timescale.v"
// synopsys translate_on
`include "or1200_defines.v"
`include "obf_defines.v"

module obf_top(
    // Clock and Reset
    clk, rst,

    // Inputs
    if_insn, if_pc, id_freeze, if_stall, id_flushpipe, ex_branch_taken, id_void,

    // Outputs
    if_stall_req, io_insn, io_pc, io_stall, io_no_more_dslot
);


//////////////////////////////////////////////////
// I/O 
//////////////////////////////////////////////////

input clk;
input rst;
input [31:0] if_insn;
input [31:0] if_pc;
input if_stall;
input id_freeze;
input id_void;
input id_flushpipe;
input ex_branch_taken;
output reg if_stall_req;
output [31:0] io_insn;
output reg [31:0] io_pc;
output reg io_stall;
output reg io_no_more_dslot;

wire obf_en = 1'b1; // Global obfuscator enable
wire obf_init;
wire obf_rst;
wire obf_last;
wire [`OBF_KEY_WIDTH-1:0] obf_key = `OBF_KEY_WIDTH'd0;

wire obf_bypass = !obf_en | (obf_init & (if_stall)); // TODO Obf init is necessary?
wire real_id_freeze = id_freeze & !io_stall;

//////////////////////////////////////////////////
// PSEUDO PROGRAM COUNTER (PPC)
//////////////////////////////////////////////////

reg [`OBF_PPC_WIDTH-1:0] ppc_i; // PPC output value

wire ppc_en = !obf_bypass & !real_id_freeze;
wire ppc_rst = obf_last | obf_rst;
wire ppc_skip;

assign obf_init = (ppc_i == 0);

always @(posedge clk or `OR1200_RST_EVENT rst)
begin
    if (rst == `OR1200_RST_VALUE | obf_rst) begin
        // Reset
        ppc_i <= 0;
    end
    else if(ppc_en) begin
        if(ppc_rst) begin
            // Substitution completed
            ppc_i <= 0;
        end
        else begin
            // Substitution running
            if(ppc_skip)
                // Skip immediate field
                ppc_i <= ppc_i + 2;
            else
                ppc_i <= ppc_i + 1;
        end
    end
end

//////////////////////////////////////////////////
// INPUT INSTRUCTION/PROGRAM COUNTER
//////////////////////////////////////////////////

reg [31:0] saved_insn_reg;
reg [31:0] saved_pc_reg;

wire [31:0] saved_insn;
wire [31:0] saved_pc;

assign saved_insn = obf_init ? if_insn : saved_insn_reg;
assign saved_pc = obf_init ? if_pc : saved_pc_reg;

// Stores the fetched instruction
always @(posedge clk or `OR1200_RST_EVENT rst) 
begin
    if (rst == `OR1200_RST_VALUE) begin
        // Reset
        saved_insn_reg <= {`OR1200_OR32_NOP, 26'h041_0000};
    end
    else begin
        if(obf_init) begin
            saved_insn_reg <= if_insn;
            saved_pc_reg <= if_pc;
        end
        else begin
            saved_insn_reg <= saved_insn;
            saved_pc_reg <= saved_pc_reg;
        end
    end
end

//////////////////////////////////////////////////
// OBFUSCATED INSTRUCTION GENERATOR
//////////////////////////////////////////////////

wire [31:0] obf_insn;

obf_insngen obf_insngen_i(
    saved_insn,
    ppc_i,
    obf_key,
    obf_insn,
    obf_last,
    ppc_skip
);


//////////////////////////////////////////////////
// BRANCH DSLOT
//////////////////////////////////////////////////

reg purge;
reg [31:0] io_insn_reg;
wire io_void = (io_insn_reg[31:26] == `OR1200_OR32_NOP) & io_insn_reg[16]; 

always @(*) begin
    if(ex_branch_taken) begin
        if(io_void & id_void) begin
            // dslot not yet fetched
            io_no_more_dslot <= 1'b0;
            purge <= 1'b0;
        end
        else if(!io_void & id_void) begin
            // dslot latched by obfuscator stage
            io_no_more_dslot <= 1'b1;
            purge <= 1'b0;
        end
        else if(io_void & !id_void) begin
            // dslot latched by decode stage (obfuscator void)
            io_no_more_dslot <= 1'b1;
            purge <= 1'b0;
        end
        else begin
            // dslot latched by decode stage (obfuscator not void)
            io_no_more_dslot <= 1'b1;
            purge <= 1'b1;
        end
    end
    else begin
        io_no_more_dslot <= 1'b0;
        purge <= 1'b0;
    end
end

//////////////////////////////////////////////////
// OUTPUTS
//////////////////////////////////////////////////

reg obf_flushable;
assign obf_rst = purge & obf_flushable; // TODO: flushpipe
assign io_insn = purge & obf_flushable ? {`OR1200_OR32_NOP, 26'h041_0000} : io_insn_reg;

// Instruction output
always @(posedge clk or `OR1200_RST_EVENT rst) 
begin
    if (rst == `OR1200_RST_VALUE | obf_rst) begin
        // Reset
        io_insn_reg <= {`OR1200_OR32_NOP, 26'h041_0000};
        io_pc <= 32'h00000000;
        obf_flushable <= 1'b1;
    end
    else begin
        if (real_id_freeze) begin
            // id stage frozen
            io_insn_reg <= io_insn;
            io_pc <= io_pc;
            obf_flushable <= obf_flushable;
        end
        else if (obf_bypass) begin
            // Obfuscator disabled or if stage stalling
            io_insn_reg <= if_insn;
            io_pc <= if_pc;
            obf_flushable <= 1'b1;
        end
        else begin
            // Obfusctor running
            io_insn_reg <= obf_insn;
            io_pc <= saved_pc;
            obf_flushable <= obf_init;
        end
    end
end

// Stall request
always @(*) 
begin
    if (rst == `OR1200_RST_VALUE) begin
        // Reset
        if_stall_req <= 1'b0;
    end
    else begin
        if(if_stall) begin
            // If fetch stage is stalling no action is required
            if_stall_req <= 1'b0;
        end
        else begin
            if (obf_bypass | obf_rst)
                // Obfuscator disabled or if stage stalling
                if_stall_req <= real_id_freeze;
            else
                // Obfuscator running
                if_stall_req <= (!obf_init & !io_no_more_dslot) | real_id_freeze;
            end
        end
    end

// Obfuscator stall
always @(posedge clk or `OR1200_RST_EVENT rst) 
begin
    if (rst == `OR1200_RST_VALUE) begin
        // Reset
        io_stall <= 1'b0;
    end
    else begin
        if(real_id_freeze)
            // If id stage is frozen there is no need to notify stall
            io_stall <= 1'b0;
        else if(!obf_bypass)
            // If obfuscator is running no stall is issued
            io_stall <= 1'b0;
        else
            // Other
            io_stall <= if_stall;
        end
    end
endmodule
