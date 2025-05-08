import data
import datetime

# WARNING!!! *DO NOT* REMOVE THIS LINE
# THIS ENSURES THAT THE CODE BELLOW ONLY RUNS WHEN YOU HIT THE GREEN `Run` BUTTON, AND NOT THE BLUE `Test` BUTTON
if "__main__" == __name__:
    data.load_database('test_data.csv', 'test_active.csv', 'test_dismissed.csv')
    data.regenerate_db()
    #active_reminders = data.get_active_reminders()
    #past_reminders = data.get_past_reminders()
    #future_reminders = data.get_future_reminders()
    #count = data.print_active_reminders(active_reminders)
    data.print_active_reminders()
    #print(reminders_database)
    #print(active_reminders)
    while True:
        uinpt = input('> ')
        if 'dismiss' in uinpt:
            uinpt = int(uinpt.split(' ')[1])
            #print(uinpt)
            if 0 < uinpt  and  uinpt <= len(data.get_active_reminders()):
                #print('here')
                data.dismiss_reminder(uinpt - 1)
                data.print_active_reminders()
                #print(data.regen_db)
                #del reminders_database[uinpt]
                #print(reminders_database)
                #active_reminders = data.get_active_reminders()
                #count = data.print_active_reminders(active_reminders)
            else:
                print(f'{uinpt} is not a valid item from the menu.')
        
        elif 'remind me now' in uinpt:
            uinpt = uinpt.split()[3:]
            uinpt = ' '.join(uinpt)
            data.set_reminder(uinpt)
            #active_reminders = data.get_active_reminders()
            #count = data.print_active_reminders(active_reminders)
            data.print_active_reminders()
            #print(active_reminders)
            #print(reminders_database)

        elif 'remind at' in uinpt:
            uinpt = uinpt.split()[2:]
            active_from = " ".join(uinpt[0:2]).strip("''")
            reminder_text = " ".join(uinpt[2:])
            data.set_reminder(reminder_text, active_from)
            #print(reminders_database)
            #active_reminders = data.get_active_reminders()
            #count = data.print_active_reminders(active_reminders)
            data.print_active_reminders()

        elif uinpt == 'future reminders':
            #count = data.get_active_count(active_reminders)
            #count = data.print_future_reminders(future_reminders, count)
            data.print_future_reminders()
            #data.print_active_reminders()

        elif uinpt == 'past reminders':
            #past_reminders = data.get_past_reminders()
            #data.print_past_reminders(past_reminders, count_rev)
            data.print_past_reminders()
            #data.print_active_reminders()

        elif 'renew' in uinpt:
            uinpt = uinpt.split()
            #print(uinpt)
            rem_id = int(uinpt[1][1])
            #print(rem_id)
            #data.dismiss_reminder(0)
            rem_id = data.get_past_reminders()[rem_id - 1][0]
            #print(rem_id)
            #time1 = uinpt[3].split('-')
            #time1 = [int(item) for item in time1]
            #print(time1)
            #time2 = uinpt[4].split(':')
            #time2 = [int(item) for item in time2]
            #print(time2)
            #time = datetime.datetime(time1[0],time1[1],time1[2],time2[0], time2[1], time2[2])
            #print(time)
            time = " ".join(uinpt[3:])
            time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
            #time = datetime.datetime.fromisoformat(' '.join(uinpt[3:]))
            #print(time)
            data.renew_reminder(rem_id, time)
            data.print_active_reminders()
            print(data.regen_db)
            
        
        elif uinpt == 'quit':
            print('goodbye')
            break

        else:
            continue
    
    
