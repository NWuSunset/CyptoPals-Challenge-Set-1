from itertools import combinations #Used to find all possible combinations of the split chunks in the function findKeyLen
from base64 import b64decode #Helps make everything in terms of bytes (this fixed a bunch of issues and simplified some things)

b64File = open("6base64.txt", "r")

ciphertext = [line.strip() for line in b64File]

str1 = bytes("this is a test", 'utf-8')
str2 = bytes("wokka wokka!!!", 'utf-8')

maxKey = 40
minKey = 2

#Original 'e': 12.813865, changed e value because for some reason a string decoded by ( had a lot of 'e' causing it to be higher than the actual character?
#The string that broke it ( ( , 409.4333516000001) :
# e) $-)1)1e-eee6eO1ee(!5e#<5h ,#eeh++ee+be<ee$+$,e 7$0"1e-$)++$) 0eekd<e!7$ee!ee,- *he*-$-ee$e1e2*

#the string that was supposed to be ( m, 381.1998719999999 ):
 #leahltlt h   sA
# t  mdp fyp-Feif  -nn  n' y  anai eraugt halnnaleu  .!y dra  d  iheo- ohah  a t wo


#'e' was changed to 10.813865 to fix this (caused a big headache)
occurrence_english = { #Dict of characters occurrences in english
    'a': 8.2389258,    'b': 1.5051398,    'c': 2.8065007,    'd': 4.2904556,
    'e': 10.813865,    'f': 2.2476217,    'g': 2.0327458,    'h': 6.1476691,
    'i': 6.1476691,    'j': 0.1543474,    'k': 0.7787989,    'l': 4.0604477,
    'm': 2.4271893,    'n': 6.8084376,    'o': 7.5731132,    'p': 1.9459884,
    'q': 0.0958366,    'r': 6.0397268,    's': 6.3827211,    't': 9.1357551,
    'u': 2.7822893,    'v': 0.9866131,    'w': 2.3807842,    'x': 0.1513210,
    'y': 1.9913847,    'z': 0.0746517
}

#xor set of bytes of same length
def xor_same_len(b1, b2):
    assert len(b1) == len(b2), "Byte set lengths don't match"
    return [b1[i] ^ b2[i] for i in range(len(b1))]

#hamming distance between two sets of bytes (number of bits that differ)
def hamming_distance(in1, in2):
    #first xor the bytes (so the '1's in the binary would be the differing bits)
    xored_bytes = xor_same_len(in1, in2)

    #convert bytes to binary
    binary_bytes = [bin(i)[2:] for i in xored_bytes] #remember to remove 0b from the beginning ([2:])
    binary_str = ''.join(binary_bytes)
    binary = [int(bit) for bit in binary_str]

    # add the sum of the bits which is the hamming distance (each 1 in the binary would represent a differing bit in the original byte sets
    distance = sum(binary)
    return distance

#Splits text into chunks of size 'splitSize'
def split_chunks(data, split_size):
    return [data[i:i + split_size] for i in range(0, len(data), split_size)
            if i < len(data) - split_size #ensures that a chunk that is not of the correct size is not returned (this fixed my ISSUE with the wrong keysize)
            ] #returns a list of the string split by keysize

#Get the normalized distance between hamming distances by taking the average of 4 'keysize' blocks
def normalized_distance(text, keysize):
    assert keysize < len(text) / 2, "Text is to short to make two blocks for this keysize"

    byte_list = b64decode(text) #make sure that the text is in bytes

    chunks = split_chunks(byte_list, keysize)[:4] #split into only the first 4 blocks

    #averaging the distances between 4 keysize blocks (using combinations: takes the 4 blocks and apply hamming_distance operation between two of them, does this for each combination (totaling 6 combos))
    avg = (sum(hamming_distance(a, b) for a, b in combinations(chunks, 2)) / 6) #6 possible combinations
    normalized = avg / keysize #divide by keysize to normalize
    return normalized

