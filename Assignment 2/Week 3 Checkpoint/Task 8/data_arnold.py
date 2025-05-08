import csv
import datetime

now = datetime.datetime(2025, 4, 7, 10, 0, 0)
reminders_database = None
reminders_active_database = None
reminders_dismissed_database = None

#Defined by me
#active_reminders = []
past_reminders = []
#future_reminders = []
regen_db = None


def load_database(reminders_file, active_file, dismissed_file):
    global reminders_database, reminders_active_database, reminders_dismissed_database
    reminders_database = []
    reminders_active_database = []
    reminders_dismissed_database = []

    with open(reminders_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            reminders_database.append([int(row[0]), row[1]])

    with open(active_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            reminders_active_database.append([int(row[0]), int(row[1]), datetime.datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S')])

    with open(dismissed_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            reminders_dismissed_database.append([int(row[0]), int(row[1]), datetime.datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S')])

def sort_by_datetime(database):
    # sorts the active and dismissed reminders by datetime
    return sorted(database, key=lambda x: x[2], reverse=True)

def find_latest_entry(database, rem_id):
    # finds the latest entry for the specified id in the active and dismissed db
    for entry in database:
        if entry[1] == rem_id:
            return entry[2]
    return None

def regenerate_db():
    global regen_db, reminders_active_database, reminders_dismissed_database
    regen_db = []
    reminders_active_database = sort_by_datetime(reminders_active_database)
    reminders_dismissed_database = sort_by_datetime(reminders_dismissed_database)
    for entry in reminders_database:
        entry3 = find_latest_entry(reminders_active_database, entry[0])
        entry4 = find_latest_entry(reminders_dismissed_database, entry[0])
        regen_db.append([entry[0], entry[1], entry3, entry4])

def get_active_reminders():
    global regen_db
    active_reminders = []
    for i in range(len(regen_db)):
        if regen_db[i][3] != None: 
            if regen_db[i][2] > regen_db[i][3] and regen_db[i][2] <= now:
                active_reminders.append(regen_db[i])
        else:
            if regen_db[i][2] <= now:
                active_reminders.append(regen_db[i])
            #active_reminders.append([count, reminders_database[i][1]])
    return active_reminders

def print_active_reminders():
    active_reminders = get_active_reminders()
    print('ACTIVE REMINDERS')
    count = 1
    for i in range(len(active_reminders)):
        print(f'{count}. {active_reminders[i][1]}')
        count += 1
    return count


def get_past_reminders():
    global regen_db
    #past_reminders = []
    for i in range(len(regen_db)):
        if regen_db[i][3] != None:
            if regen_db[i][3] >= regen_db[i][2] and regen_db[i][3] <= now and regen_db[i][2] <= now:
                past_reminders.append(reminders_database[i])
    return past_reminders

def print_past_reminders():
    count = -1
    past_reminders = get_past_reminders()
    print('PAST REMINDERS')
    for i in range(len(past_reminders)):
        print(f'{count}. {past_reminders[i][1]}')
        count -= 1

def get_future_reminders():
    global regen_db
    future_reminders = []
    for i in range(len(regen_db)):
        if regen_db[i][2] > now:
            future_reminders.append(regen_db[i])
    return future_reminders

def print_future_reminders():
    count = len(get_active_reminders()) + 1
    future_reminders = get_future_reminders()
    print('FUTURE REMINDERS')
    for i in range(len(future_reminders)):
        print(f'{count}. {future_reminders[i][1]}')
        count += 1
    return count

def set_reminder(reminder_text, active_from=now):
    global reminders_database, reminders_active_database, regen_db
    rem_id = len(reminders_database)
    active_count = len(reminders_active_database)
    if active_from == now:
        regen_db.append([rem_id, reminder_text, active_from, None])
        reminders_database.append([rem_id, reminder_text])
        reminders_active_database.append([active_count, rem_id, active_from])
    else:
        regen_db.append([count, reminder_text, datetime.datetime.strptime(active_from, '%Y-%m-%d %H:%M:%S'), None])
        reminders_database.append([rem_id, reminder_text])
        reminders_active_database.append([active_count, rem_id, active_from])
    #rem_active_from.append(active_from)
    #rem_dismissed_at.append(datetime.datetime.strftime(datetime.datetime.fromtimestamp(0), '%Y-%m-%d %H:%M:%S'))

def dismiss_reminder(reminder_id):
    global reminders_database, regen_db, reminders_dismissed_database
    dismiss_count = len(reminders_dismissed_database)
    if reminder_id < len(reminders_database):
        if regen_db[reminder_id][3] != None:
            if not(regen_db[reminder_id][3] >= regen_db[reminder_id][2] and regen_db[reminder_id][3] < now and regen_db[reminder_id][2] < now):
                regen_db[reminder_id][3] = now
                reminders_dismissed_database.append([dismiss_count, reminder_id, now])
        else:
            regen_db[reminder_id][3] = now
            reminders_dismissed_database.append([dismiss_count, reminder_id, now])


def renew_reminder(rem_id, active_from):
    global regen_db, reminders_active_database
    for i in range(len(regen_db)):
        if regen_db[i][0] == rem_id:
            print('here')
            #regen_db.append([len(regen_db), regen_db[i][1], active_from, None])
            regen_db[i][2] = active_from
            regen_db[i][3] = None
            reminders_active_database.append([len(reminders_active_database), rem_id, active_from])



