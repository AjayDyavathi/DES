class FeistelNetwork():
    '''
    Class that implements Feistel network.
    Note: It doesn't add any whitening or pre/post processing, this is just pure feistel.
    '''

    def __init__(self, keys, f_func, rounds=16, block_size=8):
        self.keys = keys
        self.round_count = rounds
        self.block_size = block_size
        self.f_func = f_func

    def _xor(self, a, b):
        a_i = int.from_bytes(a, "little")
        b_i = int.from_bytes(b, "little")
        return (a_i ^ b_i).to_bytes(len(a), "little")

    def _reverse(self, block):
        L = block[:self.block_size//2]
        R = block[self.block_size//2:]
        return R + L

    def round(self, block, round_key):
        L = block[:self.block_size//2]
        R = block[self.block_size//2:]

        R_prime = self.f_func(R, round_key)
        new_L = self._xor(L, R_prime)
        return R + new_L

    def feistel_encrypt_block(self, block):
        for i in range(self.round_count):
            block = self.round(block, self.keys[i])

        block = self._reverse(block)
        return block

    def feistel_decrypt_block(self, block):
        for i in range(self.round_count-1, -1, -1):
            block = self.round(block, self.keys[i])

        block = self._reverse(block)
        return block
