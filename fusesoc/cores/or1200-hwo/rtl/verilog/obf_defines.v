// Main
`define OBF_PPC_WIDTH 2
`define OBF_CMD_WIDTH 16

// LUT address fields
`define OBF_IGU_WIDTH 7
`define OBF_SUB_WIDTH 2

// LUT
/* `define OBF_LUT_ADDR_WIDTH OBF_SUB_WIDTH+OBF_IGU_WIDTH */
/* `define OBF_LUT_OUT_WIDTH OBF_INSN_TYPE_WIDTH + OBF_CMD_WIDTH */
`define OBF_LUT_ADDR_WIDTH 9
`define OBF_LUT_OUT_WIDTH  20

// Instruction types
`define OBF_INSN_TYPE_WIDTH 3
`define OBF_INSN_TYPE_N  3'b000 // Null type (passthrough)
`define OBF_INSN_TYPE_A  3'b001 // ALU
`define OBF_INSN_TYPE_I  3'b010 // Immediate
`define OBF_INSN_TYPE_B  3'b011 // Branch
`define OBF_INSN_TYPE_F  3'b100 // Flag
`define OBF_INSN_TYPE_S  3'b101 // System
`define OBF_INSN_TYPE_M  3'b110 // Memory




