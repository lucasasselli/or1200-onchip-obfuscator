`include "obf_defines.v"

module obf_lut(
    index,
    ppc,
    key,
    out_sub,
    out_imm
);

input [`OBF_IGU_WIDTH-1:0] index;
input [`OBF_PPC_WIDTH-1:0] ppc;
input [`OBF_KEY_WIDTH-1:0] key;
output [`OBF_LUT_OUT_WIDTH-1:0] out_sub;
output [`OBF_LUT_OUT_WIDTH-1:0] out_imm;

reg [`OBF_LUT_ADDR_WIDTH-1:0] addr_start;
wire [`OBF_LUT_ADDR_WIDTH-1:0] addr;

reg [`OBF_LUT_OUT_WIDTH-1:0] lut [6:0];

initial begin
    lut[0] = {`OBF_INSN_TYPE_N, 13'b000000000000_1}; // Any
    lut[1] = {`OBF_INSN_TYPE_I, 13'b100111_01_1_00_1_0}; // l.add -> l.addi r0,rA,0
    lut[2] = {`OBF_INSN_TYPE_A, 13'b0000_0001_0_10_0_0}; // l.add -> l.addc rD,r0,rB
    lut[3] = {`OBF_INSN_TYPE_A, 13'b0000_0101_1_10_1_1}; // l.add -> l.xor r0,r0,r0
    lut[4] = {`OBF_INSN_TYPE_I, 13'b100111_01_1_00_1_0}; // l.and -> l.addi r0,rA,0
    lut[5] = {`OBF_INSN_TYPE_A, 13'b0000_0001_0_10_0_0}; // l.and -> l.addc rD,r0,rB
    lut[6] = {`OBF_INSN_TYPE_A, 13'b0000_0101_1_10_1_1}; // l.and -> l.xor r0,r0,r0
    end

// Address generation
always @(index) begin
    case(index)
        //l.add
        `OBF_IGU_WIDTH'd64:  addr_start <= `OBF_LUT_ADDR_WIDTH'd1;
        default:             addr_start <= `OBF_LUT_ADDR_WIDTH'd0;
    endcase
end

assign addr = addr_start + ppc;
assign out_sub = lut[addr];
assign out_imm = lut[addr+1];

endmodule
