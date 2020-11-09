from iterators import eof_signal_iterator


class ModesOfOperation():
    def __init__(self, cipher, iv=None, nonce=None):
        self.cipher = cipher
        self.iv = iv
        self.nonce = nonce
        self.block_size = cipher.block_size

    def _xor(self, block1, block2):
        return bytes([a ^ b for a, b in zip(block1, block2)])


class ECB(ModesOfOperation):
    def __init__(self, cipher, padding_scheme):
        super(ECB, self).__init__(cipher)
        self.padding_scheme = padding_scheme

    def encrypt(self, block_iterator):
        eof_iterator = eof_signal_iterator(block_iterator)

        for data, eof in eof_iterator:
            if not eof:
                ciphertext = self.cipher.encrypt_block(data)
            else:
                block = self.padding_scheme.apply(data)
                if len(block) == self.block_size:
                    ciphertext = self.cipher.encrypt_block(block)

                elif len(block) == self.block_size * 2:
                    ciphertext = self.cipher.encrypt_block(block[:self.block_size]) + \
                        self.cipher.encrypt_block(block[self.block_size:])
                else:
                    raise Exception("Padding Error: Padding scheme returned block that is not a multiple of block_size")
            yield ciphertext

    def decrypt(self, block_iterator):
        eof_iterator = eof_signal_iterator(block_iterator)

        for data, eof in eof_iterator:
            plaintext = self.cipher.decrypt_block(data)
            block = plaintext if not eof else self.padding_scheme.remove(plaintext)
            yield block


class CBC(ModesOfOperation):
    def __init__(self, cipher, iv, padding_scheme):
        super(CBC, self).__init__(cipher, iv=iv)
        self.padding_scheme = padding_scheme
        self.ciphertext = None

    def encrypt(self, block_iterator):
        eof_iterator = eof_signal_iterator(block_iterator)

        for data, eof in eof_iterator:
            if not self.ciphertext:
                self.ciphertext = self.iv
                yield self.ciphertext

            if not eof:
                self.ciphertext = self.cipher.encrypt_block(self._xor(self.ciphertext, data))
            else:
                block = self.padding_scheme.apply(data)
                if len(block) == self.block_size:
                    self.ciphertext = self.cipher.encrypt_block(self._xor(self.ciphertext, block))
                elif len(block) == self.block_size * 2:
                    last_block = self.cipher.encrypt_block(self._xor(self.ciphertext, block[:self.block_size]))
                    self.ciphertext = self.cipher.encrypt_block(self._xor(last_block, block[self.block_size:]))
                    self.ciphertext = last_block + self.ciphertext
                else:
                    raise Exception("Padding Error: Padding scheme returned block that is not a multiple of block_size")

    def decrypt(self, block_iterator):
        eof_iterator = eof_signal_iterator(block_iterator)

        self.ciphertext, eof = next(eof_iterator)
        for data, eof in eof_iterator:
            plaintext = self._xor(self.ciphertext. self.cipher.decrypt(data))
            self.ciphertext = data
            block = plaintext if not eof else self.padding_scheme.remove(plaintext)
            yield block
