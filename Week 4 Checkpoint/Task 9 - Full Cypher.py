# Declare constants

def caesar_cypher(encrypted_text, shift):
    decrypted_string = ""
    if shift < 0 or shift > 25:
        print("Invalid caesar shift.")
        exit(0)

    else:
        for character in encrypted_string:

            # Skip spaces. No decoding
            if character == " ":
                continue

            '''ord(character) gives ASCII value and ord(character) - 65 gives the integer values in alphabet table
            for each alphabet. The next part is just subtracting caesar shift and getting the new value of shift
            which will be used for the next character in encrypted string.'''
            shift = (ord(character) - 65 - shift) % 26

            """char(integer) results in a character whose ASCII value is that integer and we add 65 to get alphabets 
            in range A-Z. The resulting character is appended to the decrypted string."""
            decrypted_string += chr(shift + 65)

    return decrypted_string


def vigenere_cipher(encrypted_text, key):
    decrypted_string = ""
    index = 0
    # Checking in input encrypted string is empty
    if encrypted_string.strip() == "":
        print("Empty encrypted string.")
        exit(0)

    else:
        # Taking input for vigenere key
        # Checking for invalid vigenere key and exit the program, if true
        if key == "":
            print("Invalid vigenère key.")
            exit(0)

        else:
            # Decoding each letter of the encrypted string
            for i in range(len(encrypted_string)):
                if encrypted_string[i] == " ":
                    continue
                else:
                    """Formula used here is Decrypted Text = (Encrypted Text - Vigenere key + 26) % 26.

                    The chr() function is used to get the character from the ASCII value and 65 is added since
                    ASCII of capital letters begins at 65.

                    The ord() function is used to get the ASCII value of a particular character."""

                    decrypted_string += chr((ord(encrypted_string[i]) - ord(key[index]) + 26) % 26 + 65)

                    """Updating the pointer in the vigenere key to ensure proper decryption happens even when the key is 
                    smaller than the encrypted string.
                    """
                    index = (index + 1) % len(key)
    return decrypted_string


def decrypt_cypher(encrypted_text, key):
    # If the given key is numeric, use the caesar_cipher technique
    if key.isnumeric():
        return caesar_cypher(encrypted_text, int(key))

    # If the given key is non-numeric, use the vigenere_cipher technique
    else:
        return vigenere_cipher(encrypted_text, key)


# Decrypt text
if __name__ == "__main__":
    # Display preamble
    print("DECRYPT STRING")

    # Get encrypted text
    encrypted_string = input("Input encrypted string: ")

    # Check for empty encrypted string
    if encrypted_string.strip() == "":
        print("Empty encrypted string.")
        exit(0)

    # Get decryption key
    decryption_key = input("Input key: ")

    # Invoking the decrypt_cypher function on the encrypted_string and given decryption_key
    decrypted_string = decrypt_cypher(encrypted_string, decryption_key)
    print("The decrypted string is:")
    for character in decrypted_string:
        print(character)
