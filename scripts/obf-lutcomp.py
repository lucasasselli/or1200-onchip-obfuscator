#!/usr/bin/python3
import argparse
import logging
from core import utils
from core import decoder
import re
import os


# Configuration
SHARED_POINTERS_ENABLED = True

# Constants
INSN_TYPE_N = "000"
INSN_TYPE_A = "001"
INSN_TYPE_I = "010"
INSN_TYPE_M = "011"


def remove_whitespace(x):
    return re.sub("\s*,\s*", ",", x)


def bin_digits(x, bits):
    n = int(x)
    s = bin(n & int("1" * bits, 2))[2:]
    return ("{0:0>%s}" % (bits)).format(s)


def is_sublist(a, b, start=0):
    if a == []:
        return start
    if b == []:
        return -1
    if b[:len(a)] == a:
        return start
    else:
        return is_sublist(a, b[1:], start + 1)


def get_D_field(x):
    if x == "r0":
        # Use r0 as rD
        return "1"
    elif x == "rD":
        # Use original rD
        return "0"
    else:
        logging.error("%s cannot be used as rD", x)
        raise ValueError


def get_A_field(x):
    if x == "rA":
        # Use original rA
        return "00"
    elif x == "rB":
        # Use rB as rA
        return "01"
    elif x == "rD":
        # Use rD as rA
        return "10"
    elif x == "r0":
        # Use r0 as rA
        return "11"
    else:
        logging.error("%s cannot be used as rA", x)
        raise ValueError


def get_B_field(x):
    if x == "r0":
        # Use r0 as rB
        return "1"
    elif x == "rB":
        # Use original rB
        return "0"
    else:
        logging.error("%s cannot be used as rB", x)
        raise ValueError


def get_I_field(x):
    if x == "I" or x == "K" or x == "L":
        # Use original immediate
        return "00"
    elif x == "0":
        # Use custom null immediate
        return "01"
    else:
        # Use custom 16bit immediate
        return "10"


def get_index(name):
    if name == "l.j":
        return 0
    if name == "l.jal":
        return 1
    if name == "l.bnf":
        return 2
    if name == "l.bf":
        return 3
    if name == "l.nop":
        return 4
    if name == "l.macrc":
        return 5
    if name == "l.movhi":
        return 6
    if name == "l.sys":
        return 7
    if name == "l.trap":
        return 8
    if name == "l.msync":
        return 9
    if name == "l.psync":
        return 10
    if name == "l.csync":
        return 11
    if name == "l.rfe":
        return 12
    if name == "l.jr":
        return 13
    if name == "l.jalr":
        return 14
    if name == "l.maci":
        return 15
    if name == "l.cust1":
        return 16
    if name == "l.cust2":
        return 17
    if name == "l.cust3":
        return 18
    if name == "l.cust4":
        return 19
    if name == "l.ld":
        return 20
    if name == "l.lwz":
        return 21
    if name == "l.lws":
        return 22
    if name == "l.lbz":
        return 23
    if name == "l.lbs":
        return 24
    if name == "l.lhz":
        return 25
    if name == "l.lhs":
        return 26
    if name == "l.addi":
        return 27
    if name == "l.addic":
        return 28
    if name == "l.andi":
        return 29
    if name == "l.ori":
        return 30
    if name == "l.xori":
        return 31
    if name == "l.muli":
        return 32
    if name == "l.mfspr":
        return 33
    if name == "l.slli":
        return 34
    if name == "l.srli":
        return 35
    if name == "l.srai":
        return 36
    if name == "l.rori":
        return 37
    if name == "l.sfeqi":
        return 38
    if name == "l.sfnei":
        return 39
    if name == "l.sfgtui":
        return 40
    if name == "l.sfgeui":
        return 41
    if name == "l.sfltui":
        return 42
    if name == "l.sfleui":
        return 43
    if name == "l.sfgtsi":
        return 44
    if name == "l.sfgesi":
        return 45
    if name == "l.sfltsi":
        return 46
    if name == "l.sflesi":
        return 47
    if name == "l.mtspr":
        return 48
    if name == "l.mac":
        return 49
    if name == "l.macu":
        return 50
    if name == "l.msb":
        return 51
    if name == "l.msbu":
        return 52
    if name == "l.swa":
        return 53
    if name == "l.sd":
        return 54
    if name == "l.sw":
        return 55
    if name == "l.sb":
        return 56
    if name == "l.sh":
        return 57
    if name == "l.exths":
        return 58
    if name == "l.extws":
        return 59
    if name == "l.extbs":
        return 60
    if name == "l.extwz":
        return 61
    if name == "l.exthz":
        return 62
    if name == "l.extbz":
        return 63
    if name == "l.add":
        return 64
    if name == "l.addc":
        return 65
    if name == "l.sub":
        return 66
    if name == "l.and":
        return 67
    if name == "l.or":
        return 68
    if name == "l.xor":
        return 69
    if name == "l.cmov":
        return 70
    if name == "l.ff1":
        return 71
    if name == "l.sll":
        return 72
    if name == "l.srl":
        return 73
    if name == "l.sra":
        return 74
    if name == "l.ror":
        return 75
    if name == "l.fl1":
        return 76
    if name == "l.mul":
        return 77
    if name == "l.muld":
        return 78
    if name == "l.div":
        return 79
    if name == "l.divu":
        return 80
    if name == "l.mulu":
        return 81
    if name == "l.muldu":
        return 82
    if name == "l.sfeq":
        return 83
    if name == "l.sfne":
        return 84
    if name == "l.sfgtu":
        return 85
    if name == "l.sfgeu":
        return 86
    if name == "l.sfltu":
        return 87
    if name == "l.sfleu":
        return 88
    if name == "l.sfgts":
        return 89
    if name == "l.sfges":
        return 90
    if name == "l.sflts":
        return 91
    if name == "l.sfles":
        return 92
    if name == "l.cust5":
        return 93
    if name == "l.cust6":
        return 94
    if name == "l.cust7":
        return 95
    if name == "l.cust8":
        return 96
    else:
        raise ValueError


