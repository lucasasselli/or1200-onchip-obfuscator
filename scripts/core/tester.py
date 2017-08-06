import re
import subprocess
import logging


# Result codes
RESULT_SKIP = -1
RESULT_SUCCESS = 0
RESULT_ERROR_UNKNOWN = 1
RESULT_ERROR_DEPLOY = 2
RESULT_ERROR_MISMATCH = 3

# Paths
PATH_TEMPLATES = "core/templates/"
PATH_TEST = "core/test/"
PATH_SHELL = "core/shell/"


def parse_result_code(code):

    if code == RESULT_SKIP:
        # Test skipped
        return "Skipped"

    if code == RESULT_SUCCESS:
        # Test passed
        return "OK"

    if code == RESULT_ERROR_DEPLOY:
        # Test failed: deploy error
        return "DEPLOY ERROR"

    if code == RESULT_ERROR_MISMATCH:
        # Test failed: result mismatch
        return "MISMATCH ERROR"


class Tester:

    operand_cues = ["rA", "rB", "rD", "I", "N", "K", "L"]
    operand_subs = ["r3", "r4", "r31", "8", "8", "8", "8"]

    def __init__(self, sub_obj):
        self.sub_obj = sub_obj

    # Generates build file from template file
    def __generate_from_template(self, infile, sub, outfile):
        # Read in the file
        with open(infile, 'r') as file:
            filedata = file.read()

        # Replace the target string
        filedata = filedata.replace("//||//", sub)

        # Write the file out again
        with open(outfile, 'w') as file:
            file.write(filedata)

    # Sets gold/sub operands
    def __set_operands(self, code, cues, subs):
        for i in range(0, len(cues)):
            code = code.replace(cues[i], subs[i])
        return code

    def __read_sim_result(self):
        with open(PATH_TEST+"simulation.log") as file:
            filedata = file.read()

        # Get result
        report_array = re.findall(r"\((.*?)\)", filedata)

        return report_array, filedata

    def __run_command(self, command):
        result = 0
        output = ""
        try:
            subprocess.check_output(command, shell=True, universal_newlines=True)
        except subprocess.CalledProcessError as exc:
            result = exc.returncode
            output = exc.output
        return result, output

    # Checks if the substitution produces the same result of the reference
    def run_result_test(self):

        # Clean test environment
        self.__run_command("./"+PATH_SHELL+"/test_clean.sh")

        # If the instruction has no destiniation register, skip it
        if "rD" not in self.sub_obj.insn_sub:
            logging.debug("(Result test) Substitution has no destination register: skipping...")
            return RESULT_SKIP

        # Generate main
        self.__run_command("cp "+PATH_TEMPLATES+"reg_result_main_c "+PATH_TEST+"/main.c")

        # Generate reference ASM
        fitted_ref = self.sub_obj.insn_ref
        fitted_ref = self.__set_operands(fitted_ref, self.operand_cues, self.operand_subs)
        self.__generate_from_template(PATH_TEMPLATES+"reg_result_test_ref_asm", fitted_ref, PATH_TEST+"/test_ref.S")

        # Generate subitution ASM
        fitted_sub = self.sub_obj.insn_sub
        fitted_sub = self.__set_operands(fitted_sub, self.operand_cues, self.operand_subs)
        self.__generate_from_template(PATH_TEMPLATES+"reg_result_test_sub_asm", fitted_sub, PATH_TEST+"test_sub.S")

        # Run simulation
        cmd_code, cmd_output = self.__run_command("./"+PATH_SHELL+"test_run.sh")
        if cmd_code > 0:
            # Deploy error
            logging.error("(Result test) Unable to deploy:\n%s", cmd_output)
            return RESULT_ERROR_DEPLOY

        # Check results
        sim_result_array, sim_output = self.__read_sim_result()

        if len(sim_result_array) == 0:
            logging.error("(Result test) Test returned an empty output")
            return RESULT_ERROR_UNKNOWN

        try:
            sim_exit_code = int(sim_result_array[-1], 16)
        except ValueError:
            logging.error("(Result test) Unable to parse exit code")
            return RESULT_ERROR_UNKNOWN

        if sim_exit_code != 1:
            print(sim_result_array)
            if len(sim_result_array) < 5:
                logging.error("(Result test) Bad output:\n%s", sim_output)
                return RESULT_ERROR_UNKNOWN

            # Parse simulation output
            error_iteration = int(sim_result_array[0], 16)
            error_operand1 = sim_result_array[1]
            error_operand2 = sim_result_array[2]
            error_result_ref = sim_result_array[3]
            error_result_sub = sim_result_array[4]

            logging.error("(Result test) Mismatch at iteration %d:\nI=%s,%s\nR=%s\nS=%s",
                          error_iteration, error_operand1, error_operand2, error_result_ref, error_result_sub)

            return RESULT_ERROR_MISMATCH

        return RESULT_SUCCESS

    def run_sr_test(self):

        # Clean test environment
        self.__run_command("./"+PATH_SHELL+"/test_clean.sh")

        # Generate main
        self.__run_command("cp "+PATH_TEMPLATES+"/reg_sr_main_c "+PATH_TEST+"/main.c")

        # Generate reference ASM
        fitted_ref = self.sub_obj.insn_ref
        fitted_ref = self.__set_operands(fitted_ref, self.operand_cues, self.operand_subs)
        self.__generate_from_template(PATH_TEMPLATES+"reg_sr_test_asm", fitted_ref, PATH_TEST+"test.S")

        # Run reference simulation
        cmd_code, cmd_output = self.__run_command("./"+PATH_SHELL+"/test_run.sh")
        if cmd_code > 0:
            # Deploy error
            logging.error("(SR test) Unable to deploy reference:\n%s", cmd_output)
            return RESULT_ERROR_DEPLOY

        # Check results
        sim_gold_sr_array, sim_gold_output = self.__read_sim_result()

        # Generate subitution ASM
        fitted_sub = self.sub_obj.insn_sub
        fitted_sub = self.__set_operands(fitted_sub, self.operand_cues, self.operand_subs)
        self.__generate_from_template(PATH_TEMPLATES+"reg_sr_test_asm", fitted_sub, PATH_TEST+"/test.S")

        # Run substitution simulation
        cmd_code, cmd_output = self.__run_command("./"+PATH_SHELL+"/test_run.sh")
        if cmd_code > 0:
            # Deploy error
            logging.error("(SR test) Unable to deploy substitution:\n%s", cmd_output)
            return RESULT_ERROR_DEPLOY

        # Check results
        sim_sub_sr_array, sim_sub_output = self.__read_sim_result()

        if sim_gold_sr_array == sim_sub_sr_array:
            return RESULT_SUCCESS
        else:
            error_out = "Reference:\n" + sim_gold_output + "\nSubstitution:\n" + sim_sub_output
            logging.error("(SR test) Mismatch:\n%s", error_out)
            return RESULT_ERROR_MISMATCH
