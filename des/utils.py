def bin_value(val, bit_size):  # Return the binary value as a string of the given size
    bin_val = bin(val)[2:] if isinstance(val, int) else bin(ord(val))[2:]
    if len(bin_val) > bit_size:
        raise "binary value larger than the expected size"
    while len(bin_val) < bit_size:
        bin_val = "0" + bin_val  # Add as many 0 as needed to get the wanted size
    return bin_val


def string_to_bit_array(text):  # Convert a string into a list of bits
    array = list()
    for char in text:
        bin_val = bin_value(char, 8)  # Get the char value on one byte
        array.extend([int(x) for x in list(bin_val)])  # Add the bits to the final list
    return array


def bit_array_to_string(array):  # Recreate the string from the bit array
    res = ''.join([chr(int(y, 2)) for y in [''.join([str(x) for x in _bytes]) for _bytes in n_split(array, 8)]])
    return res


def n_split(s, n):  # Split a list into sub-lists of size "n"
    return [s[k: k + n] for k in range(0, len(s), n)]
