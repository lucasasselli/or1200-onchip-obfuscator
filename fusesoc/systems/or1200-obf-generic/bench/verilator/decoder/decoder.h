#include <stdio.h>

//
// Instruction opcode groups (basic)
//
#define OR1200_OR32_J                 0b000000
#define OR1200_OR32_JAL               0b000001
#define OR1200_OR32_BNF               0b000011
#define OR1200_OR32_BF                0b000100
#define OR1200_OR32_NOP               0b000101
#define OR1200_OR32_MOVHI             0b000110
#define OR1200_OR32_MACRC             0b000110
#define OR1200_OR32_XSYNC             0b001000
#define OR1200_OR32_RFE               0b001001
/* */
#define OR1200_OR32_JR                0b010001
#define OR1200_OR32_JALR              0b010010
#define OR1200_OR32_MACI              0b010011
/* */
#define OR1200_OR32_LWZ               0b100001
#define OR1200_OR32_LWS               0b100010
#define OR1200_OR32_LBZ               0b100011
#define OR1200_OR32_LBS               0b100100
#define OR1200_OR32_LHZ               0b100101
#define OR1200_OR32_LHS               0b100110
#define OR1200_OR32_ADDI              0b100111
#define OR1200_OR32_ADDIC             0b101000
#define OR1200_OR32_ANDI              0b101001
#define OR1200_OR32_ORI               0b101010
#define OR1200_OR32_XORI              0b101011
#define OR1200_OR32_MULI              0b101100
#define OR1200_OR32_MFSPR             0b101101
#define OR1200_OR32_SH_ROTI 	      0b101110
#define OR1200_OR32_SFXXI             0b101111
/* */
#define OR1200_OR32_MTSPR             0b110000
#define OR1200_OR32_MACMSB            0b110001
#define OR1200_OR32_FLOAT             0b110010
/* */
#define OR1200_OR32_SW                0b110101
#define OR1200_OR32_SB                0b110110
#define OR1200_OR32_SH                0b110111
#define OR1200_OR32_ALU               0b111000
#define OR1200_OR32_SFXX              0b111001
#define OR1200_OR32_CUST5             0b111100

//
// ALUOPs
//
#define OR1200_ALUOP_NOP	0b00100
#define OR1200_ALUOP_ADD	0b00000 // 0
#define OR1200_ALUOP_ADDC	0b00001 // 1
#define OR1200_ALUOP_SUB	0b00010 // 2
#define OR1200_ALUOP_AND	0b00011 // 3
#define OR1200_ALUOP_OR		0b00100 // 4
#define OR1200_ALUOP_XOR	0b00101 // 5
#define OR1200_ALUOP_MUL	0b00110 // 6
#define OR1200_ALUOP_RESERVED	0b00111 // 7
#define OR1200_ALUOP_SHROT	0b01000 // 8
#define OR1200_ALUOP_DIV	0b01001 // 9
#define OR1200_ALUOP_DIVU	0b01010 // a
#define OR1200_ALUOP_MULU	0b01011 // b
#define OR1200_ALUOP_EXTHB	0b01100 // c
#define OR1200_ALUOP_EXTW	0b01101 // d
#define OR1200_ALUOP_CMOV	0b01110 // e
#define OR1200_ALUOP_FFL1	0b01111 // f

/* Values sent to ALU from decode unit - not defined by ISA */
#define OR1200_ALUOP_COMP       0b10000 // Comparison
#define OR1200_ALUOP_MOVHI      0b10001 // Move-high
#define OR1200_ALUOP_CUST5	0b10010 // l.cust5

//
// Shift/rotate ops
//
#define OR1200_SHROTOP_NOP	0
#define OR1200_SHROTOP_SLL	0
#define OR1200_SHROTOP_SRL	1
#define OR1200_SHROTOP_SRA	2
#define OR1200_SHROTOP_ROR	3

//
// Zero/Sign Extend ops
//
#define OR1200_EXTHBOP_BS         0x1
#define OR1200_EXTHBOP_HS         0x0
#define OR1200_EXTHBOP_BZ         0x3
#define OR1200_EXTHBOP_HZ         0x2
#define OR1200_EXTWOP_WS          0x0
#define OR1200_EXTWOP_WZ          0x1

#define OR1200_COP_SFEQ       0b000
#define OR1200_COP_SFNE       0b001
#define OR1200_COP_SFGT       0b010
#define OR1200_COP_SFGE       0b011
#define OR1200_COP_SFLT       0b100
#define OR1200_COP_SFLE       0b101
#define OR1200_COP_X          0b111

int bit_range(unsigned int in, unsigned int stop, unsigned int start){
    unsigned int l = (stop-start) + 1; 
    unsigned int mask = (1 << l) - 1;

    return (in >> start) & mask;
}

int decode(unsigned int insn, char* outstr){

    char* outstr_back = outstr;

    unsigned int opcode = bit_range(insn, 31,26);
    unsigned int j_imm = bit_range(insn, 25, 0);
    unsigned int br_imm = bit_range(insn, 25,0);

    unsigned int rD_num = bit_range(insn, 25, 21);
    unsigned int rA_num = bit_range(insn, 20, 16);
    unsigned int rB_num = bit_range(insn, 15, 11);

    unsigned int imm_16bit = bit_range(insn, 15, 0);
    unsigned int imm_split16bit = ((bit_range(insn, 25,21) << 11) | bit_range(insn,10,0));
    unsigned int alu_op = bit_range(insn, 3, 0);
    unsigned int shrot_op = bit_range(insn, 7, 6);
    unsigned int ext_op = bit_range(insn, 9, 6);
    unsigned int ffl1_op = bit_range(insn, 9, 8);  

    unsigned int shroti_imm = bit_range(insn, 5, 0);

    unsigned int sf_op = bit_range(insn, 25, 21);

    unsigned int xsync_op = bit_range(insn, 25, 21);

    switch(opcode){
        case OR1200_OR32_J:
            sprintf(outstr,"l.j 0x%07x", j_imm << 2);
            break;

        case OR1200_OR32_JAL:
            sprintf(outstr,"l.jal 0x%07x", j_imm << 2);
            break;

        case OR1200_OR32_BNF:
            sprintf(outstr,"l.bnf 0x%07x", br_imm << 2);
            break;

        case OR1200_OR32_BF:
            sprintf(outstr,"l.bf 0x%07x", br_imm << 2);
            break;

        case OR1200_OR32_RFE:
            sprintf(outstr,"l.rfe");
            break;

        case OR1200_OR32_JR:
            sprintf(outstr,"l.jr r%d",rB_num);
            break;

        case OR1200_OR32_JALR:
            sprintf(outstr,"l.jalr r%d",rB_num);
            break;

        case OR1200_OR32_LWZ:
            sprintf(outstr,"l.lwz r%d,0x%x(r%d)",rD_num,imm_16bit,rA_num);
            break;

        case OR1200_OR32_LWS:
            sprintf(outstr,"l.lws r%d,0x%x(r%d)",rD_num,imm_16bit,rA_num);
            break;

        case OR1200_OR32_LBZ:
            sprintf(outstr,"l.lbz r%d,0x%x(r%d)",rD_num,imm_16bit,rA_num);
            break;

        case OR1200_OR32_LBS:
            sprintf(outstr,"l.lbs r%d,0x%x(r%d)",rD_num,imm_16bit,rA_num);
            break;

        case OR1200_OR32_LHZ:
            sprintf(outstr,"l.lhz r%d,0x%x(r%d)",rD_num,imm_16bit,rA_num);
            break;

        case OR1200_OR32_LHS:
            sprintf(outstr,"l.lhs r%d,0x%x(r%d)",rD_num,imm_16bit,rA_num);
            break;

        case OR1200_OR32_SW:
            sprintf(outstr,"l.sw 0x%x(r%d),r%d",imm_split16bit,rA_num,rB_num);
            break;

        case OR1200_OR32_SB:
            sprintf(outstr,"l.sb 0x%x(r%d),r%d",imm_split16bit,rA_num,rB_num);
            break;

        case OR1200_OR32_SH:
            sprintf(outstr,"l.sh 0x%x(r%d),r%d",imm_split16bit,rA_num,rB_num);
            break;

        case OR1200_OR32_MFSPR:
            sprintf(outstr,"l.mfspr r%d,r%d,0x%04x",rD_num,rA_num,imm_16bit);
            break;

        case OR1200_OR32_MTSPR:
            sprintf(outstr,"l.mtspr r%d,r%d,0x%04x",rA_num,rB_num,imm_split16bit);
            break;

        case OR1200_OR32_MOVHI:
            if (!(insn & (1 << 16)))
                sprintf(outstr,"l.movhi r%d,0x%04x",rD_num,imm_16bit);
            else
                sprintf(outstr,"l.macrc r%d",rD_num);
            break;

        case OR1200_OR32_ADDI:
            sprintf(outstr,"l.addi r%d,r%d,0x%04x",rD_num,rA_num,imm_16bit);
            break;

        case OR1200_OR32_ADDIC:
            sprintf(outstr,"l.addic r%d,r%d,0x%04x",rD_num,rA_num,imm_16bit);
            break;

        case OR1200_OR32_ANDI:
            sprintf(outstr,"l.andi r%d,r%d,0x%04x",rD_num,rA_num,imm_16bit);
            break;

        case OR1200_OR32_ORI:
            sprintf(outstr,"l.ori r%d,r%d,0x%04x",rD_num,rA_num,imm_16bit);
            break;

        case OR1200_OR32_XORI:
            sprintf(outstr,"l.xori r%d,r%d,0x%04x",rD_num,rA_num,imm_16bit);
            break;

        case OR1200_OR32_MULI:
            sprintf(outstr,"l.muli r%d,r%d,0x%04x",rD_num,rA_num,imm_16bit);
            break;

        case OR1200_OR32_ALU:
            switch(alu_op){
                case OR1200_ALUOP_ADD:
                    outstr+= sprintf(outstr,"l.add ");
                    break;
                case OR1200_ALUOP_ADDC:
                    outstr+= sprintf(outstr,"l.addc ");
                    break;
                case OR1200_ALUOP_SUB:
                    outstr+= sprintf(outstr,"l.sub ");
                    break;
                case OR1200_ALUOP_AND:
                    outstr+= sprintf(outstr,"l.and ");
                    break;
                case OR1200_ALUOP_OR:
                    outstr+= sprintf(outstr,"l.or ");
                    break;
                case OR1200_ALUOP_XOR:
                    outstr+= sprintf(outstr,"l.xor ");
                    break;
                case OR1200_ALUOP_MUL:
                    outstr+= sprintf(outstr,"l.mul ");
                    break;

                case OR1200_ALUOP_SHROT:
                    switch(shrot_op){
                        case OR1200_SHROTOP_SLL:
                            outstr+= sprintf(outstr,"l.sll ");
                            break;
                        case OR1200_SHROTOP_SRL:
                            outstr+= sprintf(outstr,"l.srl ");
                            break;
                        case OR1200_SHROTOP_SRA:
                            outstr+= sprintf(outstr,"l.sra ");
                            break;
                        case OR1200_SHROTOP_ROR:
                            outstr+= sprintf(outstr,"l.ror ");
                            break;
                    }
                    break;
                case OR1200_ALUOP_DIV:
                    outstr+= sprintf(outstr,"l.div ");
                    break;
                case OR1200_ALUOP_DIVU:
                    outstr+= sprintf(outstr,"l.divu ");
                    break;
                case OR1200_ALUOP_CMOV:
                    outstr+= sprintf(outstr,"l.cmov ");
                    break;
                case OR1200_ALUOP_EXTW:
                    switch(ext_op){
                        case 0:
                            outstr+= sprintf(outstr, "l.extws ");
                            break;
                        case 1:
                            outstr+= sprintf(outstr, "l.extwz ");
                            break;
                    }
                    break;
                case OR1200_ALUOP_EXTHB:
                    switch(ext_op){
                        case 1:
                            outstr+= sprintf(outstr, "l.extbs ");
                            break;
                        case 3:
                            outstr+= sprintf(outstr, "l.extbz ");
                            break;
                        case 0:
                            outstr+= sprintf(outstr, "l.exths ");
                            break;
                        case 2:
                            outstr+= sprintf(outstr, "l.exthz ");
                            break;
                    }
                    break;
                case OR1200_ALUOP_FFL1:
                    switch(ffl1_op){
                        case 0:
                            outstr+= sprintf(outstr, "l.ff1 ");
                            break;
                        case 1:
                            outstr+= sprintf(outstr, "l.fl1 ");
                            break;
                    }
                    break;
            }
            sprintf(outstr,"r%d,r%d,r%d",rD_num,rA_num,rB_num);
            break;

        case OR1200_OR32_SH_ROTI:
            outstr = outstr_back;
            switch(shrot_op){
                case OR1200_SHROTOP_SLL:
                    outstr+= sprintf(outstr,"l.slli ");
                    break;
                case OR1200_SHROTOP_SRL:
                    outstr+= sprintf(outstr,"l.srli ");
                    break;
                case OR1200_SHROTOP_SRA:
                    outstr+= sprintf(outstr,"l.srai ");
                    break;
                case OR1200_SHROTOP_ROR:
                    outstr+= sprintf(outstr,"l.rori ");
                    break;
            }
            sprintf(outstr,"r%d,r%d,0x%02x",rD_num,rA_num,shroti_imm);
            break;

        case OR1200_OR32_SFXXI:
            switch(bit_range(sf_op, 2, 0)){
                case OR1200_COP_SFEQ:
                    outstr += sprintf(outstr,"l.sfeqi ");
                    break;
                case OR1200_COP_SFNE:
                    outstr += sprintf(outstr,"l.sfnei ");
                    break;
                case OR1200_COP_SFGT:
                    if (sf_op & (1 << 3))
                        outstr += sprintf(outstr,"l.sfgtsi ");
                    else
                        outstr += sprintf(outstr,"l.sfgtui ");
                    break;
                case OR1200_COP_SFGE:
                    if (sf_op & (1 << 3))
                        outstr += sprintf(outstr,"l.sfgesi ");
                    else
                        outstr += sprintf(outstr,"l.sfgeui ");
                    break;
                case OR1200_COP_SFLT:
                    if (sf_op & (1 << 3))
                        outstr += sprintf(outstr,"l.sfltsi ");
                    else
                        outstr += sprintf(outstr,"l.sfltui ");
                    break;
                case OR1200_COP_SFLE:
                    if (sf_op & (1 << 3))
                        outstr += sprintf(outstr,"l.sflesi ");
                    else
                        outstr += sprintf(outstr,"l.sfleui ");
                    break;
            }
            sprintf(outstr,"r%d,0x%04x",rA_num, imm_16bit);
            break;

        case OR1200_OR32_SFXX:
            switch(bit_range(sf_op, 2, 0)){
                case OR1200_COP_SFEQ:
                    outstr += sprintf(outstr,"l.sfeq ");
                    break;
                case OR1200_COP_SFNE:
                    outstr += sprintf(outstr,"l.sfne ");
                    break;
                case OR1200_COP_SFGT:
                    if (sf_op & (1 << 3))
                        outstr += sprintf(outstr,"l.sfgts ");
                    else
                        outstr += sprintf(outstr,"l.sfgtu ");
                    break;
                case OR1200_COP_SFGE:
                    if (sf_op & (1 << 3))
                        outstr += sprintf(outstr,"l.sfges ");
                    else
                        outstr += sprintf(outstr,"l.sfgeu ");
                    break;
                case OR1200_COP_SFLT:
                    if (sf_op & (1 << 3))
                        outstr += sprintf(outstr,"l.sflts ");
                    else
                        outstr += sprintf(outstr,"l.sfltu ");
                    break;
                case OR1200_COP_SFLE:
                    if (sf_op & (1 << 3))
                        outstr += sprintf(outstr,"l.sfles ");
                    else
                        outstr += sprintf(outstr,"l.sfleu ");
                    break;
            }
            sprintf(outstr,"r%d,r%d",rA_num, rB_num);
            break;

        case OR1200_OR32_MACI:
            sprintf(outstr,"l.maci r%d,0x%04x",rA_num,imm_16bit);
            break;

        case OR1200_OR32_MACMSB:
            if(bit_range(insn, 3, 0) == 1)
                outstr += sprintf(outstr,"l.mac ");
            else if(bit_range(insn, 3, 0) == 2)
                outstr += sprintf(outstr,"l.msb ");

            sprintf(outstr,"r%d,r%d",rA_num,rB_num);
            break;

        case OR1200_OR32_NOP:
            sprintf(outstr,"l.nop 0x%x",imm_16bit);
            break;

        case OR1200_OR32_XSYNC:
            switch(xsync_op){
                case 0:
                    sprintf(outstr,"l.sys 0x%04x",imm_16bit);
                    break;
                case 8:
                    sprintf(outstr,"l.trap 0x%04x",imm_16bit);
                    break;
                case 16:
                    sprintf(outstr,"l.msync");
                    break;
                case 20:
                    sprintf(outstr,"l.psync");
                    break;
                case 24:
                    sprintf(outstr,"l.csync");
                    break;
            }
            break;

        default:
            sprintf(outstr,"Unknown opcode 0x%x",opcode);
            break;
    }

    return 0;
}


