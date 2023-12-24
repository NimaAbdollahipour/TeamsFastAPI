from . import *


class DES:
    def __init__(self, key=None):
        if len(key) < 8:
            raise "Key Should be 8 bytes long"
        elif len(key) > 8:
            key = key[:8]
        self.password = key
        self.keys = list()
        self.generate_keys()

    def __run(self, text, action=0):
        if not action:
            text = add_padding(text)
        text_blocks = n_split(text, 8)
        result = list()
        for block in text_blocks:
            block = string_to_bit_array(block)
            block = permute(block, PI)
            g, d = n_split(block, 32)
            tmp = None
            for i in range(16):
                d_e = expand(d, E)
                if action == 0:
                    tmp = xor(self.keys[i], d_e)
                else:
                    tmp = xor(self.keys[15 - i], d_e)
                tmp = substitute(tmp)
                tmp = permute(tmp, P)
                tmp = xor(g, tmp)
                g = d
                d = tmp
            result += permute(d + g, PI_1)
        final_res = bit_array_to_string(result)
        if action == 1:
            return remove_padding(final_res)
        else:
            return final_res

    def generate_keys(self):  # generates round keys
        self.keys = []
        key = string_to_bit_array(self.password)
        key = permute(key, CP_1)
        g, d = n_split(key, 28)
        for i in range(16):
            g, d = shift(g, d, SHIFT[i])
            tmp = g + d
            self.keys.append(permute(tmp, CP_2))

    def encrypt(self, text):
        return self.__run(text, 0)

    def decrypt(self, text):
        return self.__run(text, 1)
