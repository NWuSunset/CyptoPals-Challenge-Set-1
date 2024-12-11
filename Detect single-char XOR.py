
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

#run through each line and track which line has the bset score

#find the weight/score of a decoded string
def weight(decoded):
    score = 0
    for i in decoded:
        if i in occurance_english.keys():
            score += occurance_english[i]
    return score

for i in hexFile: #60 strings in the file
    strList.append(i)

for x in strList:
    lineScore = 0
    decoded = ''

    # convert from hex to bytes
    byes = bytes.fromhex(x)
    print(byes)

    for key in range(256):  # 0-255 is all possible bytes
        decoded = ''.join(chr(i ^ key) for i in byes)

        lineScore += weight(decoded) #determine the score of the line

 #add the line score to the list, along with the decoded line
    #print(lineScore, decoded)
    scoreList.append((lineScore, decoded))




#find the highest score
largest = 0
for i in range(len(scoreList)):
    if scoreList[i] > scoreList[largest]:
        largest = i

# Print out the answer
print(scoreList[largest])