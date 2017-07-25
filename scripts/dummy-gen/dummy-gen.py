#!/usr/bin/python3
import argparse
import pandas
from tabulate import tabulate
from common import mylogger
from common import decoder
from common import mathutils


# Parse arguments
parser = argparse.ArgumentParser(description="Compute Open RISC 1000 optimal dummy instruction set substitution.")
parser.add_argument("-o", "--out", type=str, default="dummy-gen.log", help="log file")
parser.add_argument("-d", "--debug", action='store_true', help="enable debug output")

args = parser.parse_args()

# Logger
logger = mylogger.Logger(args.out)

# Read instruction list
instr_list = []
instr_file_name = "instr_list"

with open(instr_file_name, 'r') as f:
    for line in f:
        instr_list.append(line.rstrip())


# Read dummy list
dummy_list = []
dummy_file_name = "dummy_list"

table = []
with open(dummy_file_name, 'r') as f:
    for line in f:
        dummy_list.append(line.rstrip())

result_table = {
    'instr': [],
    'dummy': [],
    'instr_word': [],
    'dummy_word': [],
    'smd': [],
    'jaccd': []}


for instr in instr_list:
    # find dummy instr with max smd
    instr_word = decoder.parse(instr)
    if not instr_word:
        continue

    best_dummy = ""
    best_word = ""
    best_score = 0

    for dummy in dummy_list:
        dummy_word = decoder.parse(dummy)
        if not dummy_word:
            continue

        this_score = mathutils.smd(instr_word, dummy_word)

        if this_score > best_score:
            best_score = this_score
            best_dummy = dummy
            best_word = dummy_word

    # Print result
    result_table['instr'].append(instr)
    result_table['dummy'].append(best_dummy)
    result_table['instr_word'].append(instr_word)
    result_table['dummy_word'].append(best_word)
    result_table['smd'].append(best_score)
    result_table['jaccd'].append(mathutils.jaccd(best_word, instr_word))

    table.append([instr, best_dummy, best_score, mathutils.jaccd(best_word, instr_word)])

df = pandas.DataFrame(result_table)
logger.print(tabulate(df, showindex=False, headers=df.columns, cols=["instr","dummy","instr_word", "dummy_word", "smd", "jaccd"]))
