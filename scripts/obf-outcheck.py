#!/usr/bin/python3
import re
import argparse
import logging

from core import utils

START_OFFSET = 2
BLOCK_LENGTH = 10
BLOCK_OFFSET = 11


class ExBlock():

    raw_string = ""
    line_index = 0
    pc = ""
    status = []

    def from_file(self, file_path, line_index):
        self.line_index = line_index
        self.status = []
        for i in range(0, BLOCK_LENGTH):

            # line = linecache.getline(file_path, line_index + i)
            line = file_get_line(file_path, line_index + i)
            self.raw_string = self.raw_string + line

            if i == 0:
                result_array = re.findall(r"EXECUTED: (.*?):", line)
                self.pc = result_array[0]
            else:
                self.status.append(line)

        logging.debug(file_path)
        logging.debug(self.line_index)
        logging.debug(self.pc)
        # logging.debug(self.status)


def file_get_line(file_path, index):
    out_line = ""
    with open(file_path) as f:
        for i in range(0, index - 1):
            f.readline()
        out_line = f.readline()

    return out_line


def peek_line(f):
    pos = f.tell()
    line = f.readline()
    f.seek(pos)
    return line


def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description="Compare reference simulation output with obfuscated output")
    parser.add_argument("ref", type=str, help="reference file")
    parser.add_argument("sim", type=str, help="test file")
    parser.add_argument("-d", "--debug", action='store_true', help="enable debug output")
    args = parser.parse_args()

    # Logger
    utils.init_logger(debug=args.debug, log_to_file=False)

    # Read files
    ref_file_path = args.ref
    sim_file_path = args.sim

    ref_insn_index = 1
    sim_insn_index = 1

    ref_line_index = START_OFFSET
    sim_line_index = START_OFFSET

    ok = True
    while ok:

        logging.debug("Checking insn. %d", ref_insn_index)

        ref_block = ExBlock()
        ref_block.from_file(ref_file_path, ref_line_index)

        sub_length = 0

        sim_block = None
        pc_matches = True
        while pc_matches:
            temp_block = ExBlock()
            temp_block.from_file(sim_file_path, sim_line_index)

            if ref_block.pc == temp_block.pc:
                sim_block = temp_block

                sim_line_index += BLOCK_OFFSET
                sim_insn_index += 1

                sub_length += 1
            else:
                pc_matches = False

        if sim_block is None:
            sim_block = temp_block

        if ref_block.status != sim_block.status:
            # Block mismatch
            logging.error("Reference status:\n%s", ref_block.raw_string)
            logging.error("Test status:\n%s", sim_block.raw_string)
            ok = False
        else:
            # Block match
            logging.debug("Block %d is equivalent!", ref_insn_index)

        # Move to next reference instruction
        ref_line_index += BLOCK_OFFSET
        ref_insn_index += 1


if __name__ == '__main__':
    main()