def get_lut_line(line, ref, stop):

    line_find = re.findall(r"l\.", line)

    if len(line_find) == 0:
        logging.error("Unable to identify instruction: %s", line)
        raise ValueError

    if len(line_find) > 1:
        logging.error("Missing newline: %s", line)
        raise ValueError

    line_split = line.split()

    if len(line_split) > 2:
        logging.error("Junk at the end of the line: %s", line)
        raise ValueError

    if len(line_split) <= 1 and line_split[0] != "l.nop":
        logging.error("Missing space between instruction and operands: %s", line)
        raise ValueError

    insn_name = line_split[0]
    if len(line_split) > 1:
        insn_oper = line_split[1]

    # Get instruction opcode
    insn_opcode = decoder.get_opcode(insn_name)

    # Get instruction type
    if insn_opcode == decoder.OR1200_OR32_ALU:
        # Type A
        insn_type = INSN_TYPE_A
        logging.debug("Instruction %s is type A", line)
    elif(insn_opcode[:2] == "10" or
            insn_opcode == decoder.OR1200_OR32_MOVHI or
            insn_opcode == decoder.OR1200_OR32_RFE):
        # Type I
        insn_type = INSN_TYPE_I
        logging.debug("Instruction %s is type I", line)
    elif(insn_opcode == decoder.OR1200_OR32_MTSPR or
            insn_opcode == decoder.OR1200_OR32_SW or
            insn_opcode == decoder.OR1200_OR32_SH or
            insn_opcode == decoder.OR1200_OR32_SB):
        # Type M
        insn_type = INSN_TYPE_M
        logging.debug("Instruction %s is type M", line)
    else:
        # Type N
        insn_type = INSN_TYPE_N
        logging.debug("Instruction %s is type N", line)

    # Generate output
    if stop:
        stop_field = "1"
    else:
        stop_field = "0"

    # Force type N
    if line == ref and SHARED_POINTERS_ENABLED:
        logging.debug("Substitution is identical to reference, force N type")
        insn_type = INSN_TYPE_N

    out_array = []

    if insn_type == INSN_TYPE_A:
        insn_oper_split = insn_oper.split(",")

        if len(insn_oper_split) != 3:
            if insn_name == "l.ff1" or insn_name == "l.fl1" or ("l.ext" in insn_name):
                insn_oper_split.append("r0")
            else:
                logging.error("Unable to parse operands: %s", line)
                raise ValueError

        D_field = get_D_field(insn_oper_split[0])
        A_field = get_A_field(insn_oper_split[1])
        B_field = get_B_field(insn_oper_split[2])
        OP12_field = decoder.get_extra_opcode(insn_name)

        lut_word = insn_type + OP12_field + D_field + A_field + B_field + stop_field
        out_array.append(lut_word)

        return out_array

    if insn_type == INSN_TYPE_I:

        insn_oper_split = insn_oper.split(",")

        if len(insn_oper_split) != 3:
            if len(insn_oper_split) == 2 and "(" in insn_oper_split[1]:
                # Load instruction
                temp_array = re.findall(r"(.*?)\((.*?)\)", insn_oper_split[1])
                insn_oper_split[1] = temp_array[0][1]
                insn_oper_split.append(temp_array[0][0])
            elif len(insn_oper_split) == 2 and insn_name == "l.movhi":
                # Special instructions
                insn_oper_split.append(insn_oper_split[1])
                insn_oper_split[1] = "r0"
            else:
                # Error
                logging.error("Unable to parse operands: %s", line)
                raise ValueError

        D_field = get_D_field(insn_oper_split[0])
        A_field = get_A_field(insn_oper_split[1])
        I_field = get_I_field(insn_oper_split[2])
        OP0_field = decoder.get_opcode(insn_name)

        lut_word = insn_type + OP0_field + I_field + D_field + A_field + "0" + stop_field
        out_array.append(lut_word)

        if I_field == "10":
            out_array.append(bin_digits(insn_oper_split[2], 16))

        return out_array

    if insn_type == INSN_TYPE_M:

        insn_oper_split = insn_oper.split(",")

        if len(insn_oper_split) != 3:
            if len(insn_oper_split) == 2 and "(" in insn_oper_split[0]:
                # Load instruction
                temp_array = re.findall(r"(.*?)\((.*?)\)", insn_oper_split[0])
                temp = []
                temp.append(temp_array[0][1])
                temp.append(insn_oper_split[1])
                temp.append(temp_array[0][0])
                insn_oper_split = temp
            else:
                # Error
                logging.error("Unable to parse operands: %s", line)
                raise ValueError

        A_field = get_A_field(insn_oper_split[0])
        B_field = get_B_field(insn_oper_split[1])
        I_field = get_I_field(insn_oper_split[2])
        OP0_field = decoder.get_opcode(insn_name)

        lut_word = insn_type + OP0_field + I_field + "0" + A_field + B_field + stop_field
        out_array.append(lut_word)

        if I_field == "10":
            out_array.append(bin_digits(insn_oper_split[2], 16))

        return out_array

    return [INSN_TYPE_N + 12 * "0" + stop_field]


