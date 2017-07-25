#!/usr/bin/python3

import argparse
from common import mylogger
from common import tabreader
from common import decoder
from common import mathutils


def test(i):
    # Print header
    logger.set_indent(0)
    logger.println("#" * 50)
    logger.println("Instruction ", i + 1, " ", instr_ref_array[i])
    logger.println("#" * 50, "\n")

    # Compute DU word of reference instruction
    ref_du_word = decoder.parse(instr_ref_array[i])
    if not ref_du_word:
        logger.println("ERROR: Unsupported instruction\n")
        return

    # DEBUG
    if args.debug:
        logger.println("REFERENCE:")
        logger.set_indent(1)
        logger.println(ref_du_word, "\n")

    # Test substitutions
    instr_sub_array = instr_sub_table[i]
    for j in range(0, len(instr_sub_array)):

        logger.set_indent(0)
        logger.println("Substitution ", j + 1, ": ")

        # Compute DU word of the substitution
        skip = 0

        sub_du_words = []
        jaccd_scores = []
        smd_scores = []

        for op in instr_sub_array[j].split():
            if "l." in op:
                try:
                    sub_du_word = decoder.decode(op)
                    sub_du_words.append(sub_du_word)
                    jaccd_scores.append(mathutils.jaccd(ref_du_word, sub_du_word))
                    smd_scores.append(mathutils.smd(ref_du_word, sub_du_word))
                except ValueError:
                    skip = 1
                    logger.set_indent(1)
                    logger.println("ERROR: Unsupported instruction")

        if skip == 0:
            jaccd_score = sum(jaccd_scores) / float(len(jaccd_scores))
            smd_score = sum(smd_scores) / float(len(smd_scores))

            logger.set_indent(1)
            logger.println("J: ", jaccd_score)
            logger.println("SMD: ", smd_score)

            # DEBUG
            if args.debug:
                for i in range(0, len(sub_du_words)):
                    logger.print(sub_du_words[i])
                    logger.println("\t", jaccd_scores[i], "\t", smd_scores[i])

        logger.println("")

    return


# Parse arguments
parser = argparse.ArgumentParser(description="Test Open RISC 1000 instruction set substitution.")
parser.add_argument("file", type=str, help="input file")
parser.add_argument("-i", type=int, default=-1, help="instruction to test")
parser.add_argument("-o", "--out", type=str, default="du-score.log", help="log file")
parser.add_argument("-d", "--debug", action='store_true', help="enable debug output")

args = parser.parse_args()


# Logger
logger = mylogger.Logger(args.out)
logger.println("Starting DU score test...\n")

# Read table
f = open(args.file, 'rt')
instr_ref_array, instr_sub_table = tabreader.load_table(f, 1)

# Run test
if args.i >= 0:
    # Selected instruction
    if args.i < len(instr_ref_array):
        test(args.i)
    else:
        logger.println("ERROR: Index out of range")
else:
    # All instructions
    for i in range(0, len(instr_ref_array)):
        test(i)


logger.set_indent(0)
logger.println("Test completed!")
