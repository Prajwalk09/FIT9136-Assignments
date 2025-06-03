print("DECRYPT STRING")
encrypted_string = input("Input encrypted string: ")

# Initialize an empty string to store the decrypted string
decrypted_string = ""

# Checking in input encrypted string is empty
if encrypted_string.strip() == "":
    print("Empty encrypted string.")
    exit(0)

else:
    caesar_shift = input("Input caesar shift: ")

    # Checking for invalid caesar shift and exit the program, if true
    if not caesar_shift.isnumeric() or int(caesar_shift) < 0 or int(caesar_shift) > 25:
        print("Invalid caesar shift.")
        exit(0)

    else:
        caesar_shift = int(caesar_shift)
        for character in encrypted_string:

            # Skip spaces. No decoding
            if character == " ":
                continue

            '''ord(character) gives ASCII value and ord(character) - 65 gives the integer values in alphabet table
            for each alphabet. The next part is just subtracting caesar shift and getting the new value of shift
            which will be used for the next character in encrypted string.'''
            caesar_shift = (ord(character) - 65 - caesar_shift) % 26

            """char(integer) results in a character whose ASCII value is that integer and we add 65 to get alphabets 
            in range A-Z. The resulting character is appended to the decrypted string."""
            decrypted_string += chr(caesar_shift + 65)

    # Printing out the characters in the decrypted string
    print("The decrypted string is:")
    for character in decrypted_string:
        print(character)