from . import *


def xor(t1, t2):
    return [x ^ y for x, y in zip(t1, t2)]


def shift(g, d, n):
    return g[n:] + g[:n], d[n:] + d[:n]


def permute(block, table):
    return [block[x - 1] for x in table]


def expand(block, table):
    return [block[x - 1] for x in table]


def substitute(d_e):
    sub_blocks = n_split(d_e, 6)
    result = list()
    for i in range(len(sub_blocks)):
        block = sub_blocks[i]
        row = int(str(block[0]) + str(block[5]), 2)
        column = int(''.join([str(x) for x in block[1:][:-1]]), 2)
        val = S_BOX[i][row][column]
        bi = bin_value(val, 4)
        result += [int(x) for x in bi]
    return result


def remove_padding(data):
    pad_len = ord(data[-1])
    return data[:-pad_len]


def add_padding(text):
    pad_len = 8 - (len(text) % 8)
    text += pad_len * chr(pad_len)
    return text
