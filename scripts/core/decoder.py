import logging

# OPCODEs
OR1200_OR32_J = "000000"
OR1200_OR32_JAL = "000001"
OR1200_OR32_BNF = "000011"
OR1200_OR32_BF = "000100"
OR1200_OR32_NOP = "000101"
OR1200_OR32_MOVHI = "000110"
OR1200_OR32_MACRC = "000110"
OR1200_OR32_XSYNC = "001000"
OR1200_OR32_RFE = "001001"
OR1200_OR32_JR = "010001"
OR1200_OR32_JALR = "010010"
OR1200_OR32_MACI = "010011"
OR1200_OR32_LWZ = "100001"
OR1200_OR32_LWS = "100010"
OR1200_OR32_LBZ = "100011"
OR1200_OR32_LBS = "100100"
OR1200_OR32_LHZ = "100101"
OR1200_OR32_LHS = "100110"
OR1200_OR32_ADDI = "100111"
OR1200_OR32_ADDIC = "101000"
OR1200_OR32_ANDI = "101001"
OR1200_OR32_ORI = "101010"
OR1200_OR32_XORI = "101011"
OR1200_OR32_MULI = "101100"
OR1200_OR32_MFSPR = "101101"
OR1200_OR32_SH_ROTI = "101110"
OR1200_OR32_SFXXI = "101111"
OR1200_OR32_MTSPR = "110000"
OR1200_OR32_MACMSB = "110001"
OR1200_OR32_FLOAT = "110010"
OR1200_OR32_SW = "110101"
OR1200_OR32_SB = "110110"
OR1200_OR32_SH = "110111"
OR1200_OR32_ALU = "111000"
OR1200_OR32_SFXX = "111001"
OR1200_OR32_CUST5 = "111100"

# ALUOPs
OR1200_ALUOP_NOP = "00100"
OR1200_ALUOP_ADD = "00000"  # 0
OR1200_ALUOP_ADDC = "00001"  # 1
OR1200_ALUOP_SUB = "00010"  # 2
OR1200_ALUOP_AND = "00011"  # 3
OR1200_ALUOP_OR = "00100"  # 4
OR1200_ALUOP_XOR = "00101"  # 5
OR1200_ALUOP_MUL = "00110"  # 6
OR1200_ALUOP_RESERVED = "00111"  # 7
OR1200_ALUOP_SHROT = "01000"  # 8
OR1200_ALUOP_DIV = "01001"  # 9
OR1200_ALUOP_DIVU = "01010"  # a
OR1200_ALUOP_MULU = "01011"  # b
OR1200_ALUOP_EXTHB = "01100"  # c
OR1200_ALUOP_EXTW = "01101"  # d
OR1200_ALUOP_CMOV = "01110"  # e
OR1200_ALUOP_FFL1 = "01111"  # f
OR1200_ALUOP_COMP = "10000"  # Comparison
OR1200_ALUOP_MOVHI = "10001"  # Move-high
OR1200_ALUOP_CUST5 = "10010"  # l.cust5

# MACOPs
OR1200_MACOP_NOP = "000"
OR1200_MACOP_MAC = "001"
OR1200_MACOP_MSB = "010"

# SHROTOPs
OR1200_SHROTOP_NOP = "00"
OR1200_SHROTOP_SLL = "00"
OR1200_SHROTOP_SRL = "01"
OR1200_SHROTOP_SRA = "10"
OR1200_SHROTOP_ROR = "11"

# EXTHBOPs
OR1200_EXTHBOP_BS = "01"
OR1200_EXTHBOP_HS = "00"
OR1200_EXTHBOP_BZ = "11"
OR1200_EXTHBOP_HZ = "10"
OR1200_EXTWOP_WS = "00"
OR1200_EXTWOP_WZ = "01"

# BRANCHOPs
OR1200_BRANCHOP_NOP = "000"
OR1200_BRANCHOP_J = "001"
OR1200_BRANCHOP_JR = "010"
OR1200_BRANCHOP_BAL = "011"
OR1200_BRANCHOP_BF = "100"
OR1200_BRANCHOP_BNF = "101"
OR1200_BRANCHOP_RFE = "110"

