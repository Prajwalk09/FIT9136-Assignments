print("CHECK FILENAMES")
valid_departments = ['dep1', 'dep2', 'dep3']
# Use a while loop to get user input until the user enters "quit"
while True:
    # Take input for department name
    department_name = input("Input a department (or quit to exit): ")

    # Using while loop to repeatedly take input for department name (if "" was entered earlier)
    while not department_name:
        department_name = input("Input a department (or quit to exit): ")

    if department_name == 'quit':
        break

    # Checking if department name is valid
    if department_name not in valid_departments:
        continue

    else:
        # Take input for file name
        file_name = input("Input a filename: ")

        # Using while loop to get file name
        while not file_name:
            file_name = input("Input a filename: ")

        # Checking if the file name is valid for the corresponding department name
        if ((department_name == 'dep1' and file_name in ['filea', 'fileb'])
                or (department_name == 'dep2' and file_name in ['filec'])
                or (department_name == 'dep3' and file_name in ['filea', 'filec'])):

            print(f"{file_name} - is a valid filename for - {department_name}")

        else:
            print(f"{file_name} - *is not* a valid filename for - {department_name}")

print("GOODBYE")


















