`include "obf_defines.v"

module obf_lut(
    lut_addr,
    lut_out
);

input [`OBF_LUT_ADDR_WIDTH-1:0] lut_addr;
output reg [`OBF_LUT_OUT_WIDTH-1:0] lut_out;

always @(lut_addr)
    case (lut_addr)
        // l.add
        {`OBF_IGU_WIDTH'd64,`OBF_SUB_WIDTH'd0}: lut_out <= {`OBF_INSN_TYPE_A, 16'b0000_0000_101_00_000, 1'b0}; // l.add r0, rA, r0
        {`OBF_IGU_WIDTH'd64,`OBF_SUB_WIDTH'd1}: lut_out <= {`OBF_INSN_TYPE_A, 16'b0000_0001_010_00_000, 1'b0}; // l.addc rD, r0, rB
        {`OBF_IGU_WIDTH'd64,`OBF_SUB_WIDTH'd2}: lut_out <= {`OBF_INSN_TYPE_A, 16'b0000_0101_111_00_000, 1'b1}; // l.xor r0, r0, r0
        // l.add
        /* {`OBF_IGU_WIDTH'd64,`OBF_SUB_WIDTH'd0}: lut_out <= {`OBF_INSN_TYPE_S, 16'd0, 1'b0}; */
        /* {`OBF_IGU_WIDTH'd64,`OBF_SUB_WIDTH'd1}: lut_out <= {`OBF_INSN_TYPE_N, 16'd0, 1'b1}; */
        default: lut_out <= {`OBF_INSN_TYPE_N, 16'd0, 1'b1};
    endcase
endmodule
