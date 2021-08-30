#!/bin/python
import codecs
import sys

def test(argv):

    with open(argv[1], "rb") as f:
        hexdump = []
        for chunk in iter(lambda: f.read(1), b''):
            hexdump.append(codecs.encode(chunk, 'hex'))

        i = 68608
        char = hexdump[i]
        password = ""
        while char != b'00':
            num = char.decode('ascii')
            #print(chr(int(num, 16)-2))
            password += chr(int(num, 16)-2)
            i += 1
            char = hexdump[i]

        print(password)

def process(data):
    data = data.decode('ascii')
    if '.php' in data:
        return ['Gate', data]

    if '.exe' in data:
        return ['Malware', data]

    password = ""
    for c in data:
        password += chr(ord(c)-2)

    return ["Password", password]

def main(argv):

    with open(argv[1], "rb") as f:
        hexdump = f.read()
        print("File opened...")
        p = hexdump.find(b'YUIPWDFILE0YUIPKDFILE0YUICRYPTED0YUI1')
        if p == -1:
            print("This doesn't look like a Pony, sorry!")

        print("Found Pony firgerprint.")

        i = 1
        while hexdump[p-i-2:p-i] != b'\x00\x00':
            i += 1

        print("The brute data found was:\n")
        data = [d.decode('ascii') for d in hexdump[p-i:p-2].split(b'\x00')]
        print(data)


        print("\nThe processed data:\n")
        processed_data = [process(d) for d in hexdump[p-i:p-2].split(b'\x00')]
        for data in processed_data:
            print(data[0] + " | " + data[1])


        print("\nFor more information, the personal data is store before " + str(hex(p)) + "/" + str(p) + " offset.")

if __name__ == "__main__":
    main(sys.argv)
