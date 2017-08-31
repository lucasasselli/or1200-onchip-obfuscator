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

reg [`OBF_LUT_ADDR_WIDTH-1:0] lut0_pointer;
wire [`OBF_LUT_ADDR_WIDTH-1:0] lut0_addr;

reg [`OBF_LUT_OUT_WIDTH-1:0] lut0 [101:0];

initial begin
    lut0[0] = 16'b0000000000000001;
    lut0[1] = 16'b0101001110111100;
    lut0[2] = 16'b0010000000100001;
    lut0[3] = 16'b0000000000000000;
    lut0[4] = 16'b0010000001111111;
    lut0[5] = 16'b0010000000011110;
    lut0[6] = 16'b0101010000000001;
    lut0[7] = 16'b0010000010100010;
    lut0[8] = 16'b0101010110011100;
    lut0[9] = 16'b0010000000101010;
    lut0[10] = 16'b0101010010111101;
    lut0[11] = 16'b0000000000000000;
    lut0[12] = 16'b0010001110011111;
    lut0[13] = 16'b0101010111000000;
    lut0[14] = 16'b1111111111111111;
    lut0[15] = 16'b0101010100011100;
    lut0[16] = 16'b0101010111011100;
    lut0[17] = 16'b1111111111111111;
    lut0[18] = 16'b0010000010001010;
    lut0[19] = 16'b0101010111001000;
    lut0[20] = 16'b1111111111111111;
    lut0[21] = 16'b0010000010111111;
    lut0[22] = 16'b0101011101000000;
    lut0[23] = 16'b0000000000011000;
    lut0[24] = 16'b0101011101001001;
    lut0[25] = 16'b0000000000011000;
    lut0[26] = 16'b0101011101000000;
    lut0[27] = 16'b0000000000010000;
    lut0[28] = 16'b0101011101001001;
    lut0[29] = 16'b0000000000010000;
    lut0[30] = 16'b0101010011000001;
    lut0[31] = 16'b1111111111111111;
    lut0[32] = 16'b0101010110100001;
    lut0[33] = 16'b0000000000000000;
    lut0[34] = 16'b0100001100111101;
    lut0[35] = 16'b0101000110000000;
    lut0[36] = 16'b0010001110001011;
    lut0[37] = 16'b0101001000000000;
    lut0[38] = 16'b0010011110001011;
    lut0[39] = 16'b0101001010000000;
    lut0[40] = 16'b0010000110001011;
    lut0[41] = 16'b0000000000000000;
    lut0[42] = 16'b0010000110001011;
    lut0[43] = 16'b0101000010000001;
    lut0[44] = 16'b0101000100000001;
    lut0[45] = 16'b0000000000000000;
    lut0[46] = 16'b0101010010111101;
    lut0[47] = 16'b0000000000000000;
    lut0[48] = 16'b0010000010111111;
    lut0[49] = 16'b0101010111000000;
    lut0[50] = 16'b1111111111111111;
    lut0[51] = 16'b0101010110011100;
    lut0[52] = 16'b0010010110011110;
    lut0[53] = 16'b0101010111011100;
    lut0[54] = 16'b1111111111111111;
    lut0[55] = 16'b0010000001101010;
    lut0[56] = 16'b0101010111001000;
    lut0[57] = 16'b1111111111111111;
    lut0[58] = 16'b0010000010111111;
    lut0[59] = 16'b0010000010100010;
    lut0[60] = 16'b0101010110011100;
    lut0[61] = 16'b0101010111011100;
    lut0[62] = 16'b0000000000011111;
    lut0[63] = 16'b0101001111011100;
    lut0[64] = 16'b0000000000100001;
    lut0[65] = 16'b0010000100011010;
    lut0[66] = 16'b0101011100001000;
    lut0[67] = 16'b0010000010001010;
    lut0[68] = 16'b0010000010111111;
    lut0[69] = 16'b0010000010100010;
    lut0[70] = 16'b0101010110011100;
    lut0[71] = 16'b0010000100001010;
    lut0[72] = 16'b0010000010111111;
    lut0[73] = 16'b0010000010100010;
    lut0[74] = 16'b0101010110011100;
    lut0[75] = 16'b0010010100000010;
    lut0[76] = 16'b0010000010111111;
    lut0[77] = 16'b0010000010100010;
    lut0[78] = 16'b0101010110011100;
    lut0[79] = 16'b0010001100000010;
    lut0[80] = 16'b0010000010111111;
    lut0[81] = 16'b0000000000000000;
    lut0[82] = 16'b0010000110111111;
    lut0[83] = 16'b0000000000000000;
    lut0[84] = 16'b0101011100111101;
    lut0[85] = 16'b0010000010100010;
    lut0[86] = 16'b0101010100011100;
    lut0[87] = 16'b0010000110011110;
    lut0[88] = 16'b0010000010101010;
    lut0[89] = 16'b0101010010111101;
end

// Address generation
always @(index) begin
    case(index)
        `OBF_IGU_WIDTH'd64: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd1;
        `OBF_IGU_WIDTH'd65: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd3;
        `OBF_IGU_WIDTH'd27: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd5;
        `OBF_IGU_WIDTH'd28: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd7;
        `OBF_IGU_WIDTH'd67: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd11;
        `OBF_IGU_WIDTH'd29: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd13;
        `OBF_IGU_WIDTH'd60: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd22;
        `OBF_IGU_WIDTH'd63: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd22;
        `OBF_IGU_WIDTH'd58: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd26;
        `OBF_IGU_WIDTH'd62: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd30;
        `OBF_IGU_WIDTH'd59: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd32;
        `OBF_IGU_WIDTH'd61: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd32;
        `OBF_IGU_WIDTH'd71: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd33;
        `OBF_IGU_WIDTH'd76: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd33;
        `OBF_IGU_WIDTH'd24: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd35;
        `OBF_IGU_WIDTH'd23: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd37;
        `OBF_IGU_WIDTH'd26: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd39;
        `OBF_IGU_WIDTH'd25: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd41;
        `OBF_IGU_WIDTH'd22: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd43;
        `OBF_IGU_WIDTH'd21: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd44;
        `OBF_IGU_WIDTH'd33: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd45;
        `OBF_IGU_WIDTH'd6: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd47;
        `OBF_IGU_WIDTH'd48: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd45;
        `OBF_IGU_WIDTH'd68: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd45;
        `OBF_IGU_WIDTH'd30: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd49;
        `OBF_IGU_WIDTH'd75: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd45;
        `OBF_IGU_WIDTH'd37: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd59;
        `OBF_IGU_WIDTH'd57: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd45;
        `OBF_IGU_WIDTH'd72: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd45;
        `OBF_IGU_WIDTH'd34: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd69;
        `OBF_IGU_WIDTH'd74: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd45;
        `OBF_IGU_WIDTH'd36: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd73;
        `OBF_IGU_WIDTH'd73: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd45;
        `OBF_IGU_WIDTH'd35: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd77;
        `OBF_IGU_WIDTH'd66: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd81;
        `OBF_IGU_WIDTH'd55: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd45;
        `OBF_IGU_WIDTH'd69: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd83;
        `OBF_IGU_WIDTH'd31: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd85;
        default:            lut0_pointer = `OBF_LUT_ADDR_WIDTH'd0;
    endcase
end

assign lut0_addr = lut0_pointer+ppc;
assign out_sub = lut0[lut0_addr];
assign out_imm = lut0[lut0_addr+1];

endmodule
