// Config
`define OBF_RND8
`define OBF_CTRL_COUNTER

// Main
`define OBF_PPC_WIDTH 4
`define OBF_CMD_WIDTH 16
`define OBF_KEY_WIDTH 2

// Obfuscator enable counter
`define OBF_ENCNT_WIDTH 8

// LUT address fields
`define OBF_IGU_WIDTH 7
`define OBF_SUB_WIDTH 2 // TODO Better addressing mode

// LUT
`define OBF_LUT_ADDR_WIDTH 9
`define OBF_LUT_OUT_WIDTH  16

// Instruction types
`define OBF_INSN_TYPE_WIDTH 3
`define OBF_INSN_TYPE_N  3'b000 // Null type (passthrough)
`define OBF_INSN_TYPE_A  3'b001 // ALU
`define OBF_INSN_TYPE_I  3'b010 // Immediate
`define OBF_INSN_TYPE_M  3'b011 // Memory
`define OBF_INSN_TYPE_F  3'b100 // Flag
`define OBF_INSN_TYPE_FI 3'b101 // Flag immediate
`define OBF_INSN_TYPE_S  3'b110 // System
`define OBF_INSN_TYPE_B  3'b111 // Branch

