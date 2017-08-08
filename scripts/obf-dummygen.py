#!/usr/bin/python3
import os
import argparse
import logging
from operator import itemgetter

from core import decoder
from core import utils

# Constants
PATH_INSN = "insn_list"
PATH_DUMMY = "dummy_list"


def list_from_file(file_path):
    temp_list = []

    with open(file_path, 'r') as f:
        for line in f:
            temp_list.append(line.rstrip())

    return temp_list


def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description="Compute Open RISC 1000 optimal dummy instruction set substitution.")
    parser.add_argument("-o", "--out", type=str, default="dummygen.log", help="log file")
    parser.add_argument("-d", "--debug", action='store_true', help="enable debug output")
    args = parser.parse_args()

    # Logger
    utils.init_logger(args.out)

    # Read files
    PATH_RES = utils.get_res_path()

    insn_file_path = os.path.join(PATH_RES, PATH_INSN)
    insn_list = list_from_file(insn_file_path)

    dummy_file_path = os.path.join(PATH_RES, PATH_DUMMY)
    dummy_list = list_from_file(dummy_file_path)

    result_table = []

    for insn in insn_list:
        # find dummy insn with max smd
        try:
            insn_word = decoder.parse(insn)
        except ValueError:
            logging.warning("Unable to decode instruction %s", insn)
            continue

        dummy_table = []

        for dummy in dummy_list:
            try:
                dummy_word = decoder.parse(dummy)
            except ValueError:
                logging.warning("Unable to decode dummy %s", dummy)
                continue

            smd = utils.dscore(insn_word, dummy_word, "smd")
            jaccd = utils.dscore(insn_word, dummy_word, "jaccd")

            dummy_table.append((dummy, dummy_word, smd, jaccd))

        # Sort and crop dummy table
        dummy_table = sorted(dummy_table, key=itemgetter(2), reverse=True)
        dummy_table = dummy_table[0:4]

        result_table.append((insn, insn_word, dummy_table))

    # Print the result
    for result in result_table:
        # Print header
        logging.info(50 * '#')
        logging.info("%s %s", result[0], result[1])
        logging.info(50 * '#')

        # Print table
        for dummy in result[2]:
            logging.info("{:<20}{:<25}{:<5.2f}{:.2f}".format(dummy[0], dummy[1], dummy[2], dummy[3]))


if __name__ == '__main__':
    main()
