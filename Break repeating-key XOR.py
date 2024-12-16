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

def findKeyLen(list):
    def splitChunks(data, splitSize):
        #str = ""
        #for char in range(0, splitSize):
        #    str += data[char]
        return [data[i:i+splitSize] for i in range(0, len(data), splitSize)]

    
    for keysize in range(minKey, maxKey + 1):
        chunks = splitChunks(list, keysize)[:4] #Take first 4 chunks of size keysize
        #sum = sum(hammingDistance(a, b) for a, b in combinations(chunks, 2))
    
        if len(chunks) < 4:
            continue #If there are not enough chunks

        avg = sum(hammingDistance(a, b) for a, b in combinations(chunks, 2)) / 6 #6 possible combinations (4 choose 2)
        print(f"Keysize: {keysize}, Average Hamming Distance: {avg}")

    
    #avg = sum / 6*38 #Choose two chunks out of the number of chunks and do the hamming distance for them
                                                                             #then divide by 4 choose 2 = 6 (6 possible combinations)(total combinations)


   # blocks, blockSize = len(list), int(len(list)/5)
   #  list[j:j+blockSize] for j in range(0, blocks, blockSize)

    #avg = sum(hammingDistance(a, b) for a, b in)

print(hammingDistance(str1, str2))

for line in b64File:
    strList.append(line.strip())

findKeyLen(''.join(strList)) #Join the list of strings into one string


