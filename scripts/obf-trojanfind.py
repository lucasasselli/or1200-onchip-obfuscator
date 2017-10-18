#!/usr/bin/python3
import argparse
import logging
import progressbar
from core import common


class Trigger():

    def __init__(self, insn_array):
        self.insn_set = tuple(insn_array)
        self.count = 1
        self.match = 0
        self.dead = False

        self.id = hash(self.insn_set)

    def match_up(self):
        self.match += 1

    def count_up(self):
        self.count += 1

    def __len__(self):
        return len(self.insn_array)

    def kill(self):
        self.dead = True

    def __lt__(self, other):
        return self.id < other.id

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return " ".join(self.insn_set) + " (" + self.id + ")"

    def __hash__(self):
        return hash(self.insn_set)


class TriggerList():

    def __init__(self, length, max_count):
        self.trigger_array = dict({})
        self.length = length
        self.max_count = max_count

    def add(self, insn_array):
        # Search if trigger is present
        new_trigger = Trigger(insn_array)
        if new_trigger in self.trigger_array:
            t = self.trigger_array[new_trigger]
            t.count_up()
            if not t.dead and t.count > self.max_count:
                # Trigger has exceeded max count
                t.kill()
        else:
            self.trigger_array[new_trigger] = new_trigger

    def match(self, insn_array):
        # Search if trigger is present
        new_trigger = Trigger(insn_array)
        if new_trigger in self.trigger_array:
            t = self.trigger_array[new_trigger]
            if not t.dead:
                t.match_up()

    def purge_dead(self):
        cnt = 0
        inst = 0
        for i, t in enumerate(self.trigger_array):
            if t.dead:
                cnt += 1
                inst += t.count

        return cnt, inst

    def __len__(self):
        return len(self.trigger_array)

    def trigger_cnt(self):
        cnt = 0
        inst = 0
        for t in self.trigger_array:
            if not t.dead:
                cnt += 1
                inst += t.count
        return cnt, inst

    def match_cnt(self):
        cnt = 0
        inst = 0
        for t in self.trigger_array:
            if t.match > 0 and not t.dead:
                cnt += 1
                inst += t.match

        return cnt, inst

    def __str__(self):
        out = ""
        for t in self.trigger_array:
            out += str(t) + '\n'
        return out


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

    min_length = args.min_length
    max_length = args.max_length + 1

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

    # Create matchers/list
    expected_instances = 0
    matcher_array = []
    tlist_array = []
    for i in range(min_length, max_length):
        expected_instances += ref_insn_cnt - i - 1
        matcher_array.append(Matcher(i))
        tlist_array.append(TriggerList(i, args.count))

    logging.debug("Total expected instances: %d", expected_instances)

    # FIND TRIGGERS IN REFERENCE FILE
    print("Finding candidate triggers in reference file...")

    bar = progressbar.ProgressBar(maxval=ref_insn_cnt, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()

    insn_index = 0
    ref_file.seek(0)
    while 1:

        line = ref_file.readline()
        if line == "":
            # file reached EOF
            break

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

    # TODO remove!
    # Purge dead triggers
    dead_cnt = 0
    dead_inst = 0
    for tlist in tlist_array:
        cnt, inst = tlist.purge_dead()
        dead_cnt += cnt
        dead_inst += inst

    # Reset matchers
    for matcher in matcher_array:
        matcher.reset()

    # MATCH TRIGGERS IN OBFUSCATED FILE
    print("Matching triggers in obfuscated file...")

    bar = progressbar.ProgressBar(maxval=obf_insn_cnt, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()

    insn_index = 0
    obf_file.seek(0)
    while 1:

        line = obf_file.readline()
        if line == "":
            # file reached EOF
            break

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
        temp_cnt, temp_inst = tlist.trigger_cnt()
        candidate_cnt += temp_cnt
        candidate_inst += temp_inst
        temp_cnt, temp_inst = tlist.match_cnt()
        survivor_cnt += temp_cnt
        survivor_inst += temp_inst

    # Survival rate
    survival_rate = float(survivor_inst) / float(candidate_inst)

    # TODO debug only
    if not candidate_inst + survivor_inst != expected_instances:
        logging.error("Reference instances count error!")

    # Print stats
    # TODO print configuration for reference
    logging.info("Reference length: %d", ref_insn_cnt)
    logging.info("Obfuscated length: %d", obf_insn_cnt)
    logging.info("Instruction dilation: %f", or_ratio)
    logging.info("Candidate trigger: %d", candidate_cnt)
    logging.info("Candidate instances: %d", candidate_inst)
    logging.info("Dead triggers: %d", dead_cnt)
    logging.info("Dead instances: %d", dead_inst)
    logging.info("Survivor triggers: %d", survivor_cnt)
    logging.info("Survivor instances: %d", survivor_inst)
    logging.info("Survival rate: %f", survival_rate)

    # for tlist in tlist_array:
    #     print(tlist)


if __name__ == '__main__':
    main()
