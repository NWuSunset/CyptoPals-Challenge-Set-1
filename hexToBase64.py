import codecs


def hextobase64():
    hexinput = input("Input hex string: ")
    base64b = codecs.encode( codecs.decode(hexinput, 'hex'), 'base64')
    base64str = base64b.decode("utf-8") #convert to string
    print(base64str)