print("CHECK FILENAMES")
# valid_departments = ['dep1', 'dep2', 'dep3']
valid_departments_and_files = {'dep1':['filea','fileb'],
                               'dep2':['filec','filed'],
                               'dep3':['filea','filec']
                            }
files_with_password = {'fileb':'pass1', 'filed':'pass2'}
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
    if department_name not in valid_departments_and_files.keys():
        continue

    else:
        # Take input for file name
        file_name = input("Input a filename: ")

        # Using while loop to get file name
        while not file_name:
            file_name = input("Input a filename: ")

        # Checking if the entered file name has a password
        if file_name in files_with_password:
            for i in range(3):
                print(f"{3-i} password attempts remain.")
                password = input("Input password: ").strip()

                if password == "":
                    continue

                if file_name in files_with_password and password == files_with_password.get(file_name):
                    print(f"{file_name} - is a valid filename for - {department_name}")
                    break

        # This else if block checks whether entered file names are valid or not for all files WITHOUT a password
        elif department_name in valid_departments_and_files.keys() and \
                file_name in valid_departments_and_files.get(department_name):
            print(f"{file_name} - is a valid filename for - {department_name}")

        else:
            print(f"{file_name} - *is not* a valid filename for - {department_name}")

print("GOODBYE")
