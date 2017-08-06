import csvkit
from core import common
import logging
import logging.handlers


def load_csv(f, skip_header):

    insn_ref_array = []
    insn_sub_table = []

    try:
        reader = csvkit.reader(f)
        i = 0
        for row in reader:

            # Skip header if required
            if skip_header == 1 and i == 0:
                i += 1
                continue

            insn_ref_field = row[0]
            insn_ref_array.append(insn_ref_field)

            insn_sub_array = []

            for j in range(1, len(row)):

                insn_sub_field = row[j]

                # Skip empty rows
                if not insn_sub_field:
                    break

                insn_sub = common.InsnSub(insn_ref_field, insn_sub_field)

                insn_sub_array.append(insn_sub)

            insn_sub_table.append(insn_sub_array)
            i += 1

    finally:
        f.close()

    return insn_ref_array, insn_sub_table


def jaccd(str1, str2):
    if len(str1) != len(str2):
        raise ValueError

    f01 = 0
    f10 = 0
    f11 = 0

    for i in range(0, len(str1)):
        if str1[i] == "0" and str2[i] == "1":
            f01 += 1

        if str1[i] == "1" and str2[i] == "0":
            f10 += 1

        if str1[i] == "1" and str2[i] == "1":
            f11 += 1

    d = f01 + f10 + f11

    if d != 0:
        return 1 - (f11 / d)
    else:
        return 0

    return


def smd(str1, str2):
    if len(str1) != len(str2):
        raise ValueError

    D = 0
    U = len(str1)

    for i in range(0, len(str1)):
        if str1[i] != str2[i]:
            D += 1

    return D / U


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
