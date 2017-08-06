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

reg [`OBF_LUT_OUT_WIDTH-1:0] lut0 [121:0];

initial begin
    lut0[0] = 16'b0000000000000001;
    lut0[1] = 16'b0101001110110000;
    lut0[2] = 16'b0010000000101100;
    lut0[3] = 16'b0101010010111101;
    lut0[4] = 16'b0010000000100000;
    lut0[5] = 16'b0010000001111111;
    lut0[6] = 16'b0010000000111110;
    lut0[7] = 16'b0101010000000000;
    lut0[8] = 16'b0100001100111101;
    lut0[9] = 16'b0101010110011100;
    lut0[10] = 16'b0010000000100010;
    lut0[11] = 16'b0101010010111101;
    lut0[12] = 16'b0101010111010000;
    lut0[13] = 16'b1111111111111111;
    lut0[14] = 16'b0101010111000100;
    lut0[15] = 16'b1111111111111111;
    lut0[16] = 16'b0010000010001010;
    lut0[17] = 16'b0101010111001000;
    lut0[18] = 16'b1111111111111111;
    lut0[19] = 16'b0010000010111111;
    lut0[20] = 16'b0101010100011100;
    lut0[21] = 16'b0101010111011100;
    lut0[22] = 16'b1111111111111111;
    lut0[23] = 16'b0101010111000000;
    lut0[24] = 16'b1111111111111111;
    lut0[25] = 16'b0010000010001010;
    lut0[26] = 16'b0101010111001000;
    lut0[27] = 16'b1111111111111111;
    lut0[28] = 16'b0010000010111111;
    lut0[29] = 16'b0101011101000000;
    lut0[30] = 16'b0000000000011000;
    lut0[31] = 16'b0101011101001001;
    lut0[32] = 16'b0000000000011000;
    lut0[33] = 16'b0101011101000000;
    lut0[34] = 16'b0000000000011000;
    lut0[35] = 16'b0101011101001001;
    lut0[36] = 16'b0000000000011000;
    lut0[37] = 16'b0101011101000000;
    lut0[38] = 16'b0000000000010000;
    lut0[39] = 16'b0101011101001001;
    lut0[40] = 16'b0000000000010000;
    lut0[41] = 16'b0101010011000001;
    lut0[42] = 16'b1111111111111111;
    lut0[43] = 16'b0101010110100001;
    lut0[44] = 16'b0101010110100001;
    lut0[45] = 16'b0010000111100010;
    lut0[46] = 16'b0100001100111101;
    lut0[47] = 16'b0010100111100010;
    lut0[48] = 16'b0100001100111101;
    lut0[49] = 16'b0101000110000000;
    lut0[50] = 16'b0010001110001011;
    lut0[51] = 16'b0101001000000000;
    lut0[52] = 16'b0010011110001011;
    lut0[53] = 16'b0101001010000000;
    lut0[54] = 16'b0010000110001011;
    lut0[55] = 16'b0101001010000000;
    lut0[56] = 16'b0010000110001011;
    lut0[57] = 16'b0101000010000001;
    lut0[58] = 16'b0101000100000001;
    lut0[59] = 16'b0101011010000000;
    lut0[60] = 16'b0101010010111101;
    lut0[61] = 16'b0101010100001100;
    lut0[62] = 16'b0101011101001001;
    lut0[63] = 16'b0000000000010000;
    lut0[64] = 16'b0111100000000000;
    lut0[65] = 16'b0101010010111101;
    lut0[66] = 16'b0101010111010000;
    lut0[67] = 16'b1111111111111111;
    lut0[68] = 16'b0101010111000100;
    lut0[69] = 16'b1111111111111111;
    lut0[70] = 16'b0010000001101010;
    lut0[71] = 16'b0101010111001000;
    lut0[72] = 16'b1111111111111111;
    lut0[73] = 16'b0010000010111111;
    lut0[74] = 16'b0101010110011100;
    lut0[75] = 16'b0101010111011100;
    lut0[76] = 16'b1111111111111111;
    lut0[77] = 16'b0101010111000000;
    lut0[78] = 16'b1111111111111111;
    lut0[79] = 16'b0010000001101010;
    lut0[80] = 16'b0101010111001000;
    lut0[81] = 16'b1111111111111111;
    lut0[82] = 16'b0010000010111111;
    lut0[83] = 16'b0101010110011100;
    lut0[84] = 16'b0101010111011100;
    lut0[85] = 16'b0000000000011111;
    lut0[86] = 16'b0101001111011100;
    lut0[87] = 16'b0000000000100001;
    lut0[88] = 16'b0010000100010010;
    lut0[89] = 16'b0101011100000000;
    lut0[90] = 16'b0010000010001010;
    lut0[91] = 16'b0010000010111111;
    lut0[92] = 16'b0111101110000000;
    lut0[93] = 16'b0101010010111101;
    lut0[94] = 16'b0010000100000000;
    lut0[95] = 16'b0101010010111101;
    lut0[96] = 16'b0101010110011100;
    lut0[97] = 16'b0010000100000010;
    lut0[98] = 16'b0010000010111111;
    lut0[99] = 16'b0010010100000000;
    lut0[100] = 16'b0101010010111101;
    lut0[101] = 16'b0101010110011100;
    lut0[102] = 16'b0010010100000010;
    lut0[103] = 16'b0010000010111111;
    lut0[104] = 16'b0010001100000000;
    lut0[105] = 16'b0101010010111101;
    lut0[106] = 16'b0101010110011100;
    lut0[107] = 16'b0010001100000010;
    lut0[108] = 16'b0010000010111111;
    lut0[109] = 16'b0010000001000000;
    lut0[110] = 16'b0010000110111111;
    lut0[111] = 16'b0111101010000000;
    lut0[112] = 16'b0101010010111101;
    lut0[113] = 16'b0010000001110000;
    lut0[114] = 16'b0101010111011100;
    lut0[115] = 16'b1111111111111111;
    lut0[116] = 16'b0010000010000000;
    lut0[117] = 16'b0010000001101010;
    lut0[118] = 16'b0010000010111111;
    lut0[119] = 16'b0101010100011100;
    lut0[120] = 16'b0010000010100010;
    lut0[121] = 16'b0101010010111101;
    end

// Address generation
always @(index) begin
    case(index)
        `OBF_IGU_WIDTH'd64: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd1;
        `OBF_IGU_WIDTH'd65: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd4;
        `OBF_IGU_WIDTH'd27: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd6;
        `OBF_IGU_WIDTH'd28: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd9;
        `OBF_IGU_WIDTH'd67: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd12;
        `OBF_IGU_WIDTH'd29: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd20;
        `OBF_IGU_WIDTH'd60: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd29;
        `OBF_IGU_WIDTH'd63: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd33;
        `OBF_IGU_WIDTH'd58: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd37;
        `OBF_IGU_WIDTH'd62: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd41;
        `OBF_IGU_WIDTH'd59: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd43;
        `OBF_IGU_WIDTH'd61: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd44;
        `OBF_IGU_WIDTH'd71: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd45;
        `OBF_IGU_WIDTH'd76: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd47;
        `OBF_IGU_WIDTH'd24: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd49;
        `OBF_IGU_WIDTH'd23: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd51;
        `OBF_IGU_WIDTH'd26: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd53;
        `OBF_IGU_WIDTH'd25: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd55;
        `OBF_IGU_WIDTH'd22: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd57;
        `OBF_IGU_WIDTH'd21: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd58;
        `OBF_IGU_WIDTH'd33: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd59;
        `OBF_IGU_WIDTH'd5: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd61;
        `OBF_IGU_WIDTH'd48: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd64;
        `OBF_IGU_WIDTH'd68: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd66;
        `OBF_IGU_WIDTH'd30: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd74;
        `OBF_IGU_WIDTH'd37: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd83;
        `OBF_IGU_WIDTH'd57: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd92;
        `OBF_IGU_WIDTH'd72: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd94;
        `OBF_IGU_WIDTH'd34: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd96;
        `OBF_IGU_WIDTH'd74: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd99;
        `OBF_IGU_WIDTH'd36: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd101;
        `OBF_IGU_WIDTH'd73: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd104;
        `OBF_IGU_WIDTH'd35: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd106;
        `OBF_IGU_WIDTH'd66: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd109;
        `OBF_IGU_WIDTH'd55: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd111;
        `OBF_IGU_WIDTH'd69: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd113;
        `OBF_IGU_WIDTH'd31: lut0_pointer = `OBF_LUT_ADDR_WIDTH'd119;
        default:            lut0_pointer = `OBF_LUT_ADDR_WIDTH'd0;
    endcase
end

assign lut0_addr = lut0_pointer+ ppc;
assign out_sub = lut0[lut0_addr];
assign out_imm = lut0[lut0_addr+1];

endmodule