# LSUOPs
OR1200_LSUOP_NOP = "0000"
OR1200_LSUOP_LBZ = "0010"
OR1200_LSUOP_LBS = "0011"
OR1200_LSUOP_LHZ = "0100"
OR1200_LSUOP_LHS = "0101"
OR1200_LSUOP_LWZ = "0110"
OR1200_LSUOP_LWS = "0111"
OR1200_LSUOP_LD = "0001"
OR1200_LSUOP_SD = "1000"
OR1200_LSUOP_SB = "1010"
OR1200_LSUOP_SH = "1100"
OR1200_LSUOP_SW = "1110"

# RFWBOP
OR1200_RFWBOP_NOP = "0000"
OR1200_RFWBOP_ALU = "000"
OR1200_RFWBOP_LSU = "001"
OR1200_RFWBOP_SPRS = "010"
OR1200_RFWBOP_LR = "011"
OR1200_RFWBOP_FPU = "100"


def parse(insn):

    word = None

    for op in insn.split():
        if "l." in op:
            word = decode(op)
            break

    if not word:
        raise ValueError

    return word


def get_opcode(insn):
    if (insn == "l.add" or
            insn == "l.addc" or
            insn == "l.and" or
            insn == "l.cmov" or
            insn == "l.div" or
            insn == "l.divu" or
            insn == "l.extbs" or
            insn == "l.extbz" or
            insn == "l.exths" or
            insn == "l.exthz" or
            insn == "l.extws" or
            insn == "l.extwz" or
            insn == "l.ff1" or
            insn == "l.fl1" or
            insn == "l.mul" or
            insn == "l.muld" or
            insn == "l.muldu" or
            insn == "l.mulu" or
            insn == "l.ror" or
            insn == "l.or" or
            insn == "l.sll" or
            insn == "l.sra" or
            insn == "l.srl" or
            insn == "l.sub" or
            insn == "l.xor"):
        return OR1200_OR32_ALU
    if insn == "l.addi":
        return OR1200_OR32_ADDI
    elif insn == "l.addic":
        return OR1200_OR32_ADDIC
    elif insn == "l.andi":
        return OR1200_OR32_ANDI
    elif insn == "l.bf":
        return OR1200_OR32_BF
    elif insn == "l.bnf":
        return OR1200_OR32_BNF
    elif (insn == "l.csync" or
            insn == "l.msync" or
            insn == "l.psync"):
        return OR1200_OR32_XSYNC
    elif (insn == "l.cust1" or
            insn == "l.cust2" or
            insn == "l.cust3" or
            insn == "l.cust4" or
            insn == "l.cust5" or
            insn == "l.cust6" or
            insn == "l.cust7" or
            insn == "l.cust8"):
        # TODO
        pass
    elif insn == "l.j":
        return OR1200_OR32_J
    elif insn == "l.jal":
        return OR1200_OR32_JAL
    elif insn == "l.jalr":
        return OR1200_OR32_JALR
    elif insn == "l.jr":
        return OR1200_OR32_JR
    elif insn == "l.lbs":
        return OR1200_OR32_LBS
    elif insn == "l.lbz":
        return OR1200_OR32_LBZ
    elif insn == "l.lhs":
        return OR1200_OR32_LHS
    elif insn == "l.lhz":
        return OR1200_OR32_LHZ
    elif insn == "l.lws":
        return OR1200_OR32_LWS
    elif insn == "l.lwz":
        return OR1200_OR32_LWZ
    elif (insn == "l.mac" or
            insn == "l.msb" or
            insn == "l.msbu"):
        return OR1200_OR32_MACMSB
    elif insn == "l.maci":
        return OR1200_OR32_MACI
    elif insn == "l.macrc":
        return OR1200_OR32_MACRC
    elif insn == "l.mfspr":
        return OR1200_OR32_MFSPR
    elif insn == "l.movhi":
        return OR1200_OR32_MOVHI
    elif insn == "l.mtspr":
        return OR1200_OR32_MTSPR
    elif insn == "l.muli":
        return OR1200_OR32_MULI
    elif insn == "l.nop":
        return OR1200_OR32_NOP
    elif insn == "l.ori":
        return OR1200_OR32_ORI
    elif insn == "l.rfe":
        return OR1200_OR32_RFE
    elif insn == "l.rori":
        return OR1200_OR32_SH_ROTI
    elif insn == "l.sb":
        return OR1200_OR32_SB
    elif insn == "l.sd":
        # TODO
        pass
    elif (insn == "l.sfeq" or
            insn == "l.sfges" or
            insn == "l.sfgeu" or
            insn == "l.sfgts" or
            insn == "l.sfgtu" or
            insn == "l.sfles" or
            insn == "l.sfleu" or
            insn == "l.sflts" or
            insn == "l.sfltu" or
            insn == "l.sfne"):
        return OR1200_OR32_SFXX
    elif (insn == "l.sfeqi" or
            insn == "l.sfgesi" or
            insn == "l.sfgeui" or
            insn == "l.sfgtsi" or
            insn == "l.sfgtui" or
            insn == "l.sflesi" or
            insn == "l.sfleui" or
            insn == "l.sfltsi" or
            insn == "l.sfltui" or
            insn == "l.sfnei"):
        return OR1200_OR32_SFXXI
    elif insn == "l.sh":
        return OR1200_OR32_SH
    elif (insn == "l.slli" or
            insn == "l.srai" or
            insn == "l.srli"):
        return OR1200_OR32_SH_ROTI
    elif insn == "l.sw":
        return OR1200_OR32_SW
    elif insn == "l.swa":
        # TODO
        pass
    elif insn == "l.sys":
        # TODO
        pass
    elif insn == "l.trap":
        # TODO
        pass
    elif insn == "l.xori":
        return OR1200_OR32_XORI
    else:
        # Unknown instruction
        raise ValueError


