
hexFile = open("4hex.txt", "r") #open hex file for read only
#hexFile.readline() file organize in string lines
strList = []
scoreList = []

occurance_english = { #Dict of characters occurrences in english
    'a': 8.2389258,    'b': 1.5051398,    'c': 2.8065007,    'd': 4.2904556,
    'e': 12.813865,    'f': 2.2476217,    'g': 2.0327458,    'h': 6.1476691,
    'i': 6.1476691,    'j': 0.1543474,    'k': 0.7787989,    'l': 4.0604477,
    'm': 2.4271893,    'n': 6.8084376,    'o': 7.5731132,    'p': 1.9459884,
    'q': 0.0958366,    'r': 6.0397268,    's': 6.3827211,    't': 9.1357551,
    'u': 2.7822893,    'v': 0.9866131,    'w': 2.3807842,    'x': 0.1513210,
    'y': 1.9913847,    'z': 0.0746517
}


#find the weight/score of a decoded string
def weight(decoded):
    score = 0
    for i in decoded:
        if i in occurance_english.keys():
            score += occurance_english[i]
    return score

#Find the highest value (number) in a list
def findHighest(lst):
    high = 0
    for j in range(len(lst)):
        if lst[j] > lst[high]:
            high = j
    return high

#Seperate each individual string in the file into list
for i in hexFile:
    strList.append(i)

#Loop through the hex strings (lines) in the list
for x in strList:
   lineS = []
   bytesStr = bytes.fromhex(x) #convert to bytes
   for key in range(256):  # Loop through all possible bytes (0-255)
       decoded = ''.join(chr(i ^ key) for i in bytesStr) #XOR the hex string against a byte
       lineS.append((weight(decoded), decoded)) #find out the weight/score of the XORed line

   #find the largest decoded line (it was decoded with the most likely key)
   largest = findHighest(lineS)
   scoreList.append((lineS[largest][0], lineS[largest][1])) #add that line with the respective score to the list

#Find the line in the file that has the highest score
largestLine = findHighest(scoreList)
print(scoreList[largestLine][1]) #Final answer string

