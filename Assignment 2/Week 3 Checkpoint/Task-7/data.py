import csv
import datetime

# Defining the now variable and initialising the reminders_database list
now = datetime.datetime(2025, 4, 7, 10, 0, 0)
reminders_database = []


def load_database(reminders_file: str) -> list:
    """
    This function takes a file name mentioned in the reminders_file parameter, opens the file and reads the content
    of the file as CSV data and stores the loaded reminders in reminders_database variable.

    Parameters:
        reminders_file (str): A variable of type string which contains the name of the CSV file from which the
        data has to be read.

    Returns:
        This function returns a list called reminders_database containing the loaded reminders from the CSV file
        which was read earlier.
    """

    # Using global keyword to access the reminders_database global_variable
    global reminders_database

    # Opening the file
    with open(reminders_file, 'r') as input_file:
        # Reading data from file and removing headers
        reminders_database = input_file.readlines()
        reminders_database = reminders_database[1:]

        # Iterating through the outer list.
        for i in range(len(reminders_database)):
            # Getting rid of \n character and splitting the values using ',' as delimiter
            reminders_database[i] = reminders_database[i].strip().split(',')

            # Iterating inside/through each reminder
            for j in range(len(reminders_database[i])):
                # Getting rid of "" character associated with each item in the reminder.
                reminders_database[i][j] = reminders_database[i][j].strip('""')

            # Converting reminder_id to int and active_from, dismissed_at to type datetime
            reminders_database[i][0] = int(reminders_database[i][0])
            reminders_database[i][2] = datetime.datetime.strptime(reminders_database[i][2], '%Y-%m-%d %H:%M:%S')
            reminders_database[i][3] = datetime.datetime.strptime(reminders_database[i][3], '%Y-%m-%d %H:%M:%S')
        return reminders_database


def get_active_reminders() -> list:
    """
    This function is used to get a list of all the reminders in the database that are currently active. A reminder is
    considered "active" if it's active_from field is more recent than its dismissed_at field, and active_from has
    already passed relative to now.

    Parameters:
         This function takes no parameters

    Returns:
        This function returns a list of all the reminders that are currently active.
    """
    global reminders_database
    active_reminders = []
    for i in range(len(reminders_database)):
        active_from, dismissed_at = reminders_database[i][2:]

        # Checking whether a reminder is active using the conditions mentioned
        if dismissed_at < active_from <= now:
            active_reminders.append(reminders_database[i])
    return active_reminders


def print_active_reminders():
    """
    This function is used to print all the reminders that are currently active. This function does not take any
    parameters, it only displays the reminders which are currently active. A reminder is
    considered "active" if it's active_from field is more recent than its dismissed_at field, and active_from has
    already passed relative to now.

    Parameters:
        This function does not take any parameters at all. It just displays all the reminders that are currently active.

    Returns:
          The function does not return anything. It only prints the reminders that are currently active.
    """
    print('ACTIVE REMINDERS')
    count = 1
    active_reminders = get_active_reminders()
    for i in range(len(active_reminders)):
        print(f"{count}. {active_reminders[i][1]}")
        count += 1


def get_past_reminders() -> list:
    """
    This function is used to get a list of all the reminders which are "past" in the database. A reminder is
    considered "past" if it's dismissed_at field is equal to or more recent than its active_from field, and both the
    active_from and dismissed_at fields have already passed relative to now.

    Parameters:
         This function does not take any parameters. It just displays all the reminders that belong to past reminders/

    Returns:
        This function returns a list of all the reminders which are "past" in the database.
    """
    global reminders_database
    past_reminders = []
    for i in range(len(reminders_database)):
        active_from, dismissed_at = reminders_database[i][2:]
        # Specifying the condition for a reminder to be "past" in the database.
        if (dismissed_at >= active_from) and dismissed_at <= now and active_from <= now:
            past_reminders.append(reminders_database[i])
    return past_reminders


def print_past_reminders():
    """
    This function prints all the past reminders depending on the condition for a reminder to be in the past. A
    reminder is considered "past" if it's dismissed_at field is equal to or more recent than its active_from field,
    and both the active_from and dismissed_at fields have already passed relative to now.

    Parameters:
        This function does not take any parameters. It only prints the reminders that satisfy the condition of "past"
        reminders.

    Returns:
        This function does not return anything.
    """
    count = -1
    past_reminders = get_past_reminders()
    print('PAST REMINDERS')
    for i in range(len(past_reminders)):
        print(f"{count}. {past_reminders[i][1]}")
        count -= 1


def get_future_reminders() -> list:
    """
    This function is used to get a list of all the reminders which will become "active" in the future. A reminder is
    considered "future" if it's active_from field is in the future relative to now.

    Parameters:
        This function does not take any parameters. It just uses the reminders_database global variable to
        perform its task.

    Returns:
        This function returns a list of all the reminders which will become "active" in the future
    """
    global reminders_database
    future_reminders = []
    for i in range(len(reminders_database)):
        active_from = reminders_database[i][2]

        # Specifying the condition for a reminder to be considered as active
        if active_from > now:
            future_reminders.append(reminders_database[i])
    return future_reminders


def print_future_reminders():
    """
    This function is used to print all the reminders that are currently active. A reminder is
    considered "future" if it's active_from field is in the future relative to now.

    Parameters:
        This function does not take any parameters.

    Returns:
        This function does not return anything. It only prints the future reminders.
    """
    # The future reminders count starts one after the number of active reminders.
    count = len(get_active_reminders()) + 1
    future_reminders = get_future_reminders()
    print('FUTURE REMINDERS')
    for i in range(len(future_reminders)):
        print(f"{count}. {future_reminders[i][1]}")
        count += 1


def set_reminder(reminder_text: str, active_from=now):
    """
    This function is used to set a particular reminder. It takes the reminder text and active_from datetime as inputs
    and appends them as a new reminder to the reminders_database variable.

    Parameters:
        reminder_text(str): A string value which represents the text to be present in the reminder
        active_from(datetime): A datetime value which represents the datetime from which the reminder will be active.
                               The default value for this will be the now variable.

    Returns:
        This function does not return anything.
    """
    global reminders_database
    count = len(reminders_database)
    # Executes this block if the user input is remind me now
    if active_from == now:
        reminders_database.append([count, reminder_text, active_from, datetime.datetime.fromtimestamp(0)])
    # Executes this block if the user input is remind at
    else:
        reminders_database.append([count, reminder_text, datetime.datetime.strptime(active_from, '%Y-%m-%d %H:%M:%S'),
                                   datetime.datetime.fromtimestamp(0)])


def dismiss_reminder(reminder_id: int):
    """
    This function is used to dismiss a reminder whose ID is given as an input to this function.  It dismisses the
    identified reminder. If reminder_id is not found in the database or if the reminder identified
    is currently "past", nothing is changed. Otherwise, the dismissed_at value for the reminder is set to now.

    Parameters:
        reminder_id (int): This function takes an integer value which corresponds to the ID of the reminder to be
                           dismissed from the reminders_database.

    Returns:
        This function does not return anything. It either deletes the reminder or updates the dismissed_at value
        for the reminder, depending on the condition mentioned above.
    """
    global reminders_database
    active_from, dismissed_at = reminders_database[reminder_id][2:]
    # Making changes only when the reminder id is found in the database and the reminder is not currently in the past.
    if reminder_id < len(reminders_database) and not (active_from <= dismissed_at < now and active_from < now):
        reminders_database[reminder_id][3] = now

