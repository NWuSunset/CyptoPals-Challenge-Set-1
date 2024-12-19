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
        avg = (sum(hammingDistance(a, b) for a, b in combinations(chunks, 2)) / 6)
        normalized_distance = avg / keysize #Divide by keysize to normalize


        #without using combinations in case that causes issues
        #distances = [hammingDistance(chunks[i], chunks[j]) for i in range(len(chunks)) for j in range(i + 1, len(chunks))]
        #avg_distance = sum(distances) / len(distances)  # Average the distances
        #normalized_distance = avg_distance / keysize  # Normalize by keysize

        print(f"Keysize: {keysize}, Normalized avg Hamming Distance: {normalized_distance}")
        lowest.append((normalized_distance, keysize))

    lowest.sort()
    return lowest

def transpose(blocks, blocksize):
    ret = []
    print(blocksize)
    #make a block that is the first byte of every block, and a block that is the second byte of every block, and so on.
    for byteNum in range(blocksize):
     #ret.append(blocks[block][byteNum] for block in range(len(blocks))) #appends blocks of bytes at position 'byteNum' in the blocks
     for block in range(len(blocks)):

        print(blocks[block])
        print(blocks[block][byteNum])


    return ret #returns list of byte blocks

print(hammingDistance(str1, str2)) #verifies if hamming distance is write

for line in b64File:
    strList.append(line.strip())

possibleKeys = findKeyLen(''.join(strList))[:5]
print(possibleKeys)

topSplitSizes = [] #List of lists of the original string broken into the top 5 keysizes
#loop through the original
for i in range(len(possibleKeys)):
    temp = [splitChunks(''.join(strList), possibleKeys[i][1])]
    #if temp[len(temp) - 1] != possibleKeys[i][1]:
    #    continue #skip this key
    topSplitSizes.append(splitChunks(''.join(strList) , possibleKeys[i][1]))
print(topSplitSizes)
