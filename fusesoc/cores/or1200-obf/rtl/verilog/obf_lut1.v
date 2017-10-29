// WARNING:
// This code was generated by a tool. DO NOT MODIFY!

`include "obf_defines.v"

module obf_lut1(
    addr,
    out_sub,
    out_imm
);

input [`LUT_ADDR_BUS] addr;
output [`LUT_OUT_BUS] out_sub;
output [`LUT_OUT_BUS] out_imm;

reg [`LUT_OUT_BUS] lut [0:59];

initial begin
	lut[0] = 16'b0000000000000001;
	lut[1] = 16'b0000000000000000;
	lut[2] = 16'b0101010010111101;
	lut[3] = 16'b0000000000000000;
	lut[4] = 16'b0100001100111101;
	lut[5] = 16'b0010000010100010;
	lut[6] = 16'b0101010110011100;
	lut[7] = 16'b0010000000001010;
	lut[8] = 16'b0100001100111101;
	lut[9] = 16'b0000000000000000;
	lut[10] = 16'b0010000001111111;
	lut[11] = 16'b0000000000000000;
	lut[12] = 16'b0010011110011111;
	lut[13] = 16'b0010000010100010;
	lut[14] = 16'b0101010100011100;
	lut[15] = 16'b0010000001101010;
	lut[16] = 16'b0010000010111111;
	lut[17] = 16'b0101010011000001;
	lut[18] = 16'b0000000011111111;
	lut[19] = 16'b0101011101000000;
	lut[20] = 16'b0000000000010000;
	lut[21] = 16'b0101011101001001;
	lut[22] = 16'b0000000000010000;
	lut[23] = 16'b0010000110100011;
	lut[24] = 16'b0000000000000000;
	lut[25] = 16'b0000000000000001;
	lut[26] = 16'b0101000110000000;
	lut[27] = 16'b0101011101001000;
	lut[28] = 16'b0000000000011000;
	lut[29] = 16'b0101011101001001;
	lut[30] = 16'b0000000000011000;
	lut[31] = 16'b0101001000000000;
	lut[32] = 16'b0101010011001001;
	lut[33] = 16'b0000000011111111;
	lut[34] = 16'b0101001010000000;
	lut[35] = 16'b0101011101001000;
	lut[36] = 16'b0000000000010000;
	lut[37] = 16'b0101011101001001;
	lut[38] = 16'b0000000000010000;
	lut[39] = 16'b0101001000000000;
	lut[40] = 16'b0101010011001001;
	lut[41] = 16'b1111111111111111;
	lut[42] = 16'b0101010100001100;
	lut[43] = 16'b0101011101001001;
	lut[44] = 16'b0000000000010000;
	lut[45] = 16'b0000000000000000;
	lut[46] = 16'b0011100101111111;
	lut[47] = 16'b0010000010100010;
	lut[48] = 16'b0101010100011100;
	lut[49] = 16'b0010000010000010;
	lut[50] = 16'b0101010010111101;
	lut[51] = 16'b0000000000000000;
	lut[52] = 16'b0101011001011101;
	lut[53] = 16'b0000000000000001;
	lut[54] = 16'b0000000000000000;
	lut[55] = 16'b0101010110111101;
	lut[56] = 16'b0000000000000000;
	lut[57] = 16'b0101011100111101;
	lut[58] = 16'b0000000000000000;
	lut[59] = 16'b0010000100011111;

end

assign out_sub = lut[addr];
assign out_imm = lut[addr+1];

endmodule
