`include "obf_defines.v"

module obf_indexgen(
    insn,
    i
);

input [31:0] insn;

output reg [`OBF_INDEX_BUS] i;

always @(insn)
    case (insn[31:26])
        // l.j
        6'b000000: i = `OBF_INDEX_WIDTH'd0;
        // l.jal
        6'b000001: i = `OBF_INDEX_WIDTH'd1;
        // l.bnf
        6'b000011: i = `OBF_INDEX_WIDTH'd2;
        // l.bf
        6'b000100: i = `OBF_INDEX_WIDTH'd3;
        // l.nop
        6'b000101: i = `OBF_INDEX_WIDTH'd4;
        // l.movhi / l.macrc
        6'b000110 :
            if(insn[16])
                // l.macrc
                i = `OBF_INDEX_WIDTH'd5;
            else
                // l.movhi
                i = `OBF_INDEX_WIDTH'd6; 
        // l.sys / l.trap / l.xsync
        6'b001000 :
            case (insn[25:23])
                // l.sys
                3'b000 : i = `OBF_INDEX_WIDTH'd7;
                // l.trap
                3'b010 : i = `OBF_INDEX_WIDTH'd8;
                // l.msync
                3'b100 : i = `OBF_INDEX_WIDTH'd9;
                // l.csync
                3'b101 : i = `OBF_INDEX_WIDTH'd10;
                // l.csync
                3'b110 : i = `OBF_INDEX_WIDTH'd11;
                // Default (error)
                default : i = -'d1;
            endcase
        // l.rfe
        6'b001001 : i = `OBF_INDEX_WIDTH'd12;
        // l.jr
        6'b010001 : i = `OBF_INDEX_WIDTH'd13;
        // l.jalr
        6'b010010 : i = `OBF_INDEX_WIDTH'd14;
        // l.maci
        6'b010011 : i = `OBF_INDEX_WIDTH'd15;
        // l.cust1
        6'b011100 : i = `OBF_INDEX_WIDTH'd16;
        // l.cust2
        6'b011101 : i = `OBF_INDEX_WIDTH'd17;
        // l.cust3
        6'b011110 : i = `OBF_INDEX_WIDTH'd18;
        // l.cust4
        6'b011111 : i = `OBF_INDEX_WIDTH'd19;
        // l.ld
        6'b100000 : i = `OBF_INDEX_WIDTH'd20;
        // l.lwz
        6'b100001 : i = `OBF_INDEX_WIDTH'd21;
        // l.lws
        6'b100010 : i = `OBF_INDEX_WIDTH'd22;
        // l.lbz
        6'b100011 : i = `OBF_INDEX_WIDTH'd23;
        // l.lbs
        6'b100100 : i = `OBF_INDEX_WIDTH'd24;
        // l.lhz
        6'b100101 : i = `OBF_INDEX_WIDTH'd25;
        // l.lhs
        6'b100110 : i = `OBF_INDEX_WIDTH'd26;
        // l.addi 
        6'b100111 : i = `OBF_INDEX_WIDTH'd27;
        // l.addic
        6'b101000 : i = `OBF_INDEX_WIDTH'd28;
        // l.andi
        6'b101001 : i = `OBF_INDEX_WIDTH'd29;
        // l.ori
        6'b101010 : i = `OBF_INDEX_WIDTH'd30;
        // l.xori
        6'b101011 : i = `OBF_INDEX_WIDTH'd31;
        // l.muli
        6'b101100 : i = `OBF_INDEX_WIDTH'd32;
        // l.mfspr
        6'b101101 : i = `OBF_INDEX_WIDTH'd33;
        // l.sxx/l.roti
        6'b101110 :
            case(insn[7:6])
                // l.slli
                2'b00 : i = `OBF_INDEX_WIDTH'd34;
                // l.srli
                2'b01 : i = `OBF_INDEX_WIDTH'd35;
                // l.srai
                2'b10 : i = `OBF_INDEX_WIDTH'd36;
                // l.rori
                2'b11 : i = `OBF_INDEX_WIDTH'd37;
                // Default (error)
                default : i = -'d1;
            endcase
        // l.sfxxi
        6'b101111 :
            case(insn[25:21])
                // l.sfeqi
                5'b00000 : i = `OBF_INDEX_WIDTH'd38;
                // l.sfnei
                5'b00001 : i = `OBF_INDEX_WIDTH'd39;
                // l.sfgtui
                5'b00010 : i = `OBF_INDEX_WIDTH'd40;
                // l.sfgeui
                5'b00011 : i = `OBF_INDEX_WIDTH'd41;
                // l.sfltui
                5'b00100 : i = `OBF_INDEX_WIDTH'd42;
                // l.sfleui
                5'b00101 : i = `OBF_INDEX_WIDTH'd43;
                // l.sfgtsi
                5'b01010 : i = `OBF_INDEX_WIDTH'd44;
                // l.sfgesi
                5'b01011 : i = `OBF_INDEX_WIDTH'd45;
                // l.sfltsi
                5'b01100 : i = `OBF_INDEX_WIDTH'd46;
                // l.sflesi
                5'b01101 : i = `OBF_INDEX_WIDTH'd47;
                // Default (error)
                default : i = -'d1;
            endcase
        // l.mtspr
        6'b110000 : i = `OBF_INDEX_WIDTH'd48;
        // l.mac/l.msb
        6'b110001 :
            case(insn[3:0])
                // l.mac
                4'b0001 : i = `OBF_INDEX_WIDTH'd49;
                // l.macu
                4'b0011 : i = `OBF_INDEX_WIDTH'd50;
                // l.msb
                4'b0010 : i = `OBF_INDEX_WIDTH'd51;
                // l.msbu
                4'b0100 : i = `OBF_INDEX_WIDTH'd52;
                // Default (error)
                default : i = -'d1;
            endcase
        // l.swa
        6'b110011 : i = `OBF_INDEX_WIDTH'd53;
        // l.sd
        6'b110100 : i = `OBF_INDEX_WIDTH'd54;
        // l.sw
        6'b110101 : i = `OBF_INDEX_WIDTH'd55;
        // l.sb
        6'b110110 : i = `OBF_INDEX_WIDTH'd56;
        // l.sh
        6'b110111 : i = `OBF_INDEX_WIDTH'd57;
        // ALU
        6'b111000 :
            casex({insn[9:6], insn[3:0]})
                // l.exths
                8'b00001100 : i = `OBF_INDEX_WIDTH'd58;
                // l.extws
                8'b00001101 : i = `OBF_INDEX_WIDTH'd59;
                // l.extbs
                8'b00011100 : i = `OBF_INDEX_WIDTH'd60;
                // l.extwz
                8'b00011101 : i = `OBF_INDEX_WIDTH'd61;
                // l.exthz
                8'b00101100 : i = `OBF_INDEX_WIDTH'd62;
                // l.exthz
                8'b00111100 : i = `OBF_INDEX_WIDTH'd63;
                // l.add
                8'b00xx0000 : i = `OBF_INDEX_WIDTH'd64;
                // l.addc
                8'b00xx0001 : i = `OBF_INDEX_WIDTH'd65;
                // l.sub
                8'b00xx0010 : i = `OBF_INDEX_WIDTH'd66;
                // l.and
                8'b00xx0011 : i = `OBF_INDEX_WIDTH'd67;
                // l.or
                8'b00xx0100 : i = `OBF_INDEX_WIDTH'd68;
                // l.xor
                8'b00xx0101 : i = `OBF_INDEX_WIDTH'd69;
                // l.cmov
                8'b00xx1110 : i = `OBF_INDEX_WIDTH'd70;
                // l.ff1
                8'b00xx1111 : i = `OBF_INDEX_WIDTH'd71;
                // l.ssl
                8'b00001000 : i = `OBF_INDEX_WIDTH'd72;
                // l.srl
                8'b00011000 : i = `OBF_INDEX_WIDTH'd73;
                // l.sra
                8'b00101000 : i = `OBF_INDEX_WIDTH'd74;
                // l.ror
                8'b00111000 : i = `OBF_INDEX_WIDTH'd75;
                // l.fl1
                8'b01xx1111 : i = `OBF_INDEX_WIDTH'd76;
                // l.mul
                8'b11xx0110 : i = `OBF_INDEX_WIDTH'd77;
                // l.muld
                8'b11xx0111 : i = `OBF_INDEX_WIDTH'd78;
                // l.div 
                8'b11xx1001 : i = `OBF_INDEX_WIDTH'd79;
                // l.divu
                8'b11xx1010 : i = `OBF_INDEX_WIDTH'd80;
                // l.mulu
                8'b11xx1011 : i = `OBF_INDEX_WIDTH'd81;
                // l.muldu
                8'b11xx1100 : i = `OBF_INDEX_WIDTH'd82;
                // Default (error)
                default : i = -'d1;
            endcase
        // l.sfxx
        6'b111001 :
            case(insn[25:21])
                // l.sfeq
                5'b00000 : i = `OBF_INDEX_WIDTH'd83;
                // l.sfne
                5'b00001 : i = `OBF_INDEX_WIDTH'd84;
                // l.sfgtu
                5'b00010 : i = `OBF_INDEX_WIDTH'd85;
                // l.sfgeu
                5'b00011 : i = `OBF_INDEX_WIDTH'd86;
                // l.sfltu
                5'b00100 : i = `OBF_INDEX_WIDTH'd87;
                // l.sfleu
                5'b00101 : i = `OBF_INDEX_WIDTH'd88;
                // l.sfgts
                5'b01010 : i = `OBF_INDEX_WIDTH'd89;
                // l.sfges
                5'b01011 : i = `OBF_INDEX_WIDTH'd90;
                // l.sflts
                5'b01100 : i = `OBF_INDEX_WIDTH'd91;
                // l.sfles
                5'b01101 : i = `OBF_INDEX_WIDTH'd92;
                // Default (error)
                default : i = -'d1;
            endcase
        // l.cust5
        6'b111100 : i = `OBF_INDEX_WIDTH'd93;
        // l.cust6
        6'b111101 : i = `OBF_INDEX_WIDTH'd94;
        // l.cust7
        6'b111110 : i = `OBF_INDEX_WIDTH'd95;
        // l.cust8
        6'b111111 : i = `OBF_INDEX_WIDTH'd96;
        // Default (error)
        default : i = -'d1;
    endcase
endmodule 
