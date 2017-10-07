/*
    OBFUSCATED INSTRUCTION GENERATOR

    TODO:
    - F-type
    - FI-type
    - B-type
    - S-type
*/

`include "or1200_defines.v"
`include "obf_defines.v"

module obf_insngen(
    ref_insn,
    ppc_i,
    obf_key,
    obf_en,
    obf_insn,
    obf_last,
    obf_skip
);

input [31:0] ref_insn;
input [`OBF_PPC_WIDTH-1:0] ppc_i;
input [`OBF_KEY_WIDTH-1:0] obf_key;
input obf_en;
output reg [31:0] obf_insn;
output obf_last;
output obf_skip;

//////////////////////////////////////////////////
// SUBSTITUTION LUT
//////////////////////////////////////////////////

wire [`OBF_IGU_WIDTH-1:0] igu_i;
wire [`OBF_LUT_OUT_WIDTH-1:0] lut_out_sub;
wire [`OBF_LUT_OUT_WIDTH-1:0] lut_out_imm;

// Index generator unit
obf_igu obf_igu_i(
    ref_insn,
    igu_i
);

// Substitution LUT
obf_lut_top obf_lut_top_i(
    igu_i,
    ppc_i,
    obf_key,
    lut_out_sub,
    lut_out_imm
);

//////////////////////////////////////////////////
// OBFUSCATED INSTRUCTION GENERATION
//////////////////////////////////////////////////

// Instruction operand fields
reg [`OBF_INSN_TYPE_WIDTH-1:0] f_in_type;

wire [5:0] f_in_opc = ref_insn[31:26];
wire [4:0] f_in_D   = ref_insn[25:21];
wire [4:0] f_in_A   = ref_insn[20:16];
wire [4:0] f_in_B   = ref_insn[15:11];
wire [15:0] f_in_I  = (f_in_type == `OBF_INSN_TYPE_I) ? ref_insn[15:0] : {ref_insn[25:21], ref_insn[10:0]};

// Detect input instruction type
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
    else if(
        f_in_opc == `OR1200_OR32_SFXX
    ) begin
        // F-type
        f_in_type = `OBF_INSN_TYPE_F;
    end
    else if(
        f_in_opc == `OR1200_OR32_SFXXI
    ) begin
        // FI-type
        f_in_type = `OBF_INSN_TYPE_FI;
    end
    else begin
        // TODO Place holder
        f_in_type = `OBF_INSN_TYPE_N;
    end
end

// Parse LUT output
wire [`OBF_INSN_TYPE_WIDTH-1:0] sw_type = lut_out_sub[`OBF_LUT_OUT_WIDTH-1:`OBF_LUT_OUT_WIDTH-`OBF_INSN_TYPE_WIDTH];
wire [11:0]                     sw_cmd  = lut_out_sub[12:1];
wire                            sw_last = lut_out_sub[0];

// Generate output fields using cmd
wire [5:0]  f_out_OPC   = sw_cmd[11:6];
wire [3:0]  f_out_AOPC1 = sw_cmd[11:8];
wire [3:0]  f_out_AOPC2 = sw_cmd[7:4];
wire [4:0]  f_out_FOPC  = sw_cmd[11:7];
wire [4:0]  f_out_D     = sw_cmd[3] ? 5'b00000 : f_in_D;

wire [4:0]  f_out_A     = sw_cmd[2:1] == 2'b00 ? f_in_A:
                          sw_cmd[2:1] == 2'b01 ? f_in_B:
                          sw_cmd[2:1] == 2'b10 ? f_in_D:
                          5'b00000;

wire [4:0]  f_out_B     = (sw_type == `OBF_INSN_TYPE_F || sw_type == `OBF_INSN_TYPE_FI) ?
                          sw_cmd[4:3] == 2'b00 ? f_in_B:
                          sw_cmd[4:3] == 2'b01 ? f_in_A:
                          5'b00000: 
                          sw_cmd[0] ? 5'b00000 : f_in_B;

wire [15:0] f_out_I    = sw_cmd[5] ? lut_out_imm : sw_cmd[4]? 16'd0 : f_in_I;

// Parse substitution command
always @(*) 
begin
    if(obf_en) begin
        // Type-field
        case(sw_type)
           `OBF_INSN_TYPE_N: obf_insn = ref_insn;
           `OBF_INSN_TYPE_A: obf_insn = {`OR1200_OR32_ALU, f_out_D, f_out_A, f_out_B, 1'b0, f_out_AOPC1, 2'b00, f_out_AOPC2};
           `OBF_INSN_TYPE_I: obf_insn = {f_out_OPC, f_out_D, f_out_A, f_out_I};
           `OBF_INSN_TYPE_M: obf_insn = {f_out_OPC, f_out_I[15:11], f_out_A, f_out_B, f_out_I[10:0]};
           `OBF_INSN_TYPE_F: obf_insn = {`OR1200_OR32_SFXX, f_out_FOPC, f_out_A, f_out_B, 11'd0};
           `OBF_INSN_TYPE_FI: obf_insn = {`OR1200_OR32_SFXXI, f_out_FOPC, f_out_A, f_out_I};
           default: obf_insn = ref_insn; // TODO: Add some debug output
        endcase
    end 
    else begin
        // Obfuscator disabled
        obf_insn = ref_insn;
    end
end

assign obf_skip = (sw_type == `OBF_INSN_TYPE_I || sw_type == `OBF_INSN_TYPE_M) & obf_en ? sw_cmd[5] : 1'b0;
assign obf_last = obf_en ? sw_last : 1'd1;

endmodule
