import os


class Logger():

    log_name = ""
    indent = 0

    def __init__(self, log_name):
        self.log_name = log_name
        try:
            os.remove(log_name)
        except OSError:
            pass

    def __indent(self, string, amount):
        s = ""
        for i in range(0, amount):
            s += "\t"
        return s + string.replace("\n", "\n"+s)

    def set_indent(self, x):
        self.indent = x

    def print(self, *args):
        s = "".join(str(i) for i in args)
        s = self.__indent(s, self.indent)
        print(s, end="")
        with open(self.log_name, "a") as log_file:
            log_file.write(s)

    def println(self, *args):
        s = "".join(str(i) for i in args)
        s = self.__indent(s, self.indent)
        print(s)
        with open(self.log_name, "a") as log_file:
            log_file.write(s+'\n')
