// WARNING:
// This code was generated by a tool. DO NOT MODIFY!

`include "obf_defines.v"

module obf_lut0(
    addr,
    out_sub,
    out_imm
);

input [`OBF_LUT_ADDR_WIDTH-1:0] addr;
output [`OBF_LUT_OUT_WIDTH-1:0] out_sub;
output [`OBF_LUT_OUT_WIDTH-1:0] out_imm;

reg [`OBF_LUT_OUT_WIDTH-1:0] lut [0:129];

initial begin
	lut[0] = 16'b0000000000000001;
	lut[1] = 16'b0101001110111100;
	lut[2] = 16'b0010000000100001;
	lut[3] = 16'b0000000000000000;
	lut[4] = 16'b0010000001111111;
	lut[5] = 16'b0010000000011110;
	lut[6] = 16'b0101010000000001;
	lut[7] = 16'b0010000010100010;
	lut[8] = 16'b0101010110011100;
	lut[9] = 16'b0010000000101010;
	lut[10] = 16'b0101010010111101;
	lut[11] = 16'b0000000000000000;
	lut[12] = 16'b0010001110011111;
	lut[13] = 16'b0101010111000000;
	lut[14] = 16'b1111111111111111;
	lut[15] = 16'b0101010100011100;
	lut[16] = 16'b0101010111011100;
	lut[17] = 16'b1111111111111111;
	lut[18] = 16'b0010000010001010;
	lut[19] = 16'b0101010111001000;
	lut[20] = 16'b1111111111111111;
	lut[21] = 16'b0010000010111111;
	lut[22] = 16'b0101011101000000;
	lut[23] = 16'b0000000000011000;
	lut[24] = 16'b0101011101001001;
	lut[25] = 16'b0000000000011000;
	lut[26] = 16'b0101011101000000;
	lut[27] = 16'b0000000000010000;
	lut[28] = 16'b0101011101001001;
	lut[29] = 16'b0000000000010000;
	lut[30] = 16'b0101010011000001;
	lut[31] = 16'b1111111111111111;
	lut[32] = 16'b0101010110100001;
	lut[33] = 16'b0000000000000000;
	lut[34] = 16'b0100001100111101;
	lut[35] = 16'b0101000110000000;
	lut[36] = 16'b0010001110001011;
	lut[37] = 16'b0101001000000000;
	lut[38] = 16'b0010011110001011;
	lut[39] = 16'b0101001010000000;
	lut[40] = 16'b0010000110001011;
	lut[41] = 16'b0000000000000000;
	lut[42] = 16'b0010000110001011;
	lut[43] = 16'b0101000010000001;
	lut[44] = 16'b0101000100000001;
	lut[45] = 16'b0000000000000000;
	lut[46] = 16'b0101010010111101;
	lut[47] = 16'b0000000000000000;
	lut[48] = 16'b0010000010111111;
	lut[49] = 16'b0101010111000000;
	lut[50] = 16'b1111111111111111;
	lut[51] = 16'b0101010110011100;
	lut[52] = 16'b0010010110011110;
	lut[53] = 16'b0101010111011100;
	lut[54] = 16'b1111111111111111;
	lut[55] = 16'b0010000001101010;
	lut[56] = 16'b0101010111001000;
	lut[57] = 16'b1111111111111111;
	lut[58] = 16'b0010000010111111;
	lut[59] = 16'b0010000010100010;
	lut[60] = 16'b0101010110011100;
	lut[61] = 16'b0101010111011100;
	lut[62] = 16'b0000000000011111;
	lut[63] = 16'b0101001111011100;
	lut[64] = 16'b0000000000100001;
	lut[65] = 16'b0010000100011010;
	lut[66] = 16'b0101011100001000;
	lut[67] = 16'b0010000010001010;
	lut[68] = 16'b0010000010111111;
	lut[69] = 16'b0000000000000000;
	lut[70] = 16'b0010000111111111;
	lut[71] = 16'b0101010110011100;
	lut[72] = 16'b1000000000110000;
	lut[73] = 16'b0010000010111111;
	lut[74] = 16'b1000110100010101;
	lut[75] = 16'b0101010110011100;
	lut[76] = 16'b1000101100110000;
	lut[77] = 16'b0010000010111111;
	lut[78] = 16'b1000010100010101;
	lut[79] = 16'b0101010100011100;
	lut[80] = 16'b1000001100110000;
	lut[81] = 16'b0010000010111111;
	lut[82] = 16'b1000110000010101;
	lut[83] = 16'b0101010110011100;
	lut[84] = 16'b1000101000110000;
	lut[85] = 16'b0010000010111111;
	lut[86] = 16'b1000010000010101;
	lut[87] = 16'b0101010100011100;
	lut[88] = 16'b1000001000110000;
	lut[89] = 16'b0010000010111111;
	lut[90] = 16'b1000101100010101;
	lut[91] = 16'b0101010110011100;
	lut[92] = 16'b1000110100110000;
	lut[93] = 16'b0010000010111111;
	lut[94] = 16'b1000001100010101;
	lut[95] = 16'b0101010100011100;
	lut[96] = 16'b1000010100110000;
	lut[97] = 16'b0010000010111111;
	lut[98] = 16'b1000101000010101;
	lut[99] = 16'b0101010110011100;
	lut[100] = 16'b1000110000110000;
	lut[101] = 16'b0010000010111111;
	lut[102] = 16'b1000001000010101;
	lut[103] = 16'b0101010100011100;
	lut[104] = 16'b1000010000110000;
	lut[105] = 16'b0010000010111111;
	lut[106] = 16'b0101010110011100;
	lut[107] = 16'b1000000100110000;
	lut[108] = 16'b0010000010111111;
	lut[109] = 16'b0010000010100010;
	lut[110] = 16'b0101010110011100;
	lut[111] = 16'b0010000100001010;
	lut[112] = 16'b0010000010111111;
	lut[113] = 16'b0010000010100010;
	lut[114] = 16'b0101010110011100;
	lut[115] = 16'b0010010100001010;
	lut[116] = 16'b0010000010111111;
	lut[117] = 16'b0010000010100010;
	lut[118] = 16'b0101010110011100;
	lut[119] = 16'b0010001100001010;
	lut[120] = 16'b0010000010111111;
	lut[121] = 16'b0000000000000000;
	lut[122] = 16'b0010000110111111;
	lut[123] = 16'b0000000000000000;
	lut[124] = 16'b0101011100111101;
	lut[125] = 16'b0010000010100010;
	lut[126] = 16'b0101010100011100;
	lut[127] = 16'b0010000110011110;
	lut[128] = 16'b0010000010101010;
	lut[129] = 16'b0101010010111101;

end

assign out_sub = lut[addr];
assign out_imm = lut[addr+1];

endmodule