#find smallest in a list
def smallest_distance(inputs):
    #sort the inputs in ascending order
    sorted_input = sorted(inputs, reverse=False)
    return sorted_input[0] #will only return the first item in the list

def find_key_size(text):
    # a list of tuples containing: normalized_distance, keysize)
    normalized_distances = [(normalized_distance(text, keysize), keysize) for keysize in range(minKey, maxKey + 1)  ]
    key_size = smallest_distance(normalized_distances) #find the one with the smallest normalized distance

    # only have to return the keysize
    return key_size[1]

#transposes the blocks (that are broken into 'keysize'): blocks that are broken into the # byte of every keysize block
def transpose(text, chunk_size):
    byte_list = b64decode(text)
    chunks = split_chunks(byte_list, chunk_size)

    # Transpose the chunks of bytes such that each transposed block contains bytes from the same position in each chunk.
    transposed = [[chunks[block][byteNum] for block in range(len(chunks)) ]
                                          for byteNum in range(chunk_size)]

    return transposed #returns list of byte blocks

#find the weight/score of a letter string (based on the letter occurrence in english)
def weight(string):
    #Score is the sum of all letters in the string based on the occurrence in english
    score = sum(occurrence_english.get(i, 0) for i in string)
    return score

#Find the index with the highest (number) value in an iterable
def find_highest(iterable):
    high = max(range(len(iterable)), key = iterable.__getitem__) #key = iterable.__getitem__ just makes sure the comparison is done with the iterable values
    return high #return the index of the highest in the iterable

#perform the single byte xor operation (single key against a set of bytes)
def single_byte_xor(byte_list, key):
    xor_result = [byte ^ key for byte in byte_list]
    return xor_result

#This function been simplified from my original code in detect single char XOR (and because that one was meant more for a hex string)
#find the single (ASCII, since it should only be ascii in this case) character that would have been used to xor the bytes in a string
def find_single_xor(block):
    #performce the single-character-XOR operation through all single (ASCII) characters (and make a list of all of those)
    xor_bytes = [single_byte_xor(block, character) for character in range(128)]
    xor_strings = [''.join(map(chr, byte_set)) for byte_set in xor_bytes] #convert the xor_bytes into a string by performing the chr operation on each byte set of xor_bytes

    #go through xor strings and determine the weight, then find the highest weight and that is the string that has been xored against the right character.
    # The index of that string is the ASCII character that it has been xored against
    key = chr(find_highest([weight(string) for string in xor_strings]))
    return key

#determine which key was used to XOR encrypt the entire text
def find_key(block_text):
    key_size = find_key_size(block_text) #find the correct key_size
    transposed_blocks = transpose(block_text, key_size) #create the transposed blocks
    final_key = ''.join([find_single_xor(block) for block in transposed_blocks]) #Determine the single xor ASCII character for each transposed block
    return final_key #final string of ASCII characters

#finally decrypt the text using a specified key
def decrypt_text(encrypted_text, key):
    bytes_text = b64decode(encrypted_text)
    bytes_key = bytes(key, 'utf-8') #convert ASCII key to bytes

    #basically the same method from Implement repeating-key XOR, except enumerate is used iterate over the i and byte (index, value) simultaneously (so it can be a single line :) )
    decrypted_bytes = [byte ^ bytes_key[i % len(bytes_key)] for i, byte in enumerate(bytes_text)]
    decrypted_chars = [chr(byte) for byte in decrypted_bytes] #convert the decrypted bytes into characters
    decrypted_text = ''.join(decrypted_chars) #finally put all the characters together
    return decrypted_text

#Just found out that this is actually a Vigenere cipher
def run_program():
    #join all the lines of base64 encoded file together
    encrypted_text = ''.join(ciphertext)
    key = find_key(encrypted_text) #Find the decryption key
    decrypted = decrypt_text(encrypted_text, key) #decrpyt the text with it
    print(key)
    print(decrypted)

assert hamming_distance(str1, str2) == 37, "Hamming distance don't work :("
run_program()

