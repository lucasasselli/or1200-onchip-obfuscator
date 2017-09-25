#!/usr/bin/python3
import re
import argparse
import logging

from core import utils

BLOCK_LENGTH = 9
STRIKE_LIMIT = 3


class ExBlock():

    raw_string = ""
    pc = ""
    header = ""
    status = []

    def from_file(self, f):
        # Clear vars
        self.raw_string = ""
        self.header = ""
        self.status = []

        # Read block
        for i in range(0, BLOCK_LENGTH):
            line = f.readline()

            self.raw_string = self.raw_string + line

            if i == 0:
                self.header = line
                result_array = re.findall(r"EXECUTED: (.*?):", line)
                if len(result_array) == 0:
                    logging.error("File alignment broken!")
                    exit()
                else:
                    self.pc = result_array[0]
            else:
                self.status.append(line)

        f.readline()


def peek_line(f):
    pos = f.tell()
    line = f.readline()
    if line == "":
        logging.info("EOF!")
        logging.debug(f)
    f.seek(pos)
    return line


def skip_empty_lines(f):
    while peek_line(f) is "\n":
        f.readline()


def peek_next_pc(f):
    pos = f.tell()
    pc_not_found = True
    pc = ""
    while pc_not_found:
        line = f.readline()
        if "EXECUTED" in line:
            pc_not_found = False
            result_array = re.findall(r"EXECUTED: (.*?):", line)
            pc = result_array[0]
    f.seek(pos)
    return pc


def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description="Compare reference simulation output with obfuscated output")
    parser.add_argument("ref", type=str, help="reference file")
    parser.add_argument("sim", type=str, help="test file")
    parser.add_argument("-o", "--out", type=str, default="outcheck.log", help="log file")
    parser.add_argument("-d", "--debug", action='store_true', help="enable debug output")
    parser.add_argument("-p", "--parse", action='store_true', help="parse execution")
    args = parser.parse_args()

    parse = args.parse

    # Logger
    utils.init_logger(args.out, debug=args.debug)

    # Read files
    ref_file_path = args.ref
    sim_file_path = args.sim
    ref_file = open(ref_file_path)
    sim_file = open(sim_file_path)

    # Count lines
    logging.info("Counting blocks...")
    num_lines = sum(1 for line in ref_file)
    block_cnt = num_lines / 11
    logging.info("There are %d blocks to check", block_cnt)
    ref_file.seek(0)

    # Useful metrics
    ref_block_index = 0
    last_progress = 0

    ok = True

    # After STRIKE_LIMIT mismatching instructions stop execution
    strikes = 0

    logging.info("Checking blocks...")

    while ok:
        skip_empty_lines(ref_file)
        ref_block_index += 1

        ref_block = ExBlock()
        ref_block.from_file(ref_file)

        logging.debug("Checking insn. %d", ref_block_index)
        logging.debug("Current PC: %s", ref_block.pc)

        if parse:
            logging.info(ref_block.header)

        # Get last block of the substitution
        sim_block = ExBlock()
        is_last_sub = False
        sub_length = 0
        while not is_last_sub:
            sub_length += 1
            skip_empty_lines(sim_file)
            sim_block.from_file(sim_file)

            if parse:
                logging.info("\t%s", sim_block.header)

            # Get next PC
            next_sim_pc = peek_next_pc(sim_file)
            if next_sim_pc != ref_block.pc:
                is_last_sub = True
                logging.debug("Substitution length: %d", sub_length)

        if not parse:
            if ref_block.status != sim_block.status:
                # Block mismatch
                strikes += 1
                logging.error("Strike %d", strikes)
                logging.error("Reference status:\n%s", ref_block.raw_string)
                logging.error("Test status:\n%s", sim_block.raw_string)
            else:
                # Block match
                logging.debug("Block %d is equivalent!", ref_block_index)
                strikes = 0

            if strikes > STRIKE_LIMIT:
                ok = False

        progress = int((ref_block_index / block_cnt) * 100.0)
        if (progress > last_progress):
            last_progress = progress
            print(progress, "%")


if __name__ == '__main__':
    main()
