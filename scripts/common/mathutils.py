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
