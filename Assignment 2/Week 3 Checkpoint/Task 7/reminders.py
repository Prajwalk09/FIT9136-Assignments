import data
import datetime

# WARNING!!! *DO NOT* REMOVE THIS LINE
# THIS ENSURES THAT THE CODE BELLOW ONLY RUNS WHEN YOU HIT THE GREEN `Run` BUTTON, AND NOT THE BLUE `Test` BUTTON
if "__main__" == __name__:
    # Loading the database from the test_data.csv file
    reminders_database = data.load_database('test_data.csv')

    # Displaying active reminders
    data.print_active_reminders()

    while True:
        uinpt = input('> ')
        # Case when user wants to dismiss a reminder.
        if 'dismiss' in uinpt:
            uinpt = int(uinpt.split(' ')[1])
            if 0 < uinpt and uinpt <= len(data.get_active_reminders()):
                data.dismiss_reminder(data.get_active_reminders()[uinpt - 1][0])
                data.print_active_reminders()
            # If the reminder id given by the user is invalid.
            else:
                print(f'{uinpt} is not a valid item from the menu.')

        # Case when the user inputs remind me now
        elif 'remind me now' in uinpt:
            uinpt = uinpt.split()[3:]
            uinpt = ' '.join(uinpt)
            data.set_reminder(uinpt)
            data.print_active_reminders()

        # Case when the user inputs remind at
        elif 'remind at' in uinpt:
            uinpt = uinpt.split()[2:]
            active_from = " ".join(uinpt[0:2]).strip("''")
            reminder_text = " ".join(uinpt[2:])
            data.set_reminder(reminder_text, active_from)
            data.print_active_reminders()

        # Case when the user inputs future reminders
        elif uinpt == 'future reminders':
            data.print_future_reminders()

        # Case when the user inputs past reminders
        elif uinpt == 'past reminders':
            data.print_past_reminders()

        # Case when the user wants to quit
        elif uinpt == 'quit':
            print('goodbye')
            break

        else:
            continue





