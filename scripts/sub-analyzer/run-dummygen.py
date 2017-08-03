#!/usr/bin/python3
import argparse
from operator import itemgetter
import decoder
import utils
import logging


# Parse arguments
parser = argparse.ArgumentParser(description="Compute Open RISC 1000 optimal dummy instruction set substitution.")
parser.add_argument("-o", "--out", type=str, default="dummygen.log", help="log file")
parser.add_argument("-d", "--debug", action='store_true', help="enable debug output")

args = parser.parse_args()

# Logger
utils.init_logger(args.out)

# Read instruction list
instr_list = []
instr_file_name = "other/instr_list"

with open(instr_file_name, 'r') as f:
    for line in f:
        instr_list.append(line.rstrip())


# Read dummy list
dummy_list = []
dummy_file_name = "other/dummy_list"

with open(dummy_file_name, 'r') as f:
    for line in f:
        dummy_list.append(line.rstrip())

result_table = []

for instr in instr_list:
    # find dummy instr with max smd
    try:
        instr_word = decoder.parse(instr)
    except ValueError:
        logging.warning("Unable to decode instruction %s", instr)
        continue

    dummy_table = []

    for dummy in dummy_list:
        try:
            dummy_word = decoder.parse(dummy)
        except ValueError:
            logging.warning("Unable to decode dummy %s", dummy)
            continue

        smd = utils.smd(instr_word, dummy_word)
        jaccd = utils.jaccd(instr_word, dummy_word)

        dummy_table.append((dummy, dummy_word, smd, jaccd))

    # Sort and crop dummy table
    dummy_table = sorted(dummy_table, key=itemgetter(2), reverse=True)
    dummy_table = dummy_table[0:4]

    result_table.append((instr, instr_word, dummy_table))

# Print the result
for result in result_table:
    # Print header
    logging.info(50*'#')
    logging.info("%s %s", result[0], result[1])
    logging.info(50*'#')

    # Print table
    for dummy in result[2]:
        logging.info("{:<20}{:<25}{:<5.2f}{:.2f}".format(dummy[0], dummy[1], dummy[2], dummy[3]))
