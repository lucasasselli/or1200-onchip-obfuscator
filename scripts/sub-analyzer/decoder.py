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


def parse(instr):
    word = ""

    for op in instr.split():
        if "l." in op:
            word = decode(op)
            break

    if not word:
        raise ValueError

    return word


def get_opcode(instr):

    if (instr == "l.add" or
            instr == "l.and" or
            instr == "l.cmov" or
            instr == "l.div" or
            instr == "l.divu" or
            instr == "l.extbs" or
            instr == "l.extbz" or
            instr == "l.exths" or
            instr == "l.exthz" or
            instr == "l.extws" or
            instr == "l.extwz" or
            instr == "l.ff1" or
            instr == "l.fl1" or
            instr == "l.movhi" or
            instr == "l.mul" or
            instr == "l.muld" or
            instr == "l.muldu" or
            instr == "l.mulu" or
            instr == "l.or" or
            instr == "l.sll" or
            instr == "l.sra" or
            instr == "l.srl" or
            instr == "l.sub" or
            instr == "l.xor"):
        return OR1200_OR32_ALU
    if instr == "l.addi":
        return OR1200_OR32_ADDI
    elif instr == "l.addc" or instr == "l.addic":
        return OR1200_ALUOP_ADDC
    elif instr == "l.andi":
        return OR1200_OR32_ANDI
    elif instr == "l.bf":
        return OR1200_OR32_BF
    elif instr == "l.bnf":
        return OR1200_OR32_BNF
    elif (instr == "l.csync" or
            instr == "l.msync" or
            instr == "l.psync"):
        return OR1200_OR32_XSYNC
    elif (instr == "l.cust1" or
            instr == "l.cust2" or
            instr == "l.cust3" or
            instr == "l.cust4" or
            instr == "l.cust5" or
            instr == "l.cust6" or
            instr == "l.cust7" or
            instr == "l.cust8"):
        # TODO
        pass
    elif instr == "l.j":
        return OR1200_OR32_J
    elif instr == "l.jal":
        return OR1200_OR32_JAL
    elif instr == "l.jalr":
        return OR1200_OR32_JALR
    elif instr == "l.jr":
        return OR1200_OR32_JR
    elif instr == "l.lbs":
        return OR1200_OR32_LBS
    elif instr == "l.lbz":
        return OR1200_OR32_LBZ
    elif instr == "l.lhs":
        return OR1200_OR32_LHS
    elif instr == "l.lhz":
        return OR1200_OR32_LHZ
    elif instr == "l.lws":
        return OR1200_OR32_LWS
    elif instr == "l.lwz":
        return OR1200_OR32_LWZ
    elif (instr == "l.mac" or
            instr == "l.msb" or
            instr == "l.msbu"):
        return OR1200_OR32_MACMSB
    elif instr == "l.maci":
        return OR1200_OR32_MACI
    elif instr == "l.macrc":
        return OR1200_OR32_MACRC
    elif instr == "l.mfspr":
        return OR1200_OR32_MFSPR
    elif instr == "l.mtspr":
        return OR1200_OR32_MTSPR
    elif instr == "l.muli":
        return OR1200_OR32_MULI
    elif instr == "l.nop":
        return OR1200_OR32_NOP
    elif instr == "l.ori":
        return OR1200_OR32_ORI
    elif instr == "l.rfe":
        return OR1200_OR32_RFE
    elif instr == "l.rori":
        return OR1200_OR32_SH_ROTI
    elif instr == "l.sb":
        return OR1200_OR32_SB
    elif instr == "l.sd":
        # TODO
        pass
    elif (instr == "l.sfeq" or
            instr == "l.sfges" or
            instr == "l.sfgeu" or
            instr == "l.sfgts" or
            instr == "l.sfgtu" or
            instr == "l.sfles" or
            instr == "l.sfleu" or
            instr == "l.sflts" or
            instr == "l.sfltu" or
            instr == "l.sfne"):
        return OR1200_OR32_SFXX
    elif (instr == "l.sfeqi" or
            instr == "l.sfgesi" or
            instr == "l.sfgeui" or
            instr == "l.sfgtsi" or
            instr == "l.sfgtui" or
            instr == "l.sflesi" or
            instr == "l.sfleui" or
            instr == "l.sfltsi" or
            instr == "l.sfltui" or
            instr == "l.sfnei"):
        return OR1200_OR32_SFXXI
    elif instr == "l.sh":
        return OR1200_OR32_SH
    elif (instr == "l.slli" or
            instr == "l.srai" or
            instr == "l.srli"):
        return OR1200_OR32_SH_ROTI
    elif instr == "l.sw":
        return OR1200_OR32_SW
    elif instr == "l.swa":
        # TODO
        pass
    elif instr == "l.sys":
        # TODO
        pass
    elif instr == "l.trap":
        # TODO
        pass
    elif instr == "l.xori":
        return OR1200_OR32_XORI
    else:
        # TODO
        pass

    logging.warn("(Decoder) Unable to get opcode of %s", instr)
    raise ValueError