def decode(insn):

    opcode = get_opcode(insn)

    ##################################################
    # DECODE OF ALU_OP
    ##################################################

    # l.movhi
    if opcode == OR1200_OR32_MOVHI:
        alu_op = OR1200_ALUOP_MOVHI

    # l.addi
    elif opcode == OR1200_OR32_ADDI:
        alu_op = OR1200_ALUOP_ADD

    # l.addic
    elif opcode == OR1200_OR32_ADDIC:
        alu_op = OR1200_ALUOP_ADDC

    # l.andi
    elif opcode == OR1200_OR32_ANDI:
        alu_op = OR1200_ALUOP_AND

    # l.ori
    elif opcode == OR1200_OR32_ORI:
        alu_op = OR1200_ALUOP_OR

    # l.xori
    elif opcode == OR1200_OR32_XORI:
        alu_op = OR1200_ALUOP_XOR

    # l.muli
    elif opcode == OR1200_OR32_MULI:
        alu_op = OR1200_ALUOP_MUL

    # Shift and rotate insns with immediate
    elif opcode == OR1200_OR32_SH_ROTI:
        alu_op = OR1200_ALUOP_SHROT

    # SFXX insns with immediate
    elif opcode == OR1200_OR32_SFXXI:
        alu_op = OR1200_ALUOP_COMP

    # ALU insnuctions except the one with immediate
    elif opcode == OR1200_OR32_ALU:
        alu_op = get_aop(insn)

    # SFXX insnuctions
    elif opcode == OR1200_OR32_SFXX:
        alu_op = OR1200_ALUOP_COMP

    # l.cust5
    elif opcode == OR1200_OR32_CUST5:
        alu_op = OR1200_ALUOP_CUST5
    # else
    else:
        alu_op = OR1200_ALUOP_NOP

    ##################################################
    # DECODE OF SPR_READ, SPR_WRITE
    ##################################################

    # l.mfspr
    if opcode == OR1200_OR32_MFSPR:
        spr_read = "1"
        spr_write = "0"

    # l.mtspr
    elif opcode == OR1200_OR32_MTSPR:
        spr_read = "0"
        spr_write = "1"

    # else
    else:
        spr_read = "0"
        spr_write = "0"

    ##################################################
    # DECODE OF ID_LSU_OP
    ##################################################

    # l.lwz
    if opcode == OR1200_OR32_LWZ:
        id_lsu_op = OR1200_LSUOP_LWZ

    # l.lws
    elif opcode == OR1200_OR32_LWS:
        id_lsu_op = OR1200_LSUOP_LWS

    # l.lbz
    elif opcode == OR1200_OR32_LBZ:
        id_lsu_op = OR1200_LSUOP_LBZ

    # l.lbs
    elif opcode == OR1200_OR32_LBS:
        id_lsu_op = OR1200_LSUOP_LBS

    # l.lhz
    elif opcode == OR1200_OR32_LHZ:
        id_lsu_op = OR1200_LSUOP_LHZ

    # l.lhs
    elif opcode == OR1200_OR32_LHS:
        id_lsu_op = OR1200_LSUOP_LHS

    # l.sw
    elif opcode == OR1200_OR32_SW:
        id_lsu_op = OR1200_LSUOP_SW

    # l.sb
    elif opcode == OR1200_OR32_SB:
        id_lsu_op = OR1200_LSUOP_SB

    # l.sh
    elif opcode == OR1200_OR32_SH:
        id_lsu_op = OR1200_LSUOP_SH

    # Non load / store insnuctions
    else:
        id_lsu_op = OR1200_LSUOP_NOP

    ##################################################
    # DECODE OF ID_BRANCH_OP
    ##################################################

    # l.j
    if opcode == OR1200_OR32_J:
        id_branch_op = OR1200_BRANCHOP_J

    # j.jal
    elif opcode == OR1200_OR32_JAL:
        id_branch_op = OR1200_BRANCHOP_J

    # j.jalr
    elif opcode == OR1200_OR32_JALR:
        id_branch_op = OR1200_BRANCHOP_JR

    # l.jr
    elif opcode == OR1200_OR32_JR:
        id_branch_op = OR1200_BRANCHOP_JR

    # l.bnf
    elif opcode == OR1200_OR32_BNF:
        id_branch_op = OR1200_BRANCHOP_BNF

    # l.bf
    elif opcode == OR1200_OR32_BF:
        id_branch_op = OR1200_BRANCHOP_BF

    # l.rfe
    elif opcode == OR1200_OR32_RFE:
        id_branch_op = OR1200_BRANCHOP_RFE

    # Non branch insnuctions
    else:
        id_branch_op = OR1200_BRANCHOP_NOP

    ##################################################
    #  DECODE OF SEL_IMM
    ##################################################

    # j.jalr
    if opcode == OR1200_OR32_JALR:
        sel_imm = "0"

    # l.jr
    elif opcode == OR1200_OR32_JR:
        sel_imm = "0"

    # l.rfe
    elif opcode == OR1200_OR32_RFE:
        sel_imm = "0"

    # l.mfspr
    elif opcode == OR1200_OR32_MFSPR:
        sel_imm = "0"

    # l.mtspr
    elif opcode == OR1200_OR32_MTSPR:
        sel_imm = "0"

    # l.sys, l.brk and all three sync insns
    elif opcode == OR1200_OR32_XSYNC:
        sel_imm = "0"

    # l.mac/l.msb
    elif opcode == OR1200_OR32_MACMSB:
        sel_imm = "0"

    # l.sw
    elif opcode == OR1200_OR32_SW:
        sel_imm = "0"

    # l.sb
    elif opcode == OR1200_OR32_SB:
        sel_imm = "0"

    # l.sh
    elif opcode == OR1200_OR32_SH:
        sel_imm = "0"

    # ALU insnuctions except the one with immediate
    elif opcode == OR1200_OR32_ALU:
        sel_imm = "0"

    # SFXX insnuctions
    elif opcode == OR1200_OR32_SFXX:
        sel_imm = "0"

    # l.cust5 insnuctions
    elif opcode == OR1200_OR32_CUST5:
        sel_imm = "0"

    # FPU insnuctions
    elif opcode == OR1200_OR32_FLOAT:
        sel_imm = "0"
    # l.nop
    elif opcode == OR1200_OR32_NOP:
        sel_imm = "0"

    # All insnuctions with immediates
    else:
        sel_imm = "1"

    ##################################################
    # DECODE OF RFWB_OP
    ##################################################

    # j.jal
    if opcode == OR1200_OR32_JAL:
        rfwb_op = OR1200_RFWBOP_LR + "1"

    # j.jalr
    elif opcode == OR1200_OR32_JALR:
        rfwb_op = OR1200_RFWBOP_LR + "1"

    # l.movhi
    elif opcode == OR1200_OR32_MOVHI:
        rfwb_op = OR1200_RFWBOP_ALU + "1"

    # l.mfspr
    elif opcode == OR1200_OR32_MFSPR:
        rfwb_op = OR1200_RFWBOP_SPRS + "1"

    # l.lwz
    elif opcode == OR1200_OR32_LWZ:
        rfwb_op = OR1200_RFWBOP_LSU + "1"

    # l.lws
    elif opcode == OR1200_OR32_LWS:
        rfwb_op = OR1200_RFWBOP_LSU + "1"

    # l.lbz
    elif opcode == OR1200_OR32_LBZ:
        rfwb_op = OR1200_RFWBOP_LSU + "1"

    # l.lbs
    elif opcode == OR1200_OR32_LBS:
        rfwb_op = OR1200_RFWBOP_LSU + "1"

    # l.lhz
    elif opcode == OR1200_OR32_LHZ:
        rfwb_op = OR1200_RFWBOP_LSU + "1"

    # l.lhs
    elif opcode == OR1200_OR32_LHS:
        rfwb_op = OR1200_RFWBOP_LSU + "1"

    # l.addi
    elif opcode == OR1200_OR32_ADDI:
        rfwb_op = OR1200_RFWBOP_ALU + "1"

    # l.addic
    elif opcode == OR1200_OR32_ADDIC:
        rfwb_op = OR1200_RFWBOP_ALU + "1"

    # l.andi
    elif opcode == OR1200_OR32_ANDI:
        rfwb_op = OR1200_RFWBOP_ALU + "1"

    # l.ori
    elif opcode == OR1200_OR32_ORI:
        rfwb_op = OR1200_RFWBOP_ALU + "1"

    # l.xori
    elif opcode == OR1200_OR32_XORI:
        rfwb_op = OR1200_RFWBOP_ALU + "1"

    # l.muli
    elif opcode == OR1200_OR32_MULI:
        rfwb_op = OR1200_RFWBOP_ALU + "1"

    # Shift and rotate insns with immediate
    elif opcode == OR1200_OR32_SH_ROTI:
        rfwb_op = OR1200_RFWBOP_ALU + "1"

    elif opcode == OR1200_OR32_ALU:
        rfwb_op = OR1200_RFWBOP_ALU + "1"

    # l.cust5 insnuctions
    elif opcode == OR1200_OR32_CUST5:
        rfwb_op = OR1200_RFWBOP_ALU + "1"

    # insnuctions w/o register-file write-back
    else:
        rfwb_op = OR1200_RFWBOP_NOP

    ##################################################
    # DECODE OF ID_LSU_OP
    ##################################################

    # l.lwz
    if opcode == OR1200_OR32_LWZ:
        id_lsu_op = OR1200_LSUOP_LWZ

    # l.lws
    elif opcode == OR1200_OR32_LWS:
        id_lsu_op = OR1200_LSUOP_LWS

    # l.lbz
    elif opcode == OR1200_OR32_LBZ:
        id_lsu_op = OR1200_LSUOP_LBZ

    # l.lbs
    elif opcode == OR1200_OR32_LBS:
        id_lsu_op = OR1200_LSUOP_LBS

    # l.lhz
    elif opcode == OR1200_OR32_LHZ:
        id_lsu_op = OR1200_LSUOP_LHZ

    # l.lhs
    elif opcode == OR1200_OR32_LHS:
        id_lsu_op = OR1200_LSUOP_LHS

    # l.sw
    elif opcode == OR1200_OR32_SW:
        id_lsu_op = OR1200_LSUOP_SW

    # l.sb
    elif opcode == OR1200_OR32_SB:
        id_lsu_op = OR1200_LSUOP_SB

    # l.sh
    elif opcode == OR1200_OR32_SH:
        id_lsu_op = OR1200_LSUOP_SH

    # Non load/store insnuctions
    else:
        id_lsu_op = OR1200_LSUOP_NOP

    ##################################################
    # DECODE OF COMP_OP
    ##################################################

    if opcode == OR1200_OR32_SFXX or opcode == OR1200_OR32_SFXXI:
        comp_op = get_fopc(insn)
    else:
        comp_op = "0000"

    du_word = alu_op + id_branch_op + id_lsu_op + \
        spr_read + spr_write + sel_imm + rfwb_op + id_lsu_op + comp_op

    return du_word


