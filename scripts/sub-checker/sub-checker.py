#!/usr/bin/python3
import csv
from common import mylogger
import tester
import argparse


def parse_result(code, output):
    # Check result
    if code == -1:
        # Test skipped
        logger.println(0, "skip")

    if code == 0:
        # Test passed
        logger.println(0, "OK!")

    if code == 1:
        # Test failed: deploy error
        logger.println(0, "DEPLOY ERROR!")
        logger.println(2, output)

    if code == 2:
        # Test failed: result mismatch
        logger.println(0, "MISMATCH ERROR!")
        logger.println(2, output)


# Parse arguments
parser = argparse.ArgumentParser(description="Test Open RISC 1000 instruction set substitution.")
parser.add_argument("file", type=str, help="input file")
parser.add_argument("-i", type=int, default=0, help="intruction to test")
parser.add_argument("-o", "--out", type=str, default="test.log", help="log file")
args = parser.parse_args()

f = open(args.file, 'rt')

logger = mylogger.Logger("test.log")
logger.println(0, "Starting test...")

index_gold = 0
test_count = 0
test_ok = 0

try:
    reader = csv.reader(f)
    for row in reader:
        if index_gold != 0 and int(row[1]) == 1:

            # Skip marked instructions
            if row[1] == 0 or (args.i != 0 and args.i != index_gold - 1):
                index_gold += 1
                continue

            instr_gold = row[0]
            logger.println(
                0, "\n##################################################")
            logger.println(0, "Selected instruction ",
                           index_gold, " ", instr_gold)
            logger.println(
                0, "##################################################\n")

            # Test substitutions
            index_sub = 0
            for i in range(2, len(row)):

                # Skip empty substitutions
                instr_sub = row[i]
                if not instr_sub:
                    break

                success = 1

                test = tester.Tester(instr_gold, instr_sub)

                logger.println(0, "Substitution ", index_sub, ":")

                # Run result test
                logger.print(1, "--> RESULT: ")
                test_code, test_output = test.run_register_test()
                parse_result(test_code, test_output)
                if test_code > 0:
                    success = 0

                # Run sr test
                logger.print(1, "--> SR    : ")
                test_code, test_output = test.run_sr_test()
                parse_result(test_code, test_output)
                if test_code > 0:
                    success = 0

                if success == 1:
                    test_ok += 1

                test_count += 1
                index_sub += 1

        # If argument I is set stop here
        if args.i != 0 and args.i == index_gold - 1:
            break

        index_gold += 1
finally:
    f.close()

logger.println(0, "\n\nTest completed:")
logger.println(0, "TESTED: ", test_count)
logger.println(0, "FAILED: ", test_count - test_ok)
