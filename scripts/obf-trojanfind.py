#!/usr/bin/python3
import argparse
import logging
import progressbar

from core import common
from core import decoder


class Trigger():

    def __init__(self, insn_array):
        self.insn_array = list(insn_array)
        self.count = 1
        self.match = 0
        self.dead = False

    def match_up(self):
        self.match += 1

    def count_up(self):
        self.count += 1

    def size(self):
        return len(self.insn_array)

    def kill(self):
        self.dead = True

    def get_id(self):
        trigger_id = ""
        for insn in self.insn_array:
            try:
                index = decoder.get_index(insn)
            except ValueError:
                logging.error("Unable to get index of instruction %s", insn)
                exit(1)
            trigger_id += str(index)
        return trigger_id


class TriggerList():

    def __init__(self, length, max_count):
        self.trigger_array = []
        self.length = length
        self.max_count = max_count

    def add(self, insn_array):
        # Trigger must be added to the rigth list
        if len(insn_array) != self.length:
            logging.error("Trigger was added to wrong list!!!")
            exit()

        # Search if trigger is present
        found = False
        for t in self.trigger_array:
            if t.insn_array == insn_array:
                # Match found
                found = True
                # Ignore dead triggers
                if not t.dead:
                    t.count_up()
                    if t.count > self.max_count:
                        # Trigger has exceeded max count
                        t.kill()
                        logging.debug("Trigger %s has exceeded maximum count in %d", t.get_id(), self.length)
                # End loop
                break

        if not found:
            # New trigger
            trigger = Trigger(insn_array)
            self.trigger_array.append(trigger)
            logging.debug("New trigger %s added to list %d", trigger.get_id(), self.length)

    def match(self, insn_array):
        # Trigger must be added to the rigth list
        if len(insn_array) != self.length:
            logging.error("Trigger was matched to wrong list!!!")
            exit()

        # Search if trigger is present
        for t in self.trigger_array:
            if t.insn_array == insn_array:
                # Match found
                if not t.dead:
                    t.match_up()
                # End loop
                break

    def purge_dead(self):
        for i, t in enumerate(self.trigger_array):
            if t.dead:
                self.trigger_array.pop(i)


class Matcher():
    length = 0
    insn_array = []
    init_cnt = 0

    def __init__(self, length):
        self.length = length
        self.reset()

    def add(self, insn):
        self.insn_array.pop(0)
        self.insn_array.append(insn)
        if self.init_cnt > 0:
            self.init_cnt -= 1

    def valid(self):
        return self.init_cnt == 0

    def reset(self):
        self.insn_array = self.length * [None]
        self.init_cnt = self.length


def checkEOF(f):
    pos = f.tell()
    line = f.readline()
    EOF = False
    if line == "":
        EOF = True
    f.seek(pos)
    return EOF


def get_insn(line):
    for word in line.split():
        if word.startswith("l."):
            return word


def main():

    # Parse arguments
    parser = argparse.ArgumentParser(description="Compare reference simulation output with obfuscated output to spot trojan triggers")
    parser.add_argument("ref", type=str, help="reference file")
    parser.add_argument("obf", type=str, help="obfuscated file")
    parser.add_argument("min_length", type=int, help="min trigger length")
    parser.add_argument("max_length", type=int, help="max trigger length")
    parser.add_argument("count", type=int, help="how many times the trigger can appear")
    parser.add_argument("-o", "--out", type=str, help="log file")
    parser.add_argument("-d", "--debug", action='store_true', help="enable debug output")
    args = parser.parse_args()

    # Logger
    common.init_logger(args.out, debug=args.debug)

    # Create matchers/list
    matcher_array = []
    tlist_array = []
    for i in range(args.min_length, args.max_length):
        matcher_array.append(Matcher(i))
        tlist_array.append(TriggerList(i, args.count))

    # Read files
    ref_file_path = args.ref
    obf_file_path = args.obf

    try:
        ref_file = open(ref_file_path, "r")
    except IOError:
        logging.error("Unable to open reference file %s!", ref_file_path)
        exit(1)

    try:
        obf_file = open(obf_file_path, "r")
    except IOError:
        logging.error("Unable to open obfuscator file %s!", obf_file_path)
        exit(1)

    # Count instructions
    print("Counting reference file instructions...")
    ref_insn_cnt = sum(1 for line in ref_file)
    print(ref_insn_cnt, "reference instructions to check")
    ref_file.seek(0)
    print("Counting obfuscated file instructions...")
    obf_insn_cnt = sum(1 for line in obf_file)
    print(obf_insn_cnt, "obfuscated instructions to check")
    obf_file.seek(0)

    # FIND TRIGGERS IN REFERENCE FILE
    print("Finding candidate triggers in reference file...")

    bar = progressbar.ProgressBar(maxval=ref_insn_cnt, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()

    insn_index = 0
    while not checkEOF(ref_file):

        line = ref_file.readline()

        # Get instruction
        insn = get_insn(line)

        # Add line to matcher
        for matcher in matcher_array:
            matcher.add(insn)

        # Add or increase trigger instances
        for i, matcher in enumerate(matcher_array):
            # Check if matcher has been successfully initialized
            if(matcher.valid()):
                # Add candidate to relative trigger list
                tlist_array[i].add(matcher.insn_array)

        insn_index += 1
        bar.update(insn_index)

    bar.finish()

    # Purge dead triggers
    for tlist in tlist_array:
        tlist.purge_dead()

    # Reset matchers
    for matcher in matcher_array:
        matcher.reset()

    # MATCH TRIGGERS IN OBFUSCATED FILE
    print("Matching triggers in obfuscated file...")

    bar = progressbar.ProgressBar(maxval=obf_insn_cnt, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()

    insn_index = 0
    while not checkEOF(obf_file):

        line = obf_file.readline()

        # Get instruction
        insn = get_insn(line)

        # Add line to matcher
        for matcher in matcher_array:
            matcher.add(insn)

        # Add or increase trigger instances
        for i, matcher in enumerate(matcher_array):
            # Check if matcher has been successfully initialized
            if(matcher.valid()):
                # Add candidate to relative trigger list
                tlist_array[i].match(matcher.insn_array)

        insn_index += 1
        bar.update(insn_index)

    bar.finish()

    # Obfuscated-reference length ratio
    or_ratio = float(obf_insn_cnt) / float(ref_insn_cnt)

    # Triggers found/survived
    candidate_cnt = 0
    candidate_inst = 0
    survivor_cnt = 0
    survivor_inst = 0
    for tlist in tlist_array:
        for trigger in tlist.trigger_array:
            candidate_cnt += 1
            candidate_inst += trigger.count
            survivor_inst += trigger.match
            if not trigger.match == 0:
                survivor_cnt += 1

    # Survival rate
    survival_rate = float(survivor_inst)/float(candidate_inst)

    # Print stats
    # TODO print configuration for reference
    logging.info("Reference length: %d", ref_insn_cnt)
    logging.info("Obfuscated length: %d", obf_insn_cnt)
    logging.info("Instruction dilation: %f", or_ratio)
    logging.info("Candidate trigger: %d", candidate_cnt)
    logging.info("Candidate instances: %d", candidate_inst)
    logging.info("Survivor triggers: %d", survivor_cnt)
    logging.info("Survivor instances: %d", survivor_inst)
    logging.info("Survival rate: %f", survival_rate)

    ## Print survivors
    # for tlist in tlist_array:
    #     for trigger in tlist.trigger_array:
    #         if trigger.match > 0:
    #             print(trigger.insn_array)


if __name__ == '__main__':
    main()
