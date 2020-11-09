from des_cipher.des_key_schedule import DES_KeySchedule
from des_cipher.feistel import FeistelNetwork
from des_cipher.des_f_func import DES_F_func


class DES():
    def __init__(self, key):
        self.keys = DES_KeySchedule(key).generate()
        self.f_func = DES_F_func().f_func
        self.block_size = 8

    def __bytes_to_bits(self, block):
        return ''.join('{:08b}'.format(i) for i in block)

    def __bits_to_bytes(self, block):
        splitted = [''.join(block[i:i+8]) for i in range(0, len(block), 8)]
        int_bytes = map(lambda x: int(x, 2), splitted)
        return b''.join(map(lambda x: bytes([x]), int_bytes))

    def __initial_permutation(self, block):
        ip_table = [58, 50, 42, 34, 26, 18, 10, 2,
                    60, 52, 44, 36, 28, 20, 12, 4,
                    62, 54, 46, 38, 30, 22, 14, 6,
                    64, 56, 48, 40, 32, 24, 16, 8,
                    57, 49, 41, 33, 25, 17, 9, 1,
                    59, 51, 43, 35, 27, 19, 11, 3,
                    61, 53, 45, 37, 29, 21, 13, 5,
                    63, 55, 47, 39, 31, 23, 15, 7, ]
        block = self.__bytes_to_bits(block)
        permuted = [block[i-1] for i in ip_table]
        return self.__bits_to_bytes(permuted)

    def __final_permutation(self, block):
        fp_table = [40, 8, 48, 16, 56, 24, 64, 32,
                    39, 7, 47, 15, 55, 23, 63, 31,
                    38, 6, 46, 14, 54, 22, 62, 30,
                    37, 5, 45, 13, 53, 21, 61, 29,
                    36, 4, 44, 12, 52, 20, 60, 28,
                    35, 3, 43, 11, 51, 19, 59, 27,
                    34, 2, 42, 10, 50, 18, 58, 26,
                    33, 1, 41, 9, 49, 17, 57, 25, ]
        block = self.__bytes_to_bits(block)
        permuted = [block[i-1] for i in fp_table]
        return self.__bits_to_bytes(permuted)

    def encrypt_block(self, block):
        feistel = FeistelNetwork(self.keys, self.f_func)

        ip_block = self.__initial_permutation(block)
        cipher = feistel.feistel_encrypt_block(ip_block)
        fp_block = self.__final_permutation(cipher)
        return fp_block

    def decrypt_block(self, block):
        feistel = FeistelNetwork(self.keys, self.f_func)

        ip_block = self.__initial_permutation(block)
        cipher = feistel.feistel_decrypt_block(ip_block)
        fp_block = self.__final_permutation(cipher)
        return fp_block