# Internal ALU opcode
def get_aop(insn):
    if insn == "l.add":
        return OR1200_ALUOP_ADD
    elif insn == "l.addc":
        return OR1200_ALUOP_ADDC
    elif insn == "l.and":
        return OR1200_ALUOP_AND
    elif insn == "l.cmov":
        return OR1200_ALUOP_CMOV
    elif insn == "l.div":
        return OR1200_ALUOP_DIV
    elif insn == "l.divu":
        return OR1200_ALUOP_DIVU
    elif insn == "l.extbs":
        return OR1200_ALUOP_EXTHB
    elif insn == "l.extbz":
        return OR1200_ALUOP_EXTHB
    elif insn == "l.exths":
        return OR1200_ALUOP_EXTHB
    elif insn == "l.exthz":
        return OR1200_ALUOP_EXTHB
    elif insn == "l.extws":
        return OR1200_ALUOP_EXTW
    elif insn == "l.extwz":
        return OR1200_ALUOP_EXTW
    elif insn == "l.ff1":
        return OR1200_ALUOP_FFL1
    elif insn == "l.fl1":
        return OR1200_ALUOP_FFL1
    elif insn == "l.movhi":
        return OR1200_ALUOP_MOVHI
    elif insn == "l.mul":
        return OR1200_ALUOP_MUL
    elif insn == "l.mulu":
        return OR1200_ALUOP_MULU
    elif insn == "l.or":
        return OR1200_ALUOP_OR
    elif insn == "l.ror":
        return OR1200_ALUOP_SHROT
    elif insn == "l.sll":
        return OR1200_ALUOP_SHROT
    elif insn == "l.sra":
        return OR1200_ALUOP_SHROT
    elif insn == "l.srl":
        return OR1200_ALUOP_SHROT
    elif insn == "l.sub":
        return OR1200_ALUOP_SUB
    elif insn == "l.xor":
        return OR1200_ALUOP_XOR
    else:
        raise ValueError


