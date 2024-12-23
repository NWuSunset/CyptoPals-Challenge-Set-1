from itertools import combinations #Used to find all possible combinations of the split chunks in the function findKeyLen
from base64 import b64decode

b64File = open("6base64.txt", "r")

ciphertext = []

for line in b64File:
    ciphertext.append(line.strip())

str1 = "this is a test"
str2 = "wokka wokka!!!"#

maxKey = 40
minKey = 2

occurance_english = { #Dict of characters occurrences in english
    'a': 8.2389258,    'b': 1.5051398,    'c': 2.8065007,    'd': 4.2904556,
    'e': 12.813865,    'f': 2.2476217,    'g': 2.0327458,    'h': 6.1476691,
    'i': 6.1476691,    'j': 0.1543474,    'k': 0.7787989,    'l': 4.0604477,
    'm': 2.4271893,    'n': 6.8084376,    'o': 7.5731132,    'p': 1.9459884,
    'q': 0.0958366,    'r': 6.0397268,    's': 6.3827211,    't': 9.1357551,
    'u': 2.7822893,    'v': 0.9866131,    'w': 2.3807842,    'x': 0.1513210,
    'y': 1.9913847,    'z': 0.0746517
}

def hamming_distance(str1, str2):
    arr1 = str1.encode()
    arr2 = str2.encode() #turn them into byte arrays
    int1 = int.from_bytes(arr1, "big")
    int2 = int.from_bytes(arr2, "big")

    bin1 = bin(int1)
    bin2 = bin(int2)

    return sum (bit1 != bit2 for bit1, bit2 in zip(bin1, bin2))

#Splits ciphertext into chunks of size 'splitSize'
def split_chunks(data, split_size):
    return [data[i:i + split_size] for i in range(0, len(data), split_size)] #returns a list of the string split by keysize


def normalized_distance(text, keysize):
    chunks = split_chunks(text, keysize)[:4] #Take only the first 4 blocks (of size keysize)
    
    if len(chunks) < 4:
        return #If there are not enough chunks skip this keysize (shouldn't happen)
                                                             # 6 possible combinations (4 choose 2)
    avg = (sum(hamming_distance(a, b) for a, b in combinations(chunks, 2)) / 6)
    return avg / keysize #Divide by keysize to normalize

    #without using combinations in case that causes issues
    #distances = [hammingDistance(chunks[i], chunks[j]) for i in range(len(chunks)) for j in range(i + 1, len(chunks))]
    #avg_distance = sum(distances) / len(distances)  # Average the distances
    #normalized_distance = avg_distance / keysize  # Normalize by keysize

def find_key_size(text):
    lowest = []

    for keysize in range(minKey, maxKey):
        distance = normalized_distance(text, keysize)
        print(f"Keysize: {keysize}, Normalized avg Hamming Distance: {distance}")
        lowest.append((distance, keysize))

    lowest.sort()
    print(lowest[0])
    return lowest[0][1]

def transpose(text, blocksize):
    chunks = split_chunks(text, blocksize)
    #print(blocksize)
    #make a block that is the first byte of every block, and a block that is the second byte of every block, and so on.
    #for byteNum in range(blocksize - 1):
     #ret.append(blocks[block][byteNum] for block in range(len(blocks))) #appends blocks of bytes at position 'byteNum' in the blocks
     #for block in range(len(text)):

      # print(text[block])
       #print(text[block][byteNum])

    transposed = []
    for byteNum in range(blocksize):
        temp = []
        for block in range(len(chunks)):
            if len(chunks[block]) != 3:
                chunks[block] += '0'
            temp.append(chunks[block][byteNum])
        transposed.append(temp)
    return transposed #returns list of byte blocks

#find the weight/score of a decoded string
def weight(decoded):
    score = 0
    for i in decoded:
        if i in occurance_english.keys():
            score += occurance_english[i]
    return score

#Find the highest value (number) in a list
def find_highest(lst):
    high = 0
    for j in range(len(lst)):
        if lst[j] > lst[high]:
            high = j
    return high

def find_single_xor(block):
    scoreList = []
    # Loop through the hex strings (lines) in the list
    for x in block:
        lineS = []
        bytes_str = bytes(x, 'utf-8') # convert to bytes
        for key in range(256):  # Loop through all possible bytes (0-255)
            decoded = ''.join(chr(i ^ key) for i in bytes_str)  # XOR the hex string against a byte
            lineS.append((weight(decoded), decoded, key))  # find out the weight/score of the XORed line

        # find the largest decoded line (it was decoded with the most likely key)
        largest = find_highest(lineS)
        scoreList.append((lineS[largest][0], lineS[largest][1], lineS[largest][2]))  # add that line with the respective score to the list

    # Find the line in the file that has the highest score
    largestLine = find_highest(scoreList)
    print(scoreList[largestLine][1])  # Final answer string
    return chr(scoreList[largestLine][2]) #Final answer key

def find_block_key(block_text):
    key_size = find_key_size(block_text) #make keylength only return one thing?
    transposed = transpose(''.join(block_text), key_size)
    print(transposed)
    final_key = ''.join([find_single_xor(i) for i in transposed]) #join all the keys together into the single key
    return final_key

def decrypt_text(ciphertext, key):
    bytes_text = b64decode(ciphertext)
    #bytes_key = bytearray.fromhex(key.encode('utf-8').hex())
    bytes_key = bytes(key, 'utf-8')
    print(bytes_key)
    #basically the same from Implement repeating-key XOR, except enumerate is used iterate over the i and byte (index, value) simultaneously (so it can be a single line :) )
    decrypted_bytes = [byte ^ bytes_key[i % len(bytes_key)] for i, byte in enumerate(bytes_text)]
    decrypted_chars = [chr(byte) for byte in decrypted_bytes]
    decrypted_text = ''.join(decrypted_chars)
    return decrypted_text

print(hamming_distance(str1, str2)) #verifies if hamming distance is write


def run_program():
    key = find_block_key(''.join(ciphertext))
    decrypted = decrypt_text(''.join(ciphertext), key)
    print(key)
    print(decrypted)

run_program() #Currently running with only a keysize of 3 being tested (change to maybe top 5 keysizes in findkeylen()
