import re
import subprocess


class Tester:

    # Result codes
    RESULT_SKIP = -1
    RESULT_SUCCESS = 0
    RESULT_ERROR_DEPLOY = 1
    RESULT_ERROR_MISMATCH = 2

    operand_cues = ["rA", "rB", "rD", "I", "N", "K", "L"]
    operand_subs = ["r3", "r4", "r31", "8", "8", "8", "8"]

    def __init__(self, gold, sub):
        self.gold = gold
        self.sub = sub

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
    def __set_operands(self, gold, cues, subs):
        for i in range(0, len(cues)):
            gold = gold.replace(cues[i], subs[i])
        return gold

    def __read_sim_result(self):
        with open('../../sim/run/general.log') as file:
            filedata = file.read()

        # Get result
        report_array = re.findall(r"\(([0-9_]+)\)", filedata)

        return report_array, filedata

    def __run_command(self, command):
        result = 0
        output = ""
        try:
            subprocess.check_output(
                command, shell=True, universal_newlines=True)
        except subprocess.CalledProcessError as exc:
            result = exc.returncode
            output = exc.output
        return result, output

    def run_register_test(self):

        # Clean build
        # TODO

        # If the instruction has no destiniation register, skip it
        if "rD" not in self.gold:
            return self.RESULT_SKIP, ""

        # Generate main
        self.__run_command("cp templates/reg_result_main_c test/main.c")

        # Generate gold ASM
        fitted_gold = self.gold
        fitted_gold = self.__set_operands(
            fitted_gold, self.operand_cues, self.operand_subs)
        self.__generate_from_template(
            "templates/reg_result_test_gold_asm", fitted_gold, "test/test_gold.S")

        # Generate subitution ASM
        fitted_sub = self.sub
        fitted_sub = self.__set_operands(
            fitted_sub, self.operand_cues, self.operand_subs)
        self.__generate_from_template(
            "templates/reg_result_test_sub_asm", fitted_sub, "test/test_sub.S")

        # Compile and deploy test
        cmd_code, cmd_output = self.__run_command("./deploy_test.sh")
        if cmd_code > 0:
            # Deploy error
            return self.RESULT_ERROR_DEPLOY, cmd_output

        # Run simulation
        self.__run_command("../../sim_nogui.sh")

        # Check results
        sim_result_array, sim_output = self.__read_sim_result()
        if int(sim_result_array[-1]) != 1:
            return self.RESULT_ERROR_MISMATCH, sim_output

        return self.RESULT_SUCCESS, ""

    def run_sr_test(self):

        # Clean build
        # TODO

        # Generate main
        self.__run_command("cp templates/reg_sr_main_c test/main.c")

        # Generate gold ASM
        fitted_gold = self.gold
        fitted_gold = self.__set_operands(
            fitted_gold, self.operand_cues, self.operand_subs)
        self.__generate_from_template(
            "templates/reg_sr_test_asm", fitted_gold, "test/test.S")

        # Compile and deploy test
        cmd_code, cmd_output = self.__run_command("./deploy_test.sh")
        if cmd_code > 0:
            # Deploy error
            return self.RESULT_ERROR_DEPLOY, cmd_output

        # Run simulation
        self.__run_command("../../sim_nogui.sh")

        # Check results
        sim_gold_sr_array, sim_gold_output = self.__read_sim_result()

        # Generate subitution ASM
        fitted_sub = self.sub
        fitted_sub = self.__set_operands(
            fitted_sub, self.operand_cues, self.operand_subs)
        self.__generate_from_template(
            "templates/reg_sr_test_asm", fitted_sub, "test/test.S")

        # Compile and deploy test
        cmd_code, cmd_output = self.__run_command("./deploy_test.sh")
        if cmd_code > 0:
            # Deploy error
            return self.RESULT_ERROR_DEPLOY, cmd_output

        # Run simulation
        self.__run_command("../../sim_nogui.sh")

        # Check results
        sim_sub_sr_array, sim_sub_output = self.__read_sim_result()

        if sim_gold_sr_array == sim_sub_sr_array:
            return self.RESULT_SUCCESS, ""
        else:
            error_out = "GOLDEN:\n" + sim_gold_output + \
                "\n\nSUBSTITUTION:\n" + sim_sub_output
            return self.RESULT_ERROR_MISMATCH, error_out
