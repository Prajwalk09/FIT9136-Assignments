print("DECRYPT STRING")
encrypted_string = input("Input encrypted string: ")
# Initialize an empty string to store the decrypted string
decrypted_string = ""
index = 0
# Checking in input encrypted string is empty
if encrypted_string.strip() == "":
    print("Empty encrypted string.")
    exit(0)

else:
    # Taking input for vigenere key
    vigenere_key = input("Input vigenère key: ")

    # Checking for invalid vigenere key and exit the program, if true
    if vigenere_key == "":
        print("Invalid vigenère key.")
        exit(0)

    else:
        # Decoding each letter of the encrypted string
        for i in range(len(encrypted_string)):
            if encrypted_string[i] == " ":
                continue
            else:
                """Formula used here is Decrypted Text = (Encrypted Text - Vigenere key + 26) % 26.

                The chr() function is used to get the character from the ASCII value.

                The ord() function is used to get the ASCII value of a particular character."""

                decrypted_string += chr((ord(encrypted_string[i]) - ord(vigenere_key[index]) + 26) % 26 + 65)

                """Updating the pointer in the vigenere key to ensure proper decryption happens even when the key is 
                smaller than the encrypted string.
                """
                index = (index + 1) % len(vigenere_key)

    # Displaying the characters of the decrypted string
    print("The decrypted string is:")
    for character in decrypted_string:
        print(character)


