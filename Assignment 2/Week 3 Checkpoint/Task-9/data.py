import csv
import datetime

now = datetime.datetime(2025, 4, 7, 10, 0, 0)
reminders_database = None
reminders_active_database = None
reminders_dismissed_database = None

"""We define a new variable to restore the database format as per task 7 so that we can apply similar 
functions like the ones in task 7 :)"""
regen_db = None


def load_database(reminders_file: str, active_file: str, dismissed_file: str):
    """
        This function takes the file names mentioned in the reminders_file, active_file and dismissed_file and
        loads them into reminders_database, reminders_active_database and reminders_dismissed_database respectively.
        This function is used to create and populate the required databases.

        Parameters:
            reminders_file(str): A string value representing the name of the file from which data has to be read and fed into
                                 the reminders_database variable
            active_file(str): A string value representing the name of the file from which data has to be read and fed into
                              the reminders_active_database variable
            dismissed_file(str): A string value representing the name of the file from which data has to be read and fed into
                                 the reminders_dismissed_database file

        Returns:
            This function does not return anything. It just reads the files from the respective files and populates the
            corresponding databases.
        """
    # Referencing the global variables
    global reminders_database, reminders_active_database, reminders_dismissed_database
    reminders_database = []
    reminders_active_database = []
    reminders_dismissed_database = []

    # Populating the reminders_database
    with open(reminders_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            reminders_database.append([int(row[0]), row[1]])

    # Populating the reminders_active_database
    with open(active_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            reminders_active_database.append([int(row[0]), int(row[1]), datetime.datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S')])

    # Populating the reminders_dismissed_database
    with open(dismissed_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            reminders_dismissed_database.append([int(row[0]), int(row[1]), datetime.datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S')])


def sort_by_datetime(database: list):
    """
    This function takes a nested_list (reminders_active or reminders_dismissed) and sorts it based on the datetime field
    in descending order and returns the sorted nested list.

    Parameters:
        database (str): A string value which represents the name of the nested_list which has to be sorted. The possible
                        values are reminders_active or reminders_dismissed.

    Returns:
          This function returns a sorted nested list
    """
    # sorts the active and dismissed reminders by datetime
    return sorted(database, key=lambda x: x[2], reverse=True)


def sort_by_rem_id(database: str):
    """
        This function takes a nested_list and sorts it based on the reminder_id
        in ascending order and returns the sorted nested list.

        Parameters:
            database (str): A string value which represents the name of the nested_list which has to be sorted.

        Returns:
              This function returns a sorted nested list
        """
    # sorts the active and dismissed reminders by datetime
    return sorted(database, key=lambda x: x[0])


def find_latest_entry(database: str, rem_id: int):
    """
    This function finds the latest entry for a particular reminder id from the database variable. The database is a
    nested list.

    Parameters:
        database (str): A string value which represents the name of the nested_list.
        rem_id (int): An integer value whose latest entry has to be retrieved from the database variable.

    Return:
        This function returns the latest entry for a particular reminder id from the database variable. If the reminder
        id is not present at all in the database variable, the function returns None.
    """
    # Finds the latest entry for the specified id in the active and dismissed db
    for entry in database:
        if entry[1] == rem_id:
            return entry[2]
    return None


def regenerate_db():
    """
    This is a helper function which we have created to update the active_from and dismissed_at values to reflect
    the latest active_from and dismissed_at values, if there are any changes made by the user.

    (regen_db in this code is analogous to reminders_database in task 7)

    Parameters:
        This function does not take any inputs. It just populates a database which has a format as per task 7.

    Returns:
        This function does not return anything.
    """
    # Referencing global variables
    global regen_db, reminders_active_database, reminders_dismissed_database

    regen_db = []

    # Sorting the reminders_active_database and reminders_dismissed_database by the date_time
    reminders_active_database = sort_by_datetime(reminders_active_database)
    reminders_dismissed_database = sort_by_datetime(reminders_dismissed_database)

    # Populating the required database(regen_db)
    for entry in reminders_database:
        entry3 = find_latest_entry(reminders_active_database, entry[0])
        entry4 = find_latest_entry(reminders_dismissed_database, entry[0])
        regen_db.append([entry[0], entry[1], entry3, entry4])


def get_active_reminders() -> list:
    """
    This function is used to get a list of all the reminders in the regenerated database (regen_db) that are currently
    active. A reminder is considered "active" if it's active_from field is more recent than its dismissed_at field,
    and active_from has already passed relative to now.

    Parameters:
         This function takes no parameters

    Returns:
        This function returns a list of all the reminders that are currently active.
    """
    global regen_db
    active_reminders = []
    for i in range(len(regen_db)):
        if regen_db[i][3] != None:
            if regen_db[i][2] > regen_db[i][3] and regen_db[i][2] <= now:
                active_reminders.append(regen_db[i])
        else:
            if regen_db[i][2] <= now:
                active_reminders.append(regen_db[i])
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
    active_reminders = get_active_reminders()
    print('ACTIVE REMINDERS')
    count = 1
    for i in range(len(active_reminders)):
        print(f'{count}. {active_reminders[i][1]}')
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
    global regen_db
    past_reminders = []
    for i in range(len(regen_db)):
        if regen_db[i][3] != None:
            if regen_db[i][3] >= regen_db[i][2] and regen_db[i][3] <= now and regen_db[i][2] <= now:
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
        if i == 0:
            print(f'{count}. {past_reminders[i][1]}')
            count -= 1
            continue
        if past_reminders[i] == past_reminders[i-1]:
            continue
        else:
            print(f'{count}. {past_reminders[i][1]}')
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
    global regen_db
    future_reminders = []
    for i in range(len(regen_db)):
        if regen_db[i][2] > now:
            future_reminders.append(regen_db[i])
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
    count = len(get_active_reminders()) + 1
    future_reminders = get_future_reminders()
    print('FUTURE REMINDERS')
    for i in range(len(future_reminders)):
        if i == 0:
            print(f'{count}. {future_reminders[i][1]}')
            count += 1
            continue
        if future_reminders[i][1] == future_reminders[i-1][1]:
            continue
        else:
            print(f'{count}. {future_reminders[i][1]}')
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
    global reminders_database, reminders_active_database, regen_db
    rem_id = len(reminders_database)
    active_count = len(reminders_active_database)
    if active_from == now:
        regen_db.append([rem_id, reminder_text, active_from, None])
        reminders_database.append([rem_id, reminder_text])
        reminders_active_database.append([active_count, rem_id, active_from])
    else:
        regen_db.append([rem_id, reminder_text, datetime.datetime.strptime(active_from, '%Y-%m-%d %H:%M:%S'), None])
        reminders_database.append([rem_id, reminder_text])
        reminders_active_database.append([active_count, rem_id, active_from])


def dismiss_reminder(reminder_id):
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
    global reminders_database, regen_db, reminders_dismissed_database
    dismiss_count = len(reminders_dismissed_database)
    for i in range(len(regen_db)):
        if regen_db[reminder_id][3] != None:
            if not(regen_db[reminder_id][3] >= regen_db[reminder_id][2] and regen_db[reminder_id][3] < now and regen_db[reminder_id][2] < now):
                regen_db[reminder_id][3] = now
                reminders_dismissed_database.append([dismiss_count, reminder_id, now])
        else:
            regen_db[reminder_id][3] = now
            reminders_dismissed_database.append([dismiss_count, reminder_id, now])


def renew_reminder(rem_id: int, active_from):
    """
    This function is used to renew a reminder. It takes the reminder id and active from as inputs and makes changes
    to the regen_db variable which was defined earlier and the reminders_active database.

    Parameters:
        rem_id(int): The id of the reminder which has to be renewed.
        active_from (datetime): A datetime value which signifies from when the reminder specified by the rem_id has to
                                be active from.

    Returns:
        This function does not return anything. It just updates the regen_db and reminders_active database.
    """
    global regen_db, reminders_active_database
    for i in range(len(regen_db)):
        # If reminder id is found.
        if regen_db[i][0] == rem_id:
            # If dismissed_at is None
            if regen_db[i][3] == None:
                regen_db.append([rem_id, regen_db[i][1], active_from, None])
            else:
                regen_db.append([rem_id, regen_db[i][1], active_from, regen_db[i][3]])
            reminders_active_database.append([len(reminders_active_database), rem_id, active_from])
    # Sorting the regen_db by reminder_id again to aid in printing the reminders at a later point.
    regen_db = sort_by_rem_id(regen_db)


def dump_database(database_file: str):
    """
    This function gets all existing reminders (past + active + future) and writes to an output file.

    Parameters:
        database_file(str): The name of the CSV file to which all the existing reminders have to be written.

    Returns:
        This function does not return anything.
    """
    active_reminders = get_active_reminders()
    past_reminders = get_past_reminders()
    future_reminders = get_future_reminders()
    active_ids = []
    # Opening the file to write to it.
    with open(database_file, 'w') as fileref:
        # If there are any active reminders, execute this block.
        if active_reminders:
            # Write all the active reminders to the file.
            for i in range(len(active_reminders)):
                if active_reminders[i][3] == None:
                    active_reminders[i][3] = datetime.datetime.fromtimestamp(0)
                fileref.write(str(active_reminders[i][0]) + ',' + str(active_reminders[i][1]) + ',' + str(active_reminders[i][2]) + ',' + str(active_reminders[i][3]))
                active_ids.append(active_reminders[i][0])
                fileref.write('\n')

        # If there are any past reminders, execute this block.
        if past_reminders:
            # Write all the past reminders.
            for i in range(len(past_reminders)):
              fileref.write(str(past_reminders[i][0]) + ',' + str(past_reminders[i][1]) + ',' + str(past_reminders[i][2]) + ',' + str(past_reminders[i][3]))
              fileref.write('\n')

        # If there are any future reminders, execute this block
        if future_reminders:
            # Write all the future reminders.
            for i in range(len(future_reminders)):
                if future_reminders[i][0] in active_ids:
                    continue
                fileref.write(str(future_reminders[i][0]) + ',' + str(future_reminders[i][1]) + ',' + str(future_reminders[i][2]) + ',' + str(future_reminders[i][3]))
                fileref.write('\n')
