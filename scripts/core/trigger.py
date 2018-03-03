import logging

SAFE = False


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
        return "(" + hex(self.id) + ") " + " ".join(self.insn_set) + " [" + str(self.count) + ":" + str(self.match) + "]"

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

            # Detect collisions
            if SAFE:
                if list(t.insn_set) != insn_array:
                    logging.error("Collision detected!")

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

            # Detect collisions
            if SAFE:
                if list(t.insn_set) != insn_array:
                    logging.error("Collision detected!")

            if not t.dead:
                t.match_up()

    def purge_dead(self):
        cnt = 0
        inst = 0
        for key in self.trigger_array.copy():
            if self.trigger_array[key].dead:
                cnt += 1
                inst += self.trigger_array[key].count
                del self.trigger_array[key]

        return cnt, inst

    def purge_unmatched(self):
        for key in self.trigger_array.copy():
            if self.trigger_array[key].match == 0:
                del self.trigger_array[key]

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
