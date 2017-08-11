import os
import xlrd
import logging
import logging.handlers

from core import common


def get_res_path():
    return os.path.join(os.path.dirname(__file__), common.DIR_RESOURCES)


def get_root_path():
    return os.path.join(os.path.dirname(__file__), common.DIR_ROOT)


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

            insn_sub = common.InsnSub(insn_ref_field, insn_sub_field)
            insn_sub_array.append(insn_sub)

        insn_sub_table.append(insn_sub_array)

    return insn_ref_array, insn_sub_table


def dscore(str1, str2, mode="jaccd"):
    if len(str1) != len(str2):
        raise ValueError

    f00 = 0
    f01 = 0
    f10 = 0
    f11 = 0

    for i in range(0, len(str1)):
        if str1[i] == "0" and str2[i] == "0":
            f00 += 1

        if str1[i] == "0" and str2[i] == "1":
            f01 += 1

        if str1[i] == "1" and str2[i] == "0":
            f10 += 1

        if str1[i] == "1" and str2[i] == "1":
            f11 += 1

    if(mode == "jaccd"):
        d = f01 + f10 + f11

        if d != 0:
            return (f01 + f10) / (f01 + f10 + f11)
        else:
            return 0
    elif(mode == "smd"):
        return (f01 + f10) / len(str1)
    else:
        raise ValueError


# Logger
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

# These are the sequences need to get colored output.
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"

COLOR_MAP = {
    'CRITICAL': RED,
    'ERROR': RED,
    'WARNING': YELLOW,
    'INFO': WHITE,
    'DEBUG': WHITE,
}


class LogFormatter(logging.Formatter):

    fmt_default = logging.Formatter('%(levelname)s: %(message)s')
    fmt_info = logging.Formatter('%(message)s')

    def __init__(self, monochrome):
        self.monochrome = monochrome

    def format(self, record):

        if record.levelno == logging.INFO:
            uncolored = self.fmt_info.format(record)
        else:
            uncolored = self.fmt_default.format(record)

        levelname = record.levelname

        if not self.monochrome and (levelname in COLOR_MAP):
            color_seq = COLOR_SEQ % (30 + COLOR_MAP[levelname])
            formatted = color_seq + uncolored + RESET_SEQ
        else:
            formatted = uncolored

        return formatted


def init_logger(log_file="", debug=False, log_to_file=True):
    logger = logging.getLogger()

    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    if log_to_file:
        file_handler = logging.FileHandler(log_file, mode="w")
        file_handler.setFormatter(LogFormatter(monochrome=1))
        logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(LogFormatter(monochrome=0))
    logger.addHandler(console_handler)