# Instruction ALU opcode
def get_extra_opcode(insn):
    if insn == "l.add":
        return "00000000"
    if insn == "l.addc":
        return "00000001"
    if insn == "l.and":
        return "00000011"
    if insn == "l.cmov":
        return "00001110"
    if insn == "l.div":
        return "11001001"
    if insn == "l.divu":
        return "11001010"
    if insn == "l.extbs":
        return "00011100"
    if insn == "l.extbz":
        return "00111100"
    if insn == "l.exths":
        return "00001100"
    if insn == "l.exthz":
        return "00101100"
    if insn == "l.extws":
        return "00001101"
    if insn == "l.extwz":
        return "00011101"
    if insn == "l.ff1":
        return "00001111"
    if insn == "l.fl1":
        return "01001111"
    if insn == "l.mul":
        return "11000110"
    if insn == "l.muld":
        # TODO
        pass
    if insn == "l.muldu":
        # TODO
        pass
    if insn == "l.mulu":
        return "11001011"
    if insn == "l.or":
        return "00000100"
    if insn == "l.sll":
        return "00001000"
    if insn == "l.sra":
        return "00101000"
    if insn == "l.srl":
        return "00011000"
    if insn == "l.sub":
        return "00000010"
    if insn == "l.xor":
        return "00000101"
    else:
        # Unknown instruction
        raise ValueError


