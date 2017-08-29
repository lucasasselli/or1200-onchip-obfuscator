#!/usr/bin/python3
import argparse
import logging

from core import utils

# Constants
EXEC_MODE_SINGLE = 0
EXEC_MODE_ALL = 1


def test(i, insn_ref_array, insn_sub_table, score_only):
    insn_ref = insn_ref_array[i]

    if len(insn_sub_table[i]) == 0:
        return

    # Print header
    logging.info("#" * 50)
    logging.info("Instruction  %d [%s]", i + 1, insn_ref)
    logging.info("#" * 50)

    index_sub = 1

    for insn_sub in insn_sub_table[i]:

        logging.info("\nSubstitution %d:", index_sub)

        # Run tests
        if not score_only:
            test_result = insn_sub.run_result_test()
            test_sr = insn_sub.run_sr_test()

        score_jaccd = insn_sub.get_score_jaccd()
        score_smd = insn_sub.get_score_smd()

        # Log result
        if not score_only:
            if test_result and test_sr:
                test_status = "TEST PASSED!"
            else:
                test_status = "TEST FAILED!"

            logging.info("%s Score: %.2f %.2f", test_status, score_jaccd, score_smd)
        else:
            logging.info("Score: %.2f %.2f", score_jaccd, score_smd)

        index_sub += 1

    logging.info("")

    return


def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description="Test Open RISC 1000 instruction set substitutions")
    parser.add_argument("file", type=str, help="input file")
    parser.add_argument("-i", type=int, default=-1, help="instruction to test")
    parser.add_argument("-o", "--out", type=str, default="subtest.log", help="log file")
    parser.add_argument("-s", "--score-only", action='store_true', help="compute only substitution scores")
    parser.add_argument("-d", "--debug", action='store_true', help="enable debug output")
    args = parser.parse_args()

    score_only = args.s

    # Logger
    utils.init_logger(args.out, debug=args.debug)

    # Read table
    insn_ref_array, insn_sub_table = utils.load_sub_table(args.file)

    # Execution mode
    if(args.i >= 0):
        exec_mode = EXEC_MODE_SINGLE
        insn_index = args.i

        if insn_index >= len(insn_ref_array):
            logging.error("Invalid instruction index")
            exit()
    else:
        exec_mode = EXEC_MODE_ALL

    # Run test
    if exec_mode == EXEC_MODE_SINGLE:
        # Selected insnuction
        test(insn_index, insn_ref_array, insn_sub_table, score_only)

    if exec_mode == EXEC_MODE_ALL:
        # All insnuctions
        for i in range(0, len(insn_ref_array)):
            test(i, insn_ref_array, insn_sub_table, score_only)


if __name__ == '__main__':
    main()
