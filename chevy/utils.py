import numpy as np


def count_bits(n):
    count = 0
    while n:
        count += n & 1
        n >>= 1
    return count


def mirror_uci(uci):
    lst = list(uci)
    lst[1] = str(9 - int(lst[1]))
    lst[3] = str(9 - int(lst[3]))
    return "".join(lst)


def relative_cp_to_win_proba(cp):
    return 1. / (1. + np.power(np.float128(10.),
                               (np.float128(-0.25) * np.float128(cp / 100.))))
