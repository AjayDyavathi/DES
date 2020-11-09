class PKCS7():
    '''
    Class that implements PKCS7 padding standard
    '''

    def __init__(self, block_size):
        self.block_size = block_size

    def apply(self, block):
        if len(block) == self.block_size:
            return block + bytes([self.block_size] * self.block_size)

        diff = self.block_size - len(block)
        return block + bytes([diff] * diff)

    def remove(self, block):
        if not len(block) == self.block_size:
            raise Exception("Padding Error: Incorrect block size")

        padding_length = int(block[-1])
        padding = block[-padding_length:]

        if padding_length == 0:
            return block

        for val in padding:
            if not val == padding_length:
                raise Exception("Unknown character in padding: {}".format(val))

        return block[:-padding_length]
