from typing import final

from adodbapi.ado_consts import adCurrency
from holoviews import output
from pyarrow import binary
from tomlkit import string

base = 16

hex1 = "1c0111001f010100061a024b53535009181c"
hex2 = "686974207468652062756c6c277320657965"

binary1 = bin(int(hex1, 16))[2:]
binary2 = bin(int(hex2, 16))[2:]




res = ''.join(format(i, '08b') for i in bytearray(hex1, encoding ='utf-8'))
res2 = ''.join(format(i, '08b') for i in bytearray(hex2, encoding ='utf-8'))

print(res)
print(res2)

#To properly XOR them they have to be the same length
accurateLen = len(binary1) if len(binary1) > len(binary2) else len(binary2)
bin_1 = binary1.zfill(accurateLen) #Fill either with zeros until desired length
bin_2 = binary2.zfill(accurateLen)


# Complete the XOR operation for individual bits within the two binaries. First zips the original binarys into a single list then loops through each bit
#Ex: for i, j in iterator. Basically condensing a for loop that does result = bin_1[i] ^ bin_2[i]
result = [int(bit1) ^ int(bit2) for bit1, bit2 in zip(bin_1, bin_2)]

string_result = ''.join(str(bits) for bits in result)
final_output = hex(int(string_result, 2))[2:]

print(string_result)
print(final_output)