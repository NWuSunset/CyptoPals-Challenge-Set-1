import binascii

# Encrypt something using the key ICE, by using repeating XOR
toEncrypt = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
key = "ICE"
xorBytes = bytearray()

bytesStr = toEncrypt.encode('ascii')
bytesKey = key.encode('ascii')

# XOR each byte of the input string with the corresponding byte of the key
for i in range(len(bytesStr)):
    xorBytes.append(bytesStr[i] ^ bytesKey[i % len(bytesKey)]) #XOR: char in bytes ^ remainder of i / 3. (Which will increment from 0 to 2)
    # ^
    # 0 / 3 = 0 r0
    # 1 / 3 = 0 r1
    # 2 / 3 = 0 r2
    # etc.

# Convert the result to hex
encryptedHex = binascii.hexlify(xorBytes).decode()
print(encryptedHex)

#Answer I get:
# 0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f

#Same as :
# 0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272
# a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f