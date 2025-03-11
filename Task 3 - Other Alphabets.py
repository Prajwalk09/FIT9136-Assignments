print("CAESAR CYPHER DECRYPT")

alphabet_size = int(input("Input size of the alphabet: "))

# Taking inputs for encrypted entry and shift value
encrypted_entry = int(input("Input a number from ALPHABET TABLE: "))
caesar_shift = int(input("Input a caesar shift: "))

# Calculating the decrypted entry (centre value)
decrypted_entry = (encrypted_entry - caesar_shift) % alphabet_size

# Calculating entries 2 to the left and right of the decrypted entry
left_decrypted_entry = (decrypted_entry - 2) % alphabet_size
right_decrypted_entry = (decrypted_entry + 2) % alphabet_size

print(f"\nThe decrypted entries in ALPHABET TABLE are: {left_decrypted_entry} {decrypted_entry} {right_decrypted_entry}")

