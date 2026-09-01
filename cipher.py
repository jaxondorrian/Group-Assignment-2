def encrypt_file(s1, s2, inp, out):
# get the text
    file1 = open(inp, "r")
    text1 = file1.read()
    file1.close()

    result = ""

    for char in text1:

# lowercase a to n
        if "a" <= char <= "n":
            shift = s1 * s2
            num = ord(char) - 97
            num = (num + shift) % 26
            new = chr(num + 97)
            result = result + new

        # lowercase o to z
        elif "o" <= char <= "z":
            shift = s1 + s2
            num = ord(char) - 97
            num = (num - shift) % 26
            new = chr(num + 97)
            result = result + new
 # uppercase A to M
        elif "A" <= char <= "M":
            shift = s1
            num = ord(char) - 65
            num = (num - shift) % 26
            new = chr(num + 65)
            result = result + new
 # uppercase N to Z
        elif "N" <= char <= "Z":
            shift = s2 ** 2
            num = ord(char) - 65
            num = (num + shift) % 26
            new = chr(num + 65)
            result = result + new

   # numbers
        elif "0" <= char <= "9":
            shift = s1 - s2
            num = ord(char) - 48
            num = (num + shift) % 10
            new = chr(num + 48)
            result = result + new

 # everything else stays the same
        else:
            result = result + char

    file2 = open(out, "w")
    file2.write(result)
    file2.close()
