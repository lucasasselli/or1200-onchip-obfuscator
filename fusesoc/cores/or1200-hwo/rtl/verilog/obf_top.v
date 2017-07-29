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
    if_insn, if_pc, id_freeze, if_stall, id_flushpipe, no_more_dslot, ex_branch_taken,

    // Outputs
    io_stall, io_insn, io_pc
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
input id_flushpipe;
input no_more_dslot;
input ex_branch_taken;
output reg io_stall;
output reg [31:0] io_insn;
output reg [31:0] io_pc;

wire obf_en = 1'b1; // Global obfuscator enable
wire obf_bypass;
wire obf_complete;
wire obf_init;
wire obf_rst_hard = id_flushpipe | no_more_dslot;
wire obf_rst_soft = ex_branch_taken;

//////////////////////////////////////////////////
// PSEUDO PROGRAM COUNTER (PPC)
//////////////////////////////////////////////////

reg [`OBF_PPC_WIDTH-1:0] ppc_i; // PPC output value

wire ppc_en = !obf_bypass & !id_freeze;
wire ppc_rst = obf_complete;

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
            ppc_i <= ppc_i + 1;
        end
    end
end

//////////////////////////////////////////////////
// INPUT INSTRUCTION 
//////////////////////////////////////////////////

reg [31:0] saved_insn_reg;

wire [31:0] saved_insn;

assign saved_insn = obf_init ? if_insn : saved_insn_reg;

// Stores the fetched instruction
always @(posedge clk or `OR1200_RST_EVENT rst) 
begin
    if (rst == `OR1200_RST_VALUE) begin
        // Reset
        saved_insn_reg <= {`OR1200_OR32_NOP, 26'h041_0000};
    end
    else begin
        if(obf_init)
            saved_insn_reg <= if_insn;
        else
            saved_insn_reg <= saved_insn;
    end
end

//////////////////////////////////////////////////
// SUBSTITUTION LUT
//////////////////////////////////////////////////


wire [`OBF_IGU_WIDTH-1:0] igu_i;
wire [`OBF_LUT_ADDR_WIDTH-1:0] lut_addr;
wire [`OBF_LUT_OUT_WIDTH-1:0] lut_out;

assign lut_addr = {igu_i, ppc_i};


// Index generator unit
obf_igu obf_igu_i(
    saved_insn,
    igu_i
);

// Substitution LUT
obf_lut obf_lut_i(
    lut_addr,
    lut_out
);

//////////////////////////////////////////////////
// OBFUSCATED INSTRUCTION GENERATION
//////////////////////////////////////////////////
/*
    TODO:
        - F-type
        - S-type
*/

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
    else begin
        // TODO Place holder
        f_in_type = `OBF_INSN_TYPE_N;
    end
end

// Primary input fields
assign  f_in_opc        = saved_insn[31:26];
assign f_in_D           = saved_insn[25:21];
assign f_in_A           = saved_insn[20:16];
assign f_in_B           = saved_insn[15:11];
assign f_in_I           = (f_in_type == `OBF_INSN_TYPE_I) ? saved_insn[15:0] : {saved_insn[25:21], saved_insn[10:0]};

// Parse LUT output
wire [`OBF_INSN_TYPE_WIDTH-1:0] sub_type = lut_out[`OBF_LUT_OUT_WIDTH-1:`OBF_LUT_OUT_WIDTH-`OBF_INSN_TYPE_WIDTH];
wire [15:0]                     sub_cmd  = lut_out[16:1];
wire                            sub_last = lut_out[0];

// Generate output fields using cmd
wire [5:0]  f_out_OPC0 = sub_cmd[15:10];
wire [3:0]  f_out_OPC1 = sub_cmd[15:12];
wire [3:0]  f_out_OPC2 = sub_cmd[11:8];
wire [4:0]  f_out_D    = sub_cmd[7] ? 5'b00000 : f_in_D;
wire [4:0]  f_out_A    = sub_cmd[6] ? 5'b00000 : f_in_A;

reg [4:0]  f_out_B;
always @(*)
begin
    if(f_in_type == `OBF_INSN_TYPE_M)
        f_out_B <= sub_cmd[5] ? 5'b00000 : f_in_B;
    else
        f_out_B <= sub_cmd[7] ? 5'b00000 : f_in_B;
end

reg [15:0]  f_out_I;
always @(*)
begin
    if(sub_cmd[9])
        // Cmd immediate
        if(sub_cmd[8])
            // Sign extended
            f_out_I <= {{11{sub_cmd[5]}}, sub_cmd[5:0]};
        else
            // Zero extended
            f_out_I <= {11'b0, sub_cmd[5:0]};
    else
        // Original immediate
        f_out_I <= f_in_I;
end

// Parse substitution command
always @(*) 
begin
    // Type-field
    case(sub_type)
       `OBF_INSN_TYPE_A: obf_insn <= {`OR1200_OR32_ALU, f_out_D, f_out_A, f_out_B, 1'b0, f_out_OPC1, 2'b00, f_out_OPC2};
       `OBF_INSN_TYPE_I: obf_insn <= {f_out_OPC0, f_out_D, f_out_A, f_out_I};
       `OBF_INSN_TYPE_M: obf_insn <= {f_out_OPC0, f_out_I[15:11], f_out_A, f_out_B, f_out_I[10:0]};
       `OBF_INSN_TYPE_N: obf_insn <= saved_insn;
       `OBF_INSN_TYPE_S: obf_insn <= {`OR1200_OR32_NOP, 26'h041_0001};
    endcase
end

assign obf_bypass = !obf_en | (obf_init & (if_stall)); 
assign obf_complete = sub_last;

//////////////////////////////////////////////////
// OUTPUTS
//////////////////////////////////////////////////
// TODO The ex_branch_taken as is doesn't make no sense

// Instruction output
always @(posedge clk or `OR1200_RST_EVENT rst) 
begin
    if (rst == `OR1200_RST_VALUE) begin
        // Reset
        io_insn <= {`OR1200_OR32_NOP, 26'h041_0000};
    end
    else begin
        if(obf_rst_hard & obf_init)
            io_insn <= {`OR1200_OR32_NOP, 26'h041_0000};
        else if (id_freeze)
            io_insn <= io_insn; // Re-latch old value
        else if (obf_rst_soft & obf_init)
            io_insn <= {`OR1200_OR32_NOP, 26'h041_0000}; 
        else if (obf_bypass)
            io_insn <= if_insn; // Obfuscator disabled
        else
            io_insn <= obf_insn; // Obfuscator active
        end
    end

// Stall request
always @(*) 
begin
    if (rst == `OR1200_RST_VALUE) begin
        // Reset
        io_stall <= 1'b0;
    end
    else begin
        if (id_freeze)
            io_stall <= io_stall;
        else if (obf_bypass)
            io_stall <= 1'b0;
        else
            io_stall <= !obf_complete;
        end
    end

// Program counter
always @(posedge clk or `OR1200_RST_EVENT rst) 
begin
    if (rst == `OR1200_RST_VALUE) begin
        // Reset
        io_pc <= 32'd0;
    end
    else begin
        if(id_freeze)
            io_pc <= io_pc;
        else
            io_pc <= if_pc;
        end
    end
endmodule
