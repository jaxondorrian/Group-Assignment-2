def encrypt_file(s1, s2, inp, out): # this encrypts contect from the input files then reads it
    file = open(inp, "r")
    text = file.read()
    file.close()
    result = ""

    for char in text: # this for loop foes through each character om tje text file
        if "a" <= char <= "n":
                shift = s1 * s2
                value = ord(char) - 97
                value = (value + shift) % 26
                result = result + chr(value + 97)
        elif "o" <= char <= "z":
            shift = s1 + s2
            value = ord(char) - 97
            value = (value - shift) % 26
            result = result + chr(value + 97)
        elif "A" <= char <= "M":
            shift = s1
            value = ord(char) - 65
            value = (value - shift) % 26
            result = result + chr(value + 65)
        elif "N" <= char <= "Z":
            shift = s2 * s2
            value = ord(char) - 65
            value = (value + shift) % 26
            result = result + chr(value + 65)
        elif "0" <= char <= "9":
            shift = s1 - s2
            value = ord(char) - 48
            value = (value + shift) % 10
            result = result + chr(value + 48)
        else:
            result = result + char

    file = open(out, "w") #this savees the encrypted text
    file.write(result)
    file.close()
    
def decrypt_file(s1, s2, inp, out): # this decrypts the files
    file = open(inp, "r")
    text = file.read()
    file.close()
    result = ""
    for char in text:
        if "a" <= char <= "z":
            for letter in "abcdefghijklmnopqrstuvwxyz":
                if "a" <= letter <= "n":
                    shift = s1 * s2
                    value = ord(letter) - 97
                    value = (value + shift) % 26
                    check = chr(value + 97)
                else:
                    shift = s1 + s2
                    value = ord(letter) - 97
                    value = (value - shift) % 26
                    check = chr(value + 97)
                if check == char:
                    result = result + letter
                    break
        elif "A" <= char <= "Z":
            for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                if "A" <= letter <= "M":
                    shift = s1
                    value = ord(letter) - 65
                    value = (value - shift) % 26
                    check = chr(value + 65)
                else:
                    shift = s2 * s2
                    value = ord(letter) - 65
                    value = (value + shift) % 26
                    check = chr(value + 65)
                if check == char:
                    result = result + letter
                    break
        elif "0" <= char <= "9":
            shift = s1 - s2
            value = ord(char) - 48
            value = (value - shift) % 10
            result = result + chr(value + 48)
        else:
            result = result + char
    file = open(out, "w")
    file.write(result)
    file.close()

def verify_files(inp, dec):
        file = open(inp, "r")
        orignail = file.read()
        file.close()
        file = open(dec, "r")
        decrypted = file.read()
        file.close()
        if orignail == decrypted:
            print("Decryption was successful")
            return True
        else:
            print("Decryption was not successful")
            return False
# this will ask the user for the shift vaules
s1 = int(input("Enter shift1: "))
s2 = int(input("Enter shift2: "))
# this code just runs all the code results to the text files
encrypt_file(s1, s2, "raw_text.txt", "encrypted_text.txt")
decrypt_file(s1, s2, "encrypted_text.txt", "decrypted_text.txt")
verify_files("raw_text.txt", "decrypted_text.txt")
