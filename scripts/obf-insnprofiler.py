#!/usr/bin/python3
import argparse
import logging
import progressbar
import os.path

from core import common
from core.trigger import Matcher, TriggerList

TYPE_BRANCH = 0
TYPE_ARITHM = 1
TYPE_SYSTEM = 2
TYPE_FLAG = 3
TYPE_MEMORY = 4

BRANCH_LIST = ["l.j", "l.jal", "l.bnf", "l.bf", "l.jr", "l.jalr"]
SYSTEM_LIST = ["l.msync", "l.psync", "l.csync", "l.cust1", "l.cust2", "l.cust3", "l.cust4", "l.rfe",
               "l.cust5", "l.cust6", "l.cust7", "l.cust8", "l.mtspr", "l.mfspr", "l.sys", "l.trap", "l.nop"]
ARITH_LIST = ["l.addi", "l.addic", "l.andi", "l.ori", "l.xori", "l.muli", "l.slli", "l.srli", "l.srai", "l.rori",
              "l.exths", "l.extws", "l.extbs", "l.extwz", "l.exthz", "l.extbz", "l.add", "l.addc", "l.sub", "l.and",
              "l.or", "l.xor", "l.cmov", "l.ff1", "l.sll", "l.srl", "l.sra", "l.ror", "l.fl1", "l.mul", "l.muld",
              "l.div", "l.divu", "l.mulu", "l.muldu", "l.mac", "l.macu", "l.msb", "l.msbu", "l.movhi", "l.macrc", "l.maci"]
FLAG_LIST = ["l.sfeqi", "l.sfnei", "l.sfgtui", "l.sfgeui", "l.sfltui", "l.sfleui", "l.sfgtsi", "l.sfgesi", "l.sfltsi",
             "l.sflesi", "l.sfeq", "l.sfne", "l.sfgtu", "l.sfgeu", "l.sfltu", "l.sfleu", "l.sfgts", "l.sfges", "l.sflts", "l.sfles"]
MEMORY_LIST = ["l.lwz", "l.lws", "l.lbz", "l.lbs", "l.lhz", "l.lhs", "l.swa", "l.sd", "l.sw", "l.sb", "l.sh", "l.ld"]


def get_type(insn):
    if insn in BRANCH_LIST:
        return TYPE_BRANCH
    elif insn in ARITH_LIST:
        return TYPE_ARITHM
    elif insn in SYSTEM_LIST:
        return TYPE_SYSTEM
    elif insn in FLAG_LIST:
        return TYPE_FLAG
    elif insn in MEMORY_LIST:
        return TYPE_MEMORY
    else:
        logging.error("Unknown type for instruction %s!", insn)
        exit()


def get_insn(line):
    for word in line.split():
        if word.startswith("l."):
            return word


def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description="Perform a simple analysis of a program trace")
    parser.add_argument("input", type=str, help="input file")
    parser.add_argument("min_length", type=int, help="min trigger length")
    parser.add_argument("max_length", type=int, help="max trigger length")
    parser.add_argument("count", type=int, help="how many times the trigger can appear")
    parser.add_argument("-o", "--out", type=str, help="log file")
    parser.add_argument("-d", "--debug", action='store_true', help="enable debug output")
    args = parser.parse_args()

    min_length = args.min_length
    max_length = args.max_length + 1

    # Logger
    common.init_logger(args.out, debug=args.debug)

    # Read files
    input_file_path = args.input

    if os.path.isfile(input_file_path):
        input_file = open(input_file_path)
    else:
        logging.error("Unable to open file %s!", input_file_path)
        exit(1)

    # Count lines
    logging.info("Counting instructions...")
    insn_cnt = sum(1 for line in input_file)
    logging.info("There are %d instructions to check", insn_cnt)
    input_file.seek(0)

    bar = progressbar.ProgressBar(maxval=insn_cnt, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])

    # Useful metrics
    insn_index = 0
    type_cnt = [0, 0, 0, 0, 0]

    # Create matchers/list
    matcher_array = []
    tlist_array = []
    for i in range(min_length, max_length):
        matcher_array.append(Matcher(i))
        tlist_array.append(TriggerList(i, args.count))

    logging.info("Analyzing...")
    bar.start()

    insn_dict = {}

    for line in input_file:

        insn = get_insn(line)

        type_cnt[get_type(insn)] += 1

        # Add line to matcher
        for matcher in matcher_array:
            matcher.add(insn)

        # Add or increase trigger instances
        for i, matcher in enumerate(matcher_array):
            # Check if matcher has been successfully initialized
            if(matcher.valid()):
                # Add candidate to relative trigger list
                tlist_array[i].add(matcher.insn_array)

        # Check if entry exists
        if insn in insn_dict:
            insn_dict[insn] += 1
        else:
            insn_dict[insn] = 1

        bar.update(insn_index)
        insn_index += 1

    bar.finish()

    # Print candidates info
    logging.info("Candidates info:")
    for tlist in tlist_array:
        logging.info("%d\t%d", tlist.length, len(tlist))

    # Print insn info
    logging.info("Insn type info:")
    for i, t in enumerate(type_cnt):
        logging.info("%d\t%f", i, (t/insn_cnt)*100)

    # checksum = 0
    # for insn in sorted(insn_dict):
    #     logging.info("{:<10} {:}".format(insn, insn_dict[insn]))
    #     # logging.info("%d", insn_dict[insn])
    #     checksum += insn_dict[insn]

    # if not checksum == insn_cnt:
    #     logging.error("Insn count doesn't match data!")


if __name__ == '__main__':
    main()
