print("CAESAR CYPHER DECRYPT")

# Taking inputs for encrypted entry and shift value
encrypted_entry = int(input("Input a number from ALPHABET TABLE: "))
caesar_shift = int(input("Input a caesar shift: "))

# Calculating the decrypted entry (centre value)
decrypted_entry = (encrypted_entry - caesar_shift) % 26

# Calculating entries 2 to the left and right of the decrypted entry
left_decrypted_entry = (decrypted_entry - 2) % 26
right_decrypted_entry = (decrypted_entry + 2) % 26

print(f"\nThe decrypted entries in ALPHABET TABLE are: {left_decrypted_entry} {decrypted_entry} {right_decrypted_entry}")

