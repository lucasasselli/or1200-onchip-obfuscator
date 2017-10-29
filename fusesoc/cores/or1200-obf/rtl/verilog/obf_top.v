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
output io_stall;
output reg io_no_more_dslot;

wire obf_init;
wire obf_rst;
wire obf_stop;
wire obf_last;
wire obf_en;

// Current IF insn and PC
wire [31:0] saved_insn;
wire [31:0] saved_pc;

// Bypass insn directly to output while IF is stalling
wire obf_bypass = obf_init & if_stall;

// Prevent feedback between io_stall and id_freeze
wire real_id_freeze = id_freeze & !io_stall;

// Enables counters (ppc and encnt)
wire cnt_en = !obf_bypass & !real_id_freeze & !obf_stop;

//////////////////////////////////////////////////
// CONTROL
//////////////////////////////////////////////////

wire ctrl_go = cnt_en & obf_last;

obf_keydec obf_keydec(
    .clk(clk),
    .rst(rst),
    .ctrl_go(ctrl_go),
    .obf_en(obf_en)
);

//////////////////////////////////////////////////
// PSEUDO PROGRAM COUNTER (PPC)
//////////////////////////////////////////////////

reg [`OBF_PPC_BUS] ppc_i; // PPC output value

wire ppc_en = cnt_en;
wire ppc_rst = obf_last | obf_rst;
wire ppc_skip;

assign obf_init = (ppc_i == 0);

always @(posedge clk or `OR1200_RST_EVENT rst)
begin
    if (rst == `OR1200_RST_VALUE) begin
        // System reset
        ppc_i <= 0;
    end
    else begin 
        if(obf_rst) begin 
            // Internal reset
            ppc_i <= 0;
        end
        else if(ppc_en) begin
            // PPC Enabled
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
        else begin
            // PPC Disabled
            ppc_i <= ppc_i;
        end
    end
end

//////////////////////////////////////////////////
// INPUT INSTRUCTION/PROGRAM COUNTER
//////////////////////////////////////////////////

reg [31:0] saved_insn_reg;
reg [31:0] saved_pc_reg;

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

obf_insngen obf_insngen(
    .ref_insn(saved_insn),
    .ppc(ppc_i),
    .obf_en(obf_en),
    .obf_insn(obf_insn),
    .obf_last(obf_last),
    .ppc_skip(ppc_skip)
);

//////////////////////////////////////////////////
// BRANCH DSLOT
//////////////////////////////////////////////////

reg purge;
reg [31:0] io_insn_reg;
wire io_void = (io_insn_reg[31:26] == `OR1200_OR32_NOP) & io_insn_reg[16]; 

// Prevents fecth module from fetching old instruction
assign obf_stop = io_no_more_dslot & if_stall;

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
        // No branch
        io_no_more_dslot <= 1'b0;
        purge <= 1'b0;
    end
end

//////////////////////////////////////////////////
// OUTPUTS
//////////////////////////////////////////////////

reg obf_flushable;
reg io_stall_reg;

assign obf_rst = (purge & obf_flushable) | id_flushpipe;

assign io_insn = obf_rst ? {`OR1200_OR32_NOP, 26'h041_0000} : io_insn_reg;
assign io_stall = obf_stop ? 1'b1 : io_stall_reg;

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

// Output
always @(posedge clk or `OR1200_RST_EVENT rst) 
begin
    if (rst == `OR1200_RST_VALUE) begin
        // System reset
        io_insn_reg <= {`OR1200_OR32_NOP, 26'h041_0000};
        io_pc <= 32'h00000000;
        io_stall_reg <= 1'b0;

        obf_flushable <= 1'b1;
    end
    else begin
        if (obf_rst) begin
            // Internal reset
            io_insn_reg <= {`OR1200_OR32_NOP, 26'h041_0000};
            io_pc <= 32'h00000000;
            io_stall_reg <= 1'b0;

            obf_flushable <= 1'b1;
        end
        else if (real_id_freeze) begin
            // ID stage frozen
            io_insn_reg <= io_insn;
            io_pc <= io_pc;
            io_stall_reg <= 1'b0;

            obf_flushable <= obf_flushable;
        end
        else if (obf_stop) begin
            // Allows new instruction to be fetched after branch
            io_insn_reg <= io_insn;
            io_pc <= io_pc;
            io_stall_reg <= 1'b0;

            obf_flushable <= obf_flushable;
        end
        else if (obf_bypass) begin
            // IF stage stalling
            io_insn_reg <= if_insn;
            io_pc <= if_pc;
            io_stall_reg <= 1'b1;

            obf_flushable <= 1'b1;
        end
        else begin
            // Obfusctor running
            io_insn_reg <= obf_insn;
            io_pc <= saved_pc;
            io_stall_reg <= 1'b0;

            obf_flushable <= obf_init;
        end
    end
end

endmodule
