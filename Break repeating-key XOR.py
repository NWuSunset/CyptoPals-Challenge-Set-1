from itertools import combinations #Used to find all possible combinations of the split chunks in the function findKeyLen


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

#Splits ciphertext into chunks of size 'splitSize'
def splitChunks(data, splitSize):
    return [data[i:i+splitSize] for i in range(0, len(data), splitSize)] #returns a list of the string split by keysize

def findKeyLen(list):
    lowest = [] #list from lowest from highest
    temp = 100


    for keysize in range(minKey, maxKey + 1):
        chunks = splitChunks(list, keysize)[:4] #Take only the first 4 blocks (of size keysize)
    
        if len(chunks) < 4:
            continue #If there are not enough chunks skip this keysize (shouldn't happen)
                                                             # 6 possible combinations (4 choose 2)
        avg = (sum(hammingDistance(a, b) for a, b in combinations(chunks, 2)) / 6)/keysize #Divide by keysize to normalize
        print(f"Keysize: {keysize}, Average Hamming Distance: {avg}")

        lowest.append((avg, keysize))

    lowest.sort()
    return lowest

def transpose(blocks, blocksize):
    ret = []
    #make a block that is the first byte of every block, and a block that is the second byte of every block, and so on.
    for j in range(len(blocks) + 1):
     ret.append(blocks[i] for i in range(0, len(blocks), blocksize + j)) #returns list of the j byte in every block
    return ret

print(hammingDistance(str1, str2))

for line in b64File:
    strList.append(line.strip())

print(findKeyLen(''.join(strList))[:5]) #Join the list of strings into one string

possibleKeys = findKeyLen(''.join(strList))[:5]

transpose(possibleKeys[][0], possibleKeys[][1])

