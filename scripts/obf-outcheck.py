#!/usr/bin/python3
import re
import argparse
import logging
import progressbar
import os.path

from core import utils

BLOCK_LENGTH = 9
STRIKE_LIMIT = 1
CONTEXT_SIZE = 50


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
                    exit(1)
                else:
                    self.pc = result_array[0]
            else:
                self.status.append(line)

        f.readline()


def peek_line(f):
    pos = f.tell()
    line = f.readline()
    f.seek(pos)
    return line


def checkEOF(f):
    pos = f.tell()
    line = f.readline()
    EOF = False
    if line == "":
        EOF = True
    f.seek(pos)
    return EOF


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
    parser.add_argument("-o", "--out", type=str, help="log file")
    parser.add_argument("-d", "--debug", action='store_true', help="enable debug output")
    args = parser.parse_args()

    # Logger
    utils.init_logger(args.out, debug=args.debug)

    # Read files
    ref_file_path = args.ref
    sim_file_path = args.sim

    if os.path.isfile(ref_file_path):
        ref_file = open(ref_file_path)
    else:
        logging.error("Unable to open reference file %s!", ref_file_path)
        exit(1)

    if os.path.isfile(sim_file_path):
        sim_file = open(sim_file_path)
    else:
        logging.error("Unable to open simulator file %s!", sim_file_path)
        exit(1)

    # Count lines
    logging.info("Counting blocks...")
    num_lines = sum(1 for line in ref_file)
    block_cnt = num_lines / 11
    logging.info("There are %d blocks to check", block_cnt)
    ref_file.seek(0)

    bar = progressbar.ProgressBar(maxval=block_cnt, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])

    # Useful metrics
    ref_block_index = 0

    ok = True
    ref_eof = False
    sim_eof = False

    ref_context = [None]*CONTEXT_SIZE
    sim_context = [None]*CONTEXT_SIZE

    # After STRIKE_LIMIT mismatching instructions stop execution
    strikes = 0

    logging.info("Checking blocks...")
    bar.start()

    while ok:
        skip_empty_lines(ref_file)
        ref_block_index += 1

        # Trim context
        ref_context.pop(0)
        sim_context.pop(0)

        if checkEOF(ref_file):
            ref_eof = True
            break

        ref_block = ExBlock()
        ref_block.from_file(ref_file)

        # Add to context
        ref_context.append(ref_block)

        logging.debug("Checking insn. %d", ref_block_index)
        logging.debug("Current PC: %s", ref_block.pc)

        # Get last block of the substitution
        sim_block = None
        is_last_sub = False
        pc_error = False
        sub_length = 0
        temp_sim_context = []
        while not is_last_sub:
            sub_length += 1
            skip_empty_lines(sim_file)
            temp_block = ExBlock()
            temp_block.from_file(sim_file)
            temp_sim_context.append(temp_block)
            sim_block = temp_block

            if sub_length == 1 and temp_block.pc != ref_block.pc:
                pc_error = True
                break

            # Get next PC
            if checkEOF(ref_file):
                sim_eof = True
                break

            next_sim_pc = peek_next_pc(sim_file)
            if next_sim_pc != ref_block.pc:
                is_last_sub = True
                logging.debug("Substitution length: %d", sub_length)

        sim_context.append(temp_sim_context)

        if ref_block.status != sim_block.status or pc_error:
            # Block mismatch
            strikes += 1
            logging.error("Strike %d", strikes)
            logging.error("Reference status:\n%s", ref_block.raw_string)
            logging.error("Test status:\n%s", sim_block.raw_string)
        else:
            # Block match
            logging.debug("Block %d is equivalent!", ref_block_index)
            strikes = 0

        bar.update(ref_block_index)

        if strikes >= STRIKE_LIMIT:
            ok = False

    bar.finish()

    if ok and ref_eof and not sim_eof:
        logging.error("Test didn't reach EOF!")
    elif not ok:
        logging.error("Test failed!")
        logging.info("Dumping reference context...")
        with open("ref_context.log", "w") as f:
            for block in ref_context:
                f.write(block.raw_string)
        logging.info("Dumping test context...")
        with open("test_context.log", "w") as f:
            for block_list in sim_context:
                for block in block_list:
                    f.write(block.raw_string)
    else:
        logging.info("Test passed!")


if __name__ == '__main__':
    main()