def write_out_file(out_file, template_file, sub_array):
    # Read in the file
    res_path = utils.get_res_path()

    template_path = os.path.join(res_path, template_file)

    with open(template_path, 'r') as file:
        filedata = file.read()

    # Replace the target string
    for sub in sub_array:
        filedata = filedata.replace(sub[0], sub[1])

    # Write the file out again
    with open(out_file, 'w') as file:
        file.write(filedata)


def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description="Generate LUT content for hardware obfuscator")
    parser.add_argument("file", type=str, help="input file")
    parser.add_argument("-d", "--debug", action='store_true', help="enable debug output")
    args = parser.parse_args()

    # Logger
    utils.init_logger(debug=args.debug, log_to_file=False)

    # Read table
    insn_ref_array, insn_sub_table = utils.load_sub_table(args.file)

    # Compile
    logging.info("Compiler running...")

    lut_number = 0  # Stores the number of luts

    # Run initial analysis
    for insn_sub_row in insn_sub_table:
        lut_number = max(len(insn_sub_row), lut_number)

    logging.debug("LUT number is %d", lut_number)

    # Run compilation
    for lut_index in range(0, lut_number):

        lut_pointer = 0
        lut_content = []
        lut_decoder = []

        logging.info("Compiling LUT %d", lut_index)

        # First line is reserved to missing substitutions
        lut_content.append(15 * "0" + "1")
        lut_pointer += 1

        for insn_index, insn_sub_row in enumerate(insn_sub_table):
            if lut_index >= len(insn_sub_row):
                logging.warning("[%d:%d] Missing substitution", lut_index, insn_index)
                continue

            sub_asm = insn_sub_row[lut_index].insn_sub
            sub_asm_split = sub_asm.split("\n")

            # Get reference index
            ref_insn = insn_ref_array[insn_index]
            ref_insn_split = ref_insn.split()
            decoder_index = get_index(ref_insn_split[0])

            temp_lut_content = []

            for line_index, line in enumerate(sub_asm_split):

                stop = (line_index == len(sub_asm_split) - 1)

                # Clean input
                line = remove_whitespace(line)
                ref_insn = remove_whitespace(ref_insn)

                try:
                    lut_word = get_lut_line(line, ref_insn, stop)
                except ValueError:
                    logging.error("[%d:%d:%d] Error while parsing substitution: %s", lut_index, insn_index, line_index, line)
                    exit()

                temp_lut_content += lut_word

            # Add substitution to decoder
            match_pointer = is_sublist(temp_lut_content, lut_content)
            if(match_pointer >= 0 and SHARED_POINTERS_ENABLED):
                logging.debug("[%d:%d] Substituion found at LUT index %d", lut_index, insn_index, match_pointer)

                # Add reference to decoder
                decoder_word = [decoder_index, match_pointer]
                lut_decoder.append(decoder_word)
            else:
                # Add substitution to decoder
                decoder_word = [decoder_index, lut_pointer]
                lut_decoder.append(decoder_word)

                # Add substitution to LUT
                lut_content += temp_lut_content
                lut_pointer += len(temp_lut_content)

        # Write decoder content
        decoder_body = ""
        for lut_decoder_word in lut_decoder:
            decoder_body += "\t\t`OBF_IGU_WIDTH'd{:}: addr = `OBF_LUT_ADDR_WIDTH'd{:};\n".format(lut_decoder_word[0], lut_decoder_word[1])
        decoder_sub_array = [("%index%", str(lut_index)), ("%body%", decoder_body)]
        write_out_file("obf_pt{:}.v".format(lut_index), "pt_template", decoder_sub_array)

        # Write lut content
        lut_body = ""
        for lut_word_index, lut_word in enumerate(lut_content):
            lut_body += "\tlut[{:}] = 16'b{:};\n".format(lut_word_index, lut_word)
        lut_sub_array = [("%index%", str(lut_index)), ("%lenght%", str(len(lut_content)-1)), ("%body%", lut_body)]
        write_out_file("obf_lut{:}.v".format(lut_index), "lut_template", lut_sub_array)


if __name__ == "__main__":
    main()
