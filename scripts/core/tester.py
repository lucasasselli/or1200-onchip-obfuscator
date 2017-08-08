import os
import re
import subprocess
import logging
import shutil

from core import utils

# Constants
SIMULATOR = "icarus"
TARGET = "or1200-ref-generic"

# Paths
DIR_TEMPLATES = "templates"
DIR_TEST = "test"
DIR_SHELL = "shell"

PATH_WORK = "/tmp/obf-temp"

FILE_SIM_RESULT = "tb-general.log"

OPERAND_SUBS = [("rA", "r3"), ("rB", "r4"), ("rD", "r31"), ("I", "8"), ("N", "8"), ("K", "8"), ("L", "8")]


class TestFile:

    def __init__(self, template_name, code, output_name, has_code=True):
        self.has_code = has_code
        self.template_name = template_name
        self.output_name = output_name
        self.code = code

    def write(self):
        # Read in the file
        res_path = utils.get_res_path()

        template_path = os.path.join(res_path, DIR_TEMPLATES, self.template_name)
        output_path = os.path.join(PATH_WORK, DIR_TEST, self.output_name)

        with open(template_path, 'r') as file:
            filedata = file.read()

        if self.has_code:
            # Swap placeholder operands with real ones
            for i in range(0, len(OPERAND_SUBS)):
                self.code = self.code.replace(OPERAND_SUBS[i][0], OPERAND_SUBS[i][1])

            # Replace the target string
            filedata = filedata.replace("//||//", self.code)

        # Write the file out again
        with open(output_path, 'w') as file:
            file.write(filedata)


class Tester:

    result_array = []

    def __init__(self, sub_obj):
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

    def __simulate(self, test_file_array):

        res_path = utils.get_res_path()
        root_path = utils.get_root_path()

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
            test_file.write()

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

        # If the instruction has no destiniation register, skip it
        if "rD" not in self.sub_obj.insn_sub:
            logging.debug("(Result test) Substitution has no destination register: skipping...")
            return False

        # Generate main
        test_file_array = []
        test_file_array.append(TestFile("reg_result_main_c", None, "main.c", False))
        test_file_array.append(TestFile("reg_result_test_ref_asm", self.sub_obj.insn_ref, "test_ref.S"))
        test_file_array.append(TestFile("reg_result_test_sub_asm", self.sub_obj.insn_sub, "test_sub.S"))

        result = self.__simulate(test_file_array)

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

                logging.error("(Result test) Mismatch at iteration %d:\nI=%s,%s\nR=%s\nS=%s",
                              error_iteration, error_operand1, error_operand2, error_result_ref, error_result_sub)

                return False

            return True
        else:
            # Simulation failed
            logging.error("(Result test) Unable to deploy test")
            return False

    def run_sr_test(self):

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
        test_file_array.append(TestFile("reg_sr_test_asm", self.sub_obj.insn_ref, "test.S"))

        result = self.__simulate(test_file_array)
        sub_result_array = self.result_array

        if not result:
            logging.error("(SR test) Unable to deploy substitution test")
            return False

        if sub_result_array == ref_result_array:
            return True
        else:
            logging.error("(SR test) Mismatch")
            return False
