class DES_KeySchedule():
    def __init__(self, key):
        self.offsets = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
        key_bits = self.__bytes_to_bits(key)
        if len(key_bits) > 64:
            key_bits = key_bits[:64]
        else:
            key_bits = key_bits.zfill(64)
        self.key_bits = key_bits

    def __bytes_to_bits(self, block):
        return ''.join('{:08b}'.format(i) for i in block)

    def __bits_to_bytes(self, block):
        splitted = [''.join(block[i:i+8]) for i in range(0, len(block), 8)]
        int_bytes = map(lambda x: int(x, 2), splitted)
        return b''.join(map(lambda x: bytes([x]), int_bytes))

    def __permuted_choice_1(self, key_block):
        pc1_table = [57, 49, 41, 33, 25, 17, 9,
                     1, 58, 50, 42, 34, 26, 18,
                     10, 2, 59, 51, 43, 35, 27,
                     19, 11, 3, 60, 52, 44, 36,
                     63, 55, 47, 39, 31, 23, 15,
                     7, 62, 54, 46, 38, 30, 22,
                     14, 6, 61, 53, 45, 37, 29,
                     21, 13, 5, 28, 20, 12, 4]
        permuted = [key_block[i-1] for i in pc1_table]
        return permuted

    def __permuted_choice_2(self, key_block):
        pc2_table = [14, 17, 11, 24, 1, 5,
                     3, 28, 15, 6, 21, 10,
                     23, 19, 12, 4, 26, 8,
                     16, 7, 27, 20, 13, 2,
                     41, 52, 31, 37, 47, 55,
                     30, 40, 51, 45, 33, 48,
                     44, 49, 39, 56, 34, 53,
                     46, 42, 50, 36, 29, 32, ]
        permuted = [key_block[i-1] for i in pc2_table]
        return permuted

    def __rotate_left(self, block, offset):
        return block[offset:] + block[:offset]

    def generate(self):
        key_block = self.key_bits
        keys = []

        pc1_block = self.__permuted_choice_1(key_block)
        left_block = pc1_block[:len(key_block)//2]
        right_block = pc1_block[len(key_block)//2:]
        for i in range(16):
            left_block = self.__rotate_left(left_block, self.offsets[i])
            right_block = self.__rotate_left(right_block, self.offsets[i])
            full_key = left_block + right_block
            round_key_bits = self.__permuted_choice_2(full_key)
            round_key = self.__bits_to_bytes(round_key_bits)
            keys.append(round_key)
        return keys
