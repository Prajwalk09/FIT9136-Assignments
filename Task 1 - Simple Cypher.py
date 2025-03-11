print("CAESAR CYPHER DECRYPT")

# Taking inputs for encrypted entry and shift value
encrypted_entry = int(input("Input a number from ALPHABET TABLE: "))
caesar_shift = int(input("Input a caesar shift: "))

# Calculating the decrypted entry (required output)
decrypted_entry = (encrypted_entry - caesar_shift) % 26

print(f"\nThe decrypted entry in ALPHABET TABLE is: {decrypted_entry}")
