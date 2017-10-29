// Config
// `define OBF_RND8
// `define OBF_CTRL_COUNTER

// Main
`define OBF_PPC_WIDTH 4
`define OBF_PPC_BUS 3:0

`define OBF_KEY_WIDTH 32
`define OBF_KEY_BUS 31:0

// Obfuscator enable counter
`define OBF_ENCNT_WIDTH 8

// LUT
`define OBF_INDEX_WIDTH 7
`define OBF_INDEX_BUS 6:0

`define LUT_ADDR_WIDTH 9
`define LUT_ADDR_BUS 8:0

`define LUT_OUT_WIDTH  16
`define LUT_OUT_BUS  15:0

`define LUT_SEL_WIDTH 2
`define LUT_SEL_BUS 1:0

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

