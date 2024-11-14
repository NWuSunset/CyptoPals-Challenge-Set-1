base = 16;

hex1 = "1c0111001f010100061a024b53535009181c"
hex2 = "686974207468652062756c6c277320657965"

binary1 = bin(int(hex1, 16))[2:]
binary2 = bin(int(hex2, 16))[2:]
# convert to binary fisrt

# Then make them the same length?

# Then use the XOR operation on each bit

# Complete the XOR operation for individual bits within the two binaries. First zips the original binarys into a single list then loops through each bit
#Ex: for i, j in iterator
result = [int(bit1) ^ int(bit2) for bit1, bit2 in zip(binary1, binary2)]
#use .join

print(list(result))
print(binary1)
print("\n")
print(binary2)