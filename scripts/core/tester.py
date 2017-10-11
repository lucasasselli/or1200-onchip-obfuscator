import os
import re
import subprocess
import logging
import shutil
import xlrd

from core import common
from core import decoder

# Constants
SIMULATOR = "icarus"
TARGET = "or1200-ref-generic"

# Paths
DIR_TEMPLATES = "templates"
DIR_TEST = "test"
DIR_SHELL = "shell"

PATH_WORK = "/tmp/obf-temp"

FILE_SIM_RESULT = "tb-general.log"

OPERAND_REXP = ["rA", "rB", "rD", "I|N|K", "L"]

# This is bad, I should feel bad. :-(
# TODO: Change it
OPERAND_SUBS = [
    ("r3", "r4", "r31", "8", "8"),
    ("r0", "r4", "r31", "8", "8"),
    ("r3", "r0", "r31", "8", "8"),
    ("r0", "r0", "r31", "8", "8"),
    ("r31", "r4", "r31", "8", "8"),
    ("r3", "r31", "r31", "8", "8"),
    ("r31", "r31", "r31", "8", "8")
]


class InsnSub:

    def __init__(self, ref, sub):
        self.insn_ref = ref
        self.insn_sub = sub
        self.test = Tester(self)

    def _get_sub_dword_array(self):
        sub_dword_array = []

        for insn in self.insn_sub.split():
            if "l." in insn:
                temp_dword = decoder.parse(insn)
                sub_dword_array.append(temp_dword)

        return sub_dword_array

    def __get_score(self, mode):
        try:
            ref_dword = decoder.parse(self.insn_ref)
            sub_dword_array = self._get_sub_dword_array()
        except ValueError:
            return -1

        scores = []

        for sub_dword in sub_dword_array:
            scores.append(common.dscore(ref_dword, sub_dword, mode))

        return sum(scores) / float(len(scores))

    def get_score_jaccd(self):
        return self.__get_score("jaccd")

    def get_score_smd(self):
        return self.__get_score("smd")

    def run_result_test(self):
        return self.test.run_result_test()

    def run_sr_test(self):
        return self.test.run_sr_test()


def load_sub_table(f, skip_header=True):

    insn_ref_array = []
    insn_sub_table = []

    wb = xlrd.open_workbook(f)
    sh = wb.sheet_by_index(0)

    for row_index in range(sh.nrows):

        # Skip header
        if skip_header and row_index == 0:
            continue

        row_values = sh.row_values(row_index)

        insn_ref_field = row_values[0]
        insn_ref_array.append(insn_ref_field)

        insn_sub_array = []

        for j in range(1, len(row_values)):

            insn_sub_field = row_values[j]

            # Skip empty rows
            if not insn_sub_field:
                break

            insn_sub = InsnSub(insn_ref_field, insn_sub_field)
            insn_sub_array.append(insn_sub)

        insn_sub_table.append(insn_sub_array)

    return insn_ref_array, insn_sub_table


class TestFile:

    def __init__(self, template_name, code, output_name, has_code=True):
        self.has_code = has_code
        self.template_name = template_name
        self.output_name = output_name
        self.code = code

    def write(self, operand_index):
        # Read in the file
        res_path = common.get_res_path()

        template_path = os.path.join(res_path, DIR_TEMPLATES, self.template_name)
        output_path = os.path.join(PATH_WORK, DIR_TEST, self.output_name)

        with open(template_path, 'r') as file:
            filedata = file.read()

        if self.has_code:
            # Swap placeholder operands with real ones
            code = self.code
            for rexp_index, rexp in enumerate(OPERAND_REXP):
                code = re.sub(rexp, OPERAND_SUBS[operand_index][rexp_index], code)

            # Replace the target string
            filedata = filedata.replace("//||//", code)

        # Write the file out again
        with open(output_path, 'w') as file:
            file.write(filedata)


class Tester:

    def __init__(self, sub_obj):
        self.result_array = []
        self.sub_obj = sub_obj

    def __run_command(self, command):
        result = 0
        output = ""
        try:
            subprocess.check_output(command, shell=True, universal_newlines=True, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as exc:
            output = exc.output
            result = exc.returncode
            logging.error("Error running command %s:\n%s", command, output)

        logging.debug("Command: %s\nOutput: %s", command, output)

        return result

    def __simulate(self, test_file_array, operand_index=0):

        res_path = common.get_res_path()
        root_path = common.get_root_path()

        # Clear work directory
        if os.path.exists(PATH_WORK):
            shutil.rmtree(PATH_WORK)
        os.mkdir(PATH_WORK)

        # Move test folder
        work_test_path = os.path.join(PATH_WORK, DIR_TEST)
        core_test_path = os.path.join(res_path, DIR_TEST)
        shutil.copytree(core_test_path, work_test_path)

        # Write test files
        for test_file in test_file_array:
            test_file.write(operand_index)

        # Compile test
        if self.__run_command("make all -C " + work_test_path) > 0:
            logging.error("Unable to compile test")
            return False

        # Run the actual simulation
        fusesoc_path = os.path.join(root_path, "fusesoc")
        elf_path = os.path.join(work_test_path, "test.elf")
        cmd_string = "cd " + PATH_WORK + "; fusesoc --cores-root=" + fusesoc_path + " sim --sim=" + SIMULATOR + " " + TARGET + " --elf-load=" + elf_path
        if self.__run_command(cmd_string) > 0:
            logging.error("Unable to run the simulation")
            return False

        # Read results
        result_local_path = "build/" + TARGET + "_0/sim-" + SIMULATOR + "/" + FILE_SIM_RESULT
        result_path = os.path.join(PATH_WORK, result_local_path)

        with open(result_path) as file:
            filedata = file.read()

        # Get result
        result_array = re.findall(r"\((.*?)\)", filedata)

        if(len(result_array) == 0):
            logging.error("Simulation output is empty")
            return False

        self.result_array = result_array

        return True

    # Checks if the substitution produces the same result of the reference
    def run_result_test(self):

        logging.debug("Running result test...")

        # If the instruction has no destiniation register, skip it
        if "rD" not in self.sub_obj.insn_sub:
            logging.info("(Result test) Substitution has no destination register: skipping...")
            return True

        # Generate main
        test_file_array = []
        test_file_array.append(TestFile("reg_result_main_c", None, "main.c", False))
        test_file_array.append(TestFile("reg_result_test_ref_asm", self.sub_obj.insn_ref, "test_ref.S"))
        test_file_array.append(TestFile("reg_result_test_sub_asm", self.sub_obj.insn_sub, "test_sub.S"))

        for opset_index in range(0, len(OPERAND_SUBS)):

            logging.debug("Testing operand set %d", opset_index)
            result = self.__simulate(test_file_array, opset_index)

            if result:
                # Parse exit code
                try:
                    sim_exit_code = int(self.result_array[-1], 16)
                except ValueError:
                    logging.error("(Result test) Unable to parse exit code")
                    return False

                if sim_exit_code != 1:
                    if len(self.result_array) < 5:
                        logging.error("(Result test) Bad output")
                        return False

                    # Parse simulation output
                    error_iteration = int(self.result_array[0], 16)
                    error_operand1 = self.result_array[1]
                    error_operand2 = self.result_array[2]
                    error_result_ref = self.result_array[3]
                    error_result_sub = self.result_array[4]

                    logging.error("(Result test) Mismatch at iteration %d of test %d:\nI=%s,%s\nR=%s\nS=%s",
                                  error_iteration, opset_index, error_operand1, error_operand2, error_result_ref, error_result_sub)

                    return False

                logging.debug("Test passed with operand set %d!", opset_index)
            else:
                # Simulation failed
                logging.error("(Result test) Unable to deploy test")
                return False

        return True

    def run_sr_test(self):

        logging.debug("Running SR test...")

        test_file_array = []
        test_file_array.append(TestFile("reg_sr_main_c", None, "main.c", False))
        test_file_array.append(TestFile("reg_sr_test_asm", self.sub_obj.insn_ref, "test.S"))

        result = self.__simulate(test_file_array)
        ref_result_array = self.result_array

        if not result:
            logging.error("(SR test) Unable to deploy reference test")
            return False

        test_file_array = []
        test_file_array.append(TestFile("reg_sr_main_c", None, "main.c", False))
        test_file_array.append(TestFile("reg_sr_test_asm", self.sub_obj.insn_sub, "test.S"))

        result = self.__simulate(test_file_array)
        sub_result_array = self.result_array

        logging.debug(ref_result_array)
        logging.debug(sub_result_array)

        if not result:
            logging.error("(SR test) Unable to deploy substitution test")
            return False

        if sub_result_array == ref_result_array:
            logging.debug("(SR test) Passed!")
            return True
        else:
            logging.error("(SR test) Mismatch")
            return False
