from itertools import combinations
from os.path import split

from xlwings.utils import chunk

b64File = open("6base64.txt", "r")

strList = []

str1 = "this is a test"
str2 = "wokka wokka!!!"#

maxKey = 40
minKey = 2

def hammingDistance(str1, str2):
    arr1 = str1.encode()
    arr2 = str2.encode() #turn them into byte arrays
    int1 = int.from_bytes(arr1, "big")
    int2 = int.from_bytes(arr2, "big")

    bin1 = bin(int1)
    bin2 = bin(int2)

    return sum (bit1 != bit2 for bit1, bit2 in zip(bin1, bin2))

def findKeyLen():
    #split up blocks into key size
    list = "hi guys"


    def splitChunks(list, size):
        str = ""
        for char in range(0, size):
            str += list[char]
        return str

    print(splitChunks(list, 2))
    chunks = (splitChunks(list, 2), splitChunks(list, 10), splitChunks(list, 20), splitChunks(list, 40)) #tuple of 4 chunks

    #combinations(chunks, chunk())


   # blocks, blockSize = len(list), int(len(list)/5)
   #  list[j:j+blockSize] for j in range(0, blocks, blockSize)

    #avg = sum(hammingDistance(a, b) for a, b in)

print(hammingDistance(str1, str2))

for i in b64File:
    strList.append(i)

findKeyLen()


