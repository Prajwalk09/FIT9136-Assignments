import data
import datetime

# WARNING!!! *DO NOT* REMOVE THIS LINE
# THIS ENSURES THAT THE CODE BELLOW ONLY RUNS WHEN YOU HIT THE GREEN `Run` BUTTON, AND NOT THE BLUE `Test` BUTTON
if "__main__" == __name__:
    # Populating all the required databases
    data.load_database('test_data.csv', 'test_active.csv', 'test_dismissed.csv')
    data.regenerate_db()

    # Displaying active reminders.
    data.print_active_reminders()

    while True:
        uinpt = input('> ')
        # Case when the user wants to dismiss a reminder.
        if 'dismiss' in uinpt:
            uinpt = int(uinpt.split(' ')[1])
            # If the id of the reminder to be dismissed is a valid reminder id.
            if 0 < uinpt and uinpt <= len(data.get_active_reminders()):
                data.dismiss_reminder(data.get_active_reminders()[uinpt - 1][0])
                data.print_active_reminders()
            # Case when the reminder id is not a valid one. (It is not present in the databse)
            else:
                print(f'{uinpt} is not a valid item from the menu.')

        # Case when user inputs remind me now.
        elif 'remind me now' in uinpt:
            uinpt = uinpt.split()[3:]
            uinpt = ' '.join(uinpt)

            # Setting reminder and displaying active reminders
            data.set_reminder(uinpt)
            data.print_active_reminders()

        # Case when user inputs remind at
        elif 'remind at' in uinpt:
            uinpt = uinpt.split()[2:]
            active_from = " ".join(uinpt[0:2]).strip("''")
            reminder_text = " ".join(uinpt[2:])

            # Setting reminder and displaying active reminders
            data.set_reminder(reminder_text, active_from)
            data.print_active_reminders()

        # Case to display future reminders
        elif uinpt == 'future reminders':
            data.print_future_reminders()

        # Case to display past reminders
        elif uinpt == 'past reminders':
            data.print_past_reminders()

        # Case when the user wants to renew a particular reminder
        elif 'renew' in uinpt:
            uinpt = uinpt.split()
            rem_id = int(uinpt[1])

            """If the user input is 0 or out of the range from 1 to length of reminders_active_database, then this
            block is executed."""
            if abs(rem_id) == 0 or rem_id > len(data.reminders_active_database):
                print(f'{rem_id} is not a valid item from the menu.')
                continue

            # If the user wants to renew an active reminder.
            if rem_id > 0:
                time = " ".join(uinpt[3:])
                time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
                # Renewing the active reminder and displaying the active reminders.
                data.renew_reminder(rem_id - 1, time)
                data.print_active_reminders()

            # If the user wants to renew a past reminder.
            if rem_id < 0:
                rem_id = abs(rem_id)
                # Getting the actual reminder id as per database.
                rem_id = data.get_past_reminders()[rem_id - 1][0]
                time = " ".join(uinpt[3:])
                time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')

                # Renewing the past reminder and displaying the active reminders.
                data.renew_reminder(rem_id, time)
                data.print_active_reminders()

        elif uinpt == 'quit':
            print('goodbye')
            break

        else:
            continue


