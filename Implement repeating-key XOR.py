import binascii

#Encypt something using the key ICE, by using repeating XOR

toEncrypt = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
key = 'ICE'
xorStr = ''
xorList = []
#First convert to bytes
#Then XOR them
#then convert to hex

bytesStr = bytes(toEncrypt, 'utf-8')
bytesKey = bytes(key, 'utf-8')

#print(bytesKey, bytesStr)


for j in range(len(bytesKey)):
    xorStr = ''.join(chr(i ^ j) for i in bytesStr)
    print(xorStr)

    if j == 2: #go to the beginning again if we are at the end of the key
       j = 0

for i in xorStr:
    xorList.append(i)

#encrypted = ''.join(format(x, '02x') for x in xorStr)
encryptedHex = binascii.hexlify(bytearray(xorList))
print(encryptedHex)
