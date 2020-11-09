def eof_signal_iterator(iterable):
    iterable = iter(iterable)
    prev = next(iterable)

    for item in iterable:
        yield prev, False
        prev = item

    yield prev, True


def file_block_iterator(file_path, block_size):
    with open(file_path, 'rb') as f:
        block = f.read(block_size)
        while block != b'':
            yield block
            block = f.read(block_size)


def list_block_iterator(message, block_size):
    for idx in range(0, len(message), block_size):
        yield message[idx:idx+block_size]
