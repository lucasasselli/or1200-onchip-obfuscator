/*
    TODO:
        - F-type
        - S-type
*/

// synopsys translate_off
`include "timescale.v"
// synopsys translate_on
`include "or1200_defines.v"
`include "obf_defines.v"
`include "obf_igu.v"
`include "obf_lut.v"

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
wire obf_bypass;
wire obf_complete;
wire obf_init;
wire obf_rst;
wire [`OBF_KEY_WIDTH-1:0] key = `OBF_KEY_WIDTH'd0;

wire real_id_freeze = id_freeze & !io_stall;

//////////////////////////////////////////////////
// PSEUDO PROGRAM COUNTER (PPC)
//////////////////////////////////////////////////

reg [`OBF_PPC_WIDTH-1:0] ppc_i; // PPC output value

wire ppc_en = !obf_bypass & !real_id_freeze;
wire ppc_rst = obf_complete | obf_rst;
wire ppc_skip;

assign obf_init = (ppc_i == 0);

always @(posedge clk or `OR1200_RST_EVENT rst)
begin
    if (rst == `OR1200_RST_VALUE) begin
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
// SUBSTITUTION LUT
//////////////////////////////////////////////////


wire [`OBF_IGU_WIDTH-1:0] igu_i;
wire [`OBF_LUT_OUT_WIDTH-1:0] lut_out_sub;
wire [`OBF_LUT_OUT_WIDTH-1:0] lut_out_imm;

// Index generator unit
obf_igu obf_igu_i(
    saved_insn,
    igu_i
);

// Substitution LUT
obf_lut obf_lut_i(
    igu_i,
    ppc_i,
    key,
    lut_out_sub,
    lut_out_imm
);

//////////////////////////////////////////////////
// OBFUSCATED INSTRUCTION GENERATION
//////////////////////////////////////////////////

reg [31:0] obf_insn; // Obfuscated instruction

wire [5:0]  f_in_opc; 
wire [4:0]  f_in_D; 
wire [4:0]  f_in_A; 
wire [4:0]  f_in_B; 
wire [15:0] f_in_I; 

// Detect input instruction type
reg [`OBF_INSN_TYPE_WIDTH-1:0] f_in_type;
always @(f_in_opc) begin
    if(
        f_in_opc[5:4] == 2'b10 ||
        f_in_opc == `OR1200_OR32_MOVHI ||
        f_in_opc == `OR1200_OR32_RFE
    ) begin
        // I-type
        f_in_type = `OBF_INSN_TYPE_I;
    end
    else if(
        f_in_opc == `OR1200_OR32_MTSPR ||
        f_in_opc == `OR1200_OR32_SW ||
        f_in_opc == `OR1200_OR32_SH ||
        f_in_opc == `OR1200_OR32_SB
    ) begin
        // M-type
        f_in_type = `OBF_INSN_TYPE_M;
    end
    else if(
        f_in_opc == `OR1200_OR32_ALU
    ) begin
        // A-type
        f_in_type = `OBF_INSN_TYPE_A;
    end
    else begin
        // TODO Place holder
        f_in_type = `OBF_INSN_TYPE_N;
    end
end

// Primary input fields
assign f_in_opc         = saved_insn[31:26];
assign f_in_D           = saved_insn[25:21];
assign f_in_A           = saved_insn[20:16];
assign f_in_B           = saved_insn[15:11];
assign f_in_I           = (f_in_type == `OBF_INSN_TYPE_I) ? saved_insn[15:0] : {saved_insn[25:21], saved_insn[10:0]};

// Parse LUT output
wire [`OBF_INSN_TYPE_WIDTH-1:0] sub_type = lut_out_sub[`OBF_LUT_OUT_WIDTH-1:`OBF_LUT_OUT_WIDTH-`OBF_INSN_TYPE_WIDTH];
wire [11:0]                     sub_cmd  = lut_out_sub[12:1];
wire                            sub_last = lut_out_sub[0];

// Generate output fields using cmd
wire [5:0]  f_out_OPC0 = sub_cmd[11:6];
wire [3:0]  f_out_OPC1 = sub_cmd[11:8];
wire [3:0]  f_out_OPC2 = sub_cmd[7:4];
wire [4:0]  f_out_D    = sub_cmd[3] ? 5'b00000 : f_in_D;

wire [4:0]  f_out_A    = sub_cmd[2:1] == 2'b00 ? f_in_A:
                         sub_cmd[2:1] == 2'b01 ? f_in_B:
                         sub_cmd[2:1] == 2'b10 ? f_in_D:
                         5'b00000;

wire [4:0]  f_out_B    = sub_cmd[0] ? 5'b00000 : f_in_B;
wire [15:0] f_out_I    = sub_cmd[5] ? lut_out_imm : sub_cmd[4]? 16'd0 : f_in_I;

// Parse substitution command
always @(*) 
begin
    // Type-field
    case(sub_type)
       `OBF_INSN_TYPE_A: obf_insn <= {`OR1200_OR32_ALU, f_out_D, f_out_A, f_out_B, 1'b0, f_out_OPC1, 2'b00, f_out_OPC2};
       `OBF_INSN_TYPE_I: obf_insn <= {f_out_OPC0, f_out_D, f_out_A, f_out_I};
       `OBF_INSN_TYPE_M: obf_insn <= {f_out_OPC0, f_out_I[15:11], f_out_A, f_out_B, f_out_I[10:0]};
       `OBF_INSN_TYPE_N: obf_insn <= saved_insn;
    endcase
end

assign ppc_skip = (sub_type == `OBF_INSN_TYPE_I || sub_type == `OBF_INSN_TYPE_M) ? sub_cmd[5] : 1'b0;

assign obf_bypass = !obf_en | (obf_init & (if_stall)); // TODO Obf init is necessary?
assign obf_complete = sub_last & !real_id_freeze;

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
