print("CHECK FILENAMES")

# Defining valid file names
valid_file_names = ['filea', 'fileb', 'filec', 'filed', 'filee']
# Use a while loop to get user input until the user enters "quit"
while True:
    file_name = input("Input a filename (or quit to exit): ")

    # If input is "quit", exit the loop.
    if file_name.lower() == 'quit':
        break

    # Check if given file name is valid.
    elif file_name in valid_file_names :
        print(f"{file_name} - is a valid filename.")

    # Displaying invalid file names.
    else:
        print(f"{file_name} - *is not* a valid filename.")

print("GOODBYE")

