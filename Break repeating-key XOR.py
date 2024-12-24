from itertools import combinations #Used to find all possible combinations of the split chunks in the function findKeyLen
from base64 import b64decode #Helps make everything in terms of bytes (this fixed a bunch of issues and simplified some things)

b64File = open("6base64.txt", "r")

ciphertext = [line.strip() for line in b64File]

str1 = "this is a test"
str2 = "wokka wokka!!!"#

maxKey = 40
minKey = 2

occurrence_english = { #Dict of characters occurrences in english
    'a': 8.2389258,    'b': 1.5051398,    'c': 2.8065007,    'd': 4.2904556,
    'e': 12.813865,    'f': 2.2476217,    'g': 2.0327458,    'h': 6.1476691,
    'i': 6.1476691,    'j': 0.1543474,    'k': 0.7787989,    'l': 4.0604477,
    'm': 2.4271893,    'n': 6.8084376,    'o': 7.5731132,    'p': 1.9459884,
    'q': 0.0958366,    'r': 6.0397268,    's': 6.3827211,    't': 9.1357551,
    'u': 2.7822893,    'v': 0.9866131,    'w': 2.3807842,    'x': 0.1513210,
    'y': 1.9913847,    'z': 0.0746517
}

#xor set of bytes of same length (or it owuldn't work)
def xor_same_len(b1, b2):
    assert len(b1) == len(b2), "Byte set lengths don't match"
    return [b1[i] ^ b2[i] for i in range(len(b1))]

#hamming distance between two inputs
def hamming_distance(in1, in2):
    xored_bytes = xor_same_len(in1, in2)
    binary_bytes = [bin(i)[2:] for i in xored_bytes] #remember to remove 0b from the beginning ([2:])
    binary_str = ''.join(binary_bytes)
    binary = [int(bit) for bit in binary_str]
    distance = sum(binary)
    return distance

    #old code, new one is able to take in types that are not strings (makes it easier)

    #arr1 = str1.encode()
    #arr2 = str2.encode() #turn them into byte arrays
    #int1 = int.from_bytes(arr1, "big")
    #int2 = int.from_bytes(arr2, "big")

    #bin1 = bin(int1)
    #bin2 = bin(int2)

    #return sum (bit1 != bit2 for bit1, bit2 in zip(bin1, bin2))

#Splits ciphertext into chunks of size 'splitSize'
def split_chunks(data, split_size):
    return [data[i:i + split_size] for i in range(0, len(data), split_size)
            if i < len(data) - split_size #ensures that a chunk that is not of the correct size is not returned (this fixed my ISSUE!!)
            ] #returns a list of the string split by keysize


def normalized_distance(text, keysize):
    assert keysize < len(text) / 2, "Text is to short to make two blocks for this keysize"
    byte_list = b64decode(text) #make sure that the text is in bytes (this fixes a few issues)

    chunks = split_chunks(byte_list, keysize)[:4]

    avg = (sum(hamming_distance(a, b) for a, b in combinations(chunks, 2)) / 6) #6 possible combinations
    normalized = avg / keysize
    return normalized

   # chunks = split_chunks(text, keysize)[:4] #Take only the first 4 blocks (of size keysize)
    
   # if len(chunks) < 4:
   #     return #If there are not enough chunks skip this keysize (shouldn't happen)
                                                             # 6 possible combinations (4 choose 2)
   # avg = (sum(hamming_distance(a, b) for a, b in combinations(chunks, 2)) / 6)
   # return avg / keysize #Divide by keysize to normalize

#find smallest in a list
def smallest_distance(inputs):
    sorted_input = sorted(inputs, reverse=False)
    return sorted_input[0]

def find_key_size(text):
    normalized_distances = [(normalized_distance(text, keysize), keysize) for keysize in range(minKey, maxKey + 1)  ] #a list of normalized distance tupled with their respective keysize

    #Longer line version (for testing)
    #normalized_distances = []
    #for keysize in range(minKey, maxKey):
    #    distance = normalized_distance(text, keysize)
    #    print(f"Keysize: {keysize}, Normalized avg Hamming Distance: {distance}")
    #    normalized_distances.append((distance, keysize))
    key_size = smallest_distance(normalized_distances)
    return key_size[1] #only have to return the keysize

#transposes the blocks (that are broken into 'keysize'): blocks that are broken into the # byte of every keysize block
def transpose(text, blocksize):
    byte_list = b64decode(text)
    chunks = split_chunks(byte_list, blocksize)

    transposed = [  [chunks[block][byteNum] for block in range(len(chunks)) ]
                                            for byteNum in range(blocksize) ]

    return transposed #returns list of byte blocks

#find the weight/score of a letter string (based on the letter occurrence in english)
def weight(string):
    #score = 0
    #for i in decoded:
     #   if i in occurance_english.keys():
      #      score += occurance_english[i]

    #Score is the sum of all letters in the string based on the occurrence in english
    score = sum(occurrence_english.get(i, 0) for i in string)
    return score

#Find the highest value (number) in an iterable
def find_highest(iterable):
    #high = 0
    #for j in range(len(iterable)):
    #    if iterable[j] > iterable[high]:
     #       high = j
    high = max(range(len(iterable)), key = iterable.__getitem__) #key = iterable.__getitem__ just makes sure the comparison is done with the iterable values
    return high #return the index of the highest

#perform the single byte xor operation (single key against a set of bytes
def single_byte_xor(byte_list, key):
    xor_result = [byte ^ key for byte in byte_list]
    return xor_result

#This function been simplified from my original code in detect single char XOR
#find the single (ASCII) character that  would have been used to xor the bytes
def find_single_xor(block):
    #performce the singleXOR operation through all single (ASCII) characters (and make a list of all of those)
    xor_bytes = [single_byte_xor(block, character) for character in range(128)]
    xor_strings = [''.join(map(chr, byte_set)) for byte_set in xor_bytes] #converts the xor_bytes into a string by performing the chr operation on each byte set of xor_bytes

    #go through xor strings and determine the weight, then find the highest weight and that is the string that has been xored against the right character. The index of that string is the ASCII character that it has been xored against
    key = chr(find_highest([weight(string) for string in xor_strings]))
    return key

#determine which key was used to XOR encrypt the text
def find_key(block_text):
    key_size = find_key_size(block_text) #find the correct keysize
    transposed_blocks = transpose(block_text, key_size) #create the transposed blocks
    final_key = ''.join([find_single_xor(block) for block in transposed_blocks]) #Determine the single xor ASCII character for each transposed block
    return final_key #final string of ASCII characters

#finally decrypt the text
def decrypt_text(encrypted_text, key):
    bytes_text = b64decode(encrypted_text)
    bytes_key = bytes(key, 'utf-8') #convert ASCII key to bytes

    #basically the same method from Implement repeating-key XOR, except enumerate is used iterate over the i and byte (index, value) simultaneously (so it can be a single line :) )
    decrypted_bytes = [byte ^ bytes_key[i % len(bytes_key)] for i, byte in enumerate(bytes_text)]
    decrypted_chars = [chr(byte) for byte in decrypted_bytes] #convert the decrypted bytes into characters
    decrypted_text = ''.join(decrypted_chars)
    return decrypted_text

#print(hamming_distance(str1, str2)) #verifies if hamming distance is right


def run_program():
    encrypted_text = ''.join(ciphertext)
    key = find_key(encrypted_text)
    decrypted = decrypt_text(encrypted_text, key)
    print(decrypted)

run_program() #Almost works, some single characters are broken
#keysize = find_key_size(''.join(ciphertext))
#print(keysize)
