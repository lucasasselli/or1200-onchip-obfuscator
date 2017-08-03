import decoder
import utils
import tester


class InsnSub:

    def __init__(self, ref, sub):
        self.insn_ref = ref
        self.insn_sub = sub
        self.test = tester.Tester(self)

    def _get_sub_dword_array(self):
        sub_dword_array = []

        for insn in self.insn_sub.split():
            if "l." in insn:
                temp_dword = decoder.parse(insn)
                sub_dword_array.append(temp_dword)

        return sub_dword_array

    def get_score_jaccd(self):
        try:
            ref_dword = decoder.parse(self.insn_ref)
            sub_dword_array = self._get_sub_dword_array()
        except ValueError:
            return -1

        scores = []

        for sub_dword in sub_dword_array:
            scores.append(utils.jaccd(ref_dword, sub_dword))

        return sum(scores) / float(len(scores))

    def get_score_smd(self):
        try:
            ref_dword = decoder.parse(self.insn_ref)
            sub_dword_array = self._get_sub_dword_array()
        except ValueError:
            return -1

        scores = []

        for sub_dword in sub_dword_array:
            scores.append(utils.smd(ref_dword, sub_dword))

        return sum(scores) / float(len(scores))

    def run_result_test(self):
        return self.test.run_result_test()

    def run_sr_test(self):
        return self.test.run_sr_test()