# Instruction/Internal flag opcode
def get_fopc(name):
    if name == "l.sfeq" or name == "l.sfeqi":
        return "0000"
    elif name == "l.sfges" or name == "l.sfgesi":
        return "1011"
    elif name == "l.sfgeu" or name == "l.sfgeui":
        return "0011"
    elif name == "l.sfgts" or name == "l.sfgtsi":
        return "1010"
    elif name == "l.sfgtu" or name == "l.sfgtui":
        return "0010"
    elif name == "l.sfles" or name == "l.sflesi":
        return "1101"
    elif name == "l.sfleu" or name == "l.sfleui":
        return "0101"
    elif name == "l.sflts" or name == "l.sfltsi":
        return "1100"
    elif name == "l.sfltu" or name == "l.sfltui":
        return "0100"
    elif name == "l.sfne" or name == "l.sfnei":
        return "0001"
    else:
        # Unknown instruction
        raise ValueError


# Index used to LUT addressing and docs
def get_index(name):
    if name == "l.j":
        return 0
    elif name == "l.jal":
        return 1
    elif name == "l.bnf":
        return 2
    elif name == "l.bf":
        return 3
    elif name == "l.nop":
        return 4
    elif name == "l.macrc":
        return 5
    elif name == "l.movhi":
        return 6
    elif name == "l.sys":
        return 7
    elif name == "l.trap":
        return 8
    elif name == "l.msync":
        return 9
    elif name == "l.psync":
        return 10
    elif name == "l.csync":
        return 11
    elif name == "l.rfe":
        return 12
    elif name == "l.jr":
        return 13
    elif name == "l.jalr":
        return 14
    elif name == "l.maci":
        return 15
    elif name == "l.cust1":
        return 16
    elif name == "l.cust2":
        return 17
    elif name == "l.cust3":
        return 18
    elif name == "l.cust4":
        return 19
    elif name == "l.ld":
        return 20
    elif name == "l.lwz":
        return 21
    elif name == "l.lws":
        return 22
    elif name == "l.lbz":
        return 23
    elif name == "l.lbs":
        return 24
    elif name == "l.lhz":
        return 25
    elif name == "l.lhs":
        return 26
    elif name == "l.addi":
        return 27
    elif name == "l.addic":
        return 28
    elif name == "l.andi":
        return 29
    elif name == "l.ori":
        return 30
    elif name == "l.xori":
        return 31
    elif name == "l.muli":
        return 32
    elif name == "l.mfspr":
        return 33
    elif name == "l.slli":
        return 34
    elif name == "l.srli":
        return 35
    elif name == "l.srai":
        return 36
    elif name == "l.rori":
        return 37
    elif name == "l.sfeqi":
        return 38
    elif name == "l.sfnei":
        return 39
    elif name == "l.sfgtui":
        return 40
    elif name == "l.sfgeui":
        return 41
    elif name == "l.sfltui":
        return 42
    elif name == "l.sfleui":
        return 43
    elif name == "l.sfgtsi":
        return 44
    elif name == "l.sfgesi":
        return 45
    elif name == "l.sfltsi":
        return 46
    elif name == "l.sflesi":
        return 47
    elif name == "l.mtspr":
        return 48
    elif name == "l.mac":
        return 49
    elif name == "l.macu":
        return 50
    elif name == "l.msb":
        return 51
    elif name == "l.msbu":
        return 52
    elif name == "l.swa":
        return 53
    elif name == "l.sd":
        return 54
    elif name == "l.sw":
        return 55
    elif name == "l.sb":
        return 56
    elif name == "l.sh":
        return 57
    elif name == "l.exths":
        return 58
    elif name == "l.extws":
        return 59
    elif name == "l.extbs":
        return 60
    elif name == "l.extwz":
        return 61
    elif name == "l.exthz":
        return 62
    elif name == "l.extbz":
        return 63
    elif name == "l.add":
        return 64
    elif name == "l.addc":
        return 65
    elif name == "l.sub":
        return 66
    elif name == "l.and":
        return 67
    elif name == "l.or":
        return 68
    elif name == "l.xor":
        return 69
    elif name == "l.cmov":
        return 70
    elif name == "l.ff1":
        return 71
    elif name == "l.sll":
        return 72
    elif name == "l.srl":
        return 73
    elif name == "l.sra":
        return 74
    elif name == "l.ror":
        return 75
    elif name == "l.fl1":
        return 76
    elif name == "l.mul":
        return 77
    elif name == "l.muld":
        return 78
    elif name == "l.div":
        return 79
    elif name == "l.divu":
        return 80
    elif name == "l.mulu":
        return 81
    elif name == "l.muldu":
        return 82
    elif name == "l.sfeq":
        return 83
    elif name == "l.sfne":
        return 84
    elif name == "l.sfgtu":
        return 85
    elif name == "l.sfgeu":
        return 86
    elif name == "l.sfltu":
        return 87
    elif name == "l.sfleu":
        return 88
    elif name == "l.sfgts":
        return 89
    elif name == "l.sfges":
        return 90
    elif name == "l.sflts":
        return 91
    elif name == "l.sfles":
        return 92
    elif name == "l.cust5":
        return 93
    elif name == "l.cust6":
        return 94
    elif name == "l.cust7":
        return 95
    elif name == "l.cust8":
        return 96
    else:
        # Unknown instruction
        raise ValueError