def decode(instr):

    opcode = get_opcode(instr)

    #
    # Decode of alu_op
    #

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

    # ALU instructions except the one with immediate
    elif opcode == OR1200_OR32_ALU:
        alu_op = get_alu_op(instr)

    # SFXX instructions
    elif opcode == OR1200_OR32_SFXX:
        alu_op = OR1200_ALUOP_COMP

    # l.cust5
    elif opcode == OR1200_OR32_CUST5:
        alu_op = OR1200_ALUOP_CUST5

    # else
    else:
        alu_op = OR1200_ALUOP_NOP

    #
    # Decode of spr_read, spr_write
    #

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

    #
    # Decode of id_lsu_op
    #

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

    # Non load / store instructions
    else:
        id_lsu_op = OR1200_LSUOP_NOP

    #
    # Decode of id_branch_op
    #
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

    # Non branch instructions
    else:
        id_branch_op = OR1200_BRANCHOP_NOP

    #
    #  Decode of sel_imm
    #
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

    # ALU instructions except the one with immediate
    elif opcode == OR1200_OR32_ALU:
        sel_imm = "0"

    # SFXX instructions
    elif opcode == OR1200_OR32_SFXX:
        sel_imm = "0"

    # l.cust5 instructions
    elif opcode == OR1200_OR32_CUST5:
        sel_imm = "0"

    # FPU instructions
    elif opcode == OR1200_OR32_FLOAT:
        sel_imm = "0"
    # l.nop
    elif opcode == OR1200_OR32_NOP:
        sel_imm = "0"

    # All instructions with immediates
    else:
        sel_imm = "1"

    #
    # Decode of rfwb_op
    #
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

    # l.cust5 instructions
    elif opcode == OR1200_OR32_CUST5:
        rfwb_op = OR1200_RFWBOP_ALU + "1"

    # Instructions w/o register-file write-back
    else:
        rfwb_op = OR1200_RFWBOP_NOP

    #
    # Decode of id_lsu_op
    #
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

    # Non load/store instructions
    else:
        id_lsu_op = OR1200_LSUOP_NOP

    du_word = alu_op + id_branch_op + id_lsu_op + \
        spr_read + spr_write + sel_imm + rfwb_op + id_lsu_op

    return du_word


def get_alu_op(instr):
    if instr == "l.add":
        return OR1200_ALUOP_ADD
    if instr == "l.and":
        return OR1200_ALUOP_AND
    if instr == "l.cmov":
        return OR1200_ALUOP_CMOV
    if instr == "l.div":
        return OR1200_ALUOP_DIV
    if instr == "l.divu":
        return OR1200_ALUOP_DIVU
    if instr == "l.extbs":
        return OR1200_ALUOP_EXTHB
    if instr == "l.extbz":
        return OR1200_ALUOP_EXTHB
    if instr == "l.exths":
        return OR1200_ALUOP_EXTHB
    if instr == "l.exthz":
        return OR1200_ALUOP_EXTHB
    if instr == "l.extws":
        return OR1200_ALUOP_EXTW
    if instr == "l.extwz":
        return OR1200_ALUOP_EXTW
    if instr == "l.ff1":
        return OR1200_ALUOP_FFL1
    if instr == "l.fl1":
        return OR1200_ALUOP_FFL1
    if instr == "l.movhi":
        return OR1200_ALUOP_MOVHI
    if instr == "l.mul":
        return OR1200_ALUOP_MUL
    if instr == "l.muld":
        # TODO
        pass
    if instr == "l.muldu":
        # TODO
        pass
    if instr == "l.mulu":
        return OR1200_ALUOP_MULU
    if instr == "l.or":
        return OR1200_ALUOP_OR
    if instr == "l.sll":
        return OR1200_ALUOP_SHROT
    if instr == "l.sra":
        return OR1200_ALUOP_SHROT
    if instr == "l.srl":
        return OR1200_ALUOP_SHROT
    if instr == "l.sub":
        return OR1200_ALUOP_SUB
    if instr == "l.xor":
        return OR1200_ALUOP_XOR
    else:
        # TODO
        pass

    logging.warn("(Decoder) Unable to get ALU opcode of %s", instr)
    raise ValueError