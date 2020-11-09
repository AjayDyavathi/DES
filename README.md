# DES
Data Encryption Standard implementation in pure python

This is a DES implementation in pure python from scratch. This implementation helps in understanding the DES algorithm better and analyse the flow.
DES was a US standard encryption algorithm, released in 1975 and was standardized in January 1977. It follows the balanced feistel network with 16 rounds. The key-length is 64 bits, but the effective key length is 56 bits (8 parity bits dropped). The block size is 64 bits (8 bytes). DES was developed by IBM with inputs from NSA. There're well known cryptanalysis methods for DES currently, as it uses 56 bit key length. It is not recommended to use DES for any real life purpose. However, Triple DES is still secure.

## Usage
###### Encryption
`$ python3 main.py -e -m ECB input_file output_file`
###### Encryption
`$ python3 main.py -d -m ECB input_file output_file`

[I'd not recommend encrypting/decrypting files more than an MB. Since this is written in pure python, It would take a lot of time to perform actions.]
