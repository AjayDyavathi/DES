import os
import argparse
from modes import ECB
from pkcs import PKCS7
from des_cipher.des import DES
from iterators import file_block_iterator


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-e", "--encrypt", action="store_true")
    group.add_argument("-d", "--decrypt", action="store_true")
    parser.add_argument('-m', '--mode', choices=['ECB', 'CBC'], type=str, default='ECB')
    parser.add_argument('-i', '--iv', type=str, help='Initialization Vector, used for CBC mode')
    parser.add_argument('-n', '--nonce', type=str, help='Nonce to use for CTR mode')
    parser.add_argument("input_file")
    parser.add_argument("output_file")
    args = parser.parse_args()

    key = input("Enter {} key: ".format("encryption" if args.encrypt else "decryption"))
    key = key.encode("UTF-8")

    cipher = DES(key)
    padding_scheme = PKCS7(cipher.block_size)

    if args.mode == 'ECB':
        mode = ECB(cipher, padding_scheme)

    elif args.mode == "CBC":
        iv = args.iv.encode('utf-8') if args.iv else os.urandom(cipher.block_size)

        if len(iv) != cipher.block_size:
            raise ValueError("Invalid IV length")
        padding_scheme = PKCS7(cipher.block_size)
        mode = CBC(cipher, iv, padding_scheme)

    if args.encrypt:
        file_blocks = file_block_iterator(args.input_file, cipher.block_size)
        with open(args.output_file, 'wb') as f:
            for ciphertext in mode.encrypt(file_blocks):
                f.write(ciphertext)
    else:
        file_blocks = file_block_iterator(args.input_file, cipher.block_size)
        with open(args.output_file, 'wb') as f:
            for plaintext in mode.decrypt(file_blocks):
                f.write(plaintext)


if __name__ == "__main__":
    main()
