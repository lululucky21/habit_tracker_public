""" file for analyzation logic """

from datetime import datetime, timedelta
import interface
from operator import attrgetter

# create habit list for tabulate 
# attribute can be passed in for sorting regarding this value
# descending = reverse parameter for sorting ascending (False) or descending (True)
def habit_list_creator(attribute='id', descending=False):
    habits = interface.get_habits()
    name = ["Habit Name:"]
    start_time = ["Start Time:"]
    daily_cost = ["Daily Cost:"]
    total_cost = ["Total Cost:"]
    time_wasted = ["Time Wasted:"]
    total_time_cost = ["Total Time Cost:"]
    goal = ["General Goal:"]
    days_remaining = ["Days Remaining:"]
    daily_iter = ["Daily Iterations:"]
    checkout = ["Checkout:"]
    last_checkout = ["Last Checkout:"]
    longest_streak = ["Longest Streak:"]
    date_broken = ["Last Time Broken:"]
    broken_counter = ["Times Broken:"]

    s_habits = sorted(habits, key=attrgetter(attribute), reverse=descending)
    for habit in s_habits:
        name.append(habit.name)
        start_time.append(habit.start_time)
        daily_cost.append(habit.daily_cost)
        total_cost.append(habit.total_cost)
        time_wasted.append(habit.time_wasted)
        total_time_cost.append(habit.total_time_cost)
        goal.append(habit.general_goal)
        days_remaining.append(habit.days_remaining)
        daily_iter.append(habit.daily_iter)
        checkout.append(habit.checkout_counter)
        last_checkout.append(habit.last_checkout_time)
        longest_streak.append(habit.longest_streak)
        date_broken.append(habit.date_broken)
        broken_counter.append(habit.broken_counter)

    sorted_list = [
        name, start_time, daily_cost, total_cost, time_wasted, 
        total_time_cost, goal, days_remaining, daily_iter, checkout, 
        last_checkout, longest_streak, date_broken, broken_counter
        ]
    return sorted_list

# goal calculation ------->>>>>>>> sollte so mit neuen Variablen funktionieren!
def calculate_goal():
    habits = interface.get_habits()
    names = []
    general_goal = []
    daily_iter = []
    checkout_counter = []

    for habit in habits:
        names.append(habit.name)
        general_goal.append(habit.general_goal)
        daily_iter.append(habit.daily_iter)
        checkout_counter.append(habit.checkout_counter)

    new_goal = [x-z/y if z != 0 else x for (x,y,z) in zip(general_goal, daily_iter, checkout_counter)]

    for x,y in zip(new_goal, names):
        interface.change_attribute(y, 'days_remaining', x)

    return names, new_goal 

# total time wasted calculation   --->>> testen ob total_checkout funktioniert!!!
def calculate_total_time_cost():
    habits = interface.get_habits()
    names = []
    time_wasted = []
    total_checkout = []

    for habit in habits:
        names.append(habit.name)
        time_wasted.append(habit.time_wasted)
        total_checkout.append(habit.total_checkout)

    total_time_cost = [x*y for (x,y) in zip(time_wasted, total_checkout)]
    round_ttc = [round(val, 2) for val in total_time_cost]
    
    for x,y in zip(round_ttc, names):
        interface.change_attribute(y, 'total_time_cost', x)  

# total cost calculation --->>> testen ob total_checkout funktioniert!!!
def calculate_cost():
    habits = interface.get_habits()
    
    names = []
    daily_cost = []
    daily_iter = []
    total_checkout = []

    for habit in habits:
        names.append(habit.name)
        daily_cost.append(habit.daily_cost)
        daily_iter.append(habit.daily_iter)
        total_checkout.append(habit.total_checkout)
    
    total_cost = [x*(z/y) for (x,y,z) in zip(daily_cost, daily_iter, total_checkout)]
    
    for x,y in zip(total_cost, names):
        interface.change_attribute(y, 'total_cost', x)  

# calculate checkout state for habits ------>>>> überprüfen, braucht jetzt andere Logik, da Habits weiterlaufen können, auch wenn gebrochen, geht das auf Basis von days remaining? done, testen
# ginge auch über letztes Datum von Habit gebrochen! Schauen und variante wählen
def calculate_checkout_state():
    habits = interface.get_habits()
    names = []
    #start_time = []
    days_remaining = []
    #end_date = []
    #goal = []
    
    for habit in habits:
        names.append(habit.name)
        #start_time.append(datetime.strptime(habit.start_time, '%y-%m-%d %H:%M:%S')) # die muss weg, dafür mit days remaining machen!
        days_remaining.append(habit.days_remaining)
        #goal.append(habit.general_goal)
    
    # for s, g in zip(start_time, goal):
    #     end_date.append(s + timedelta(days=g))
        
    # neue Idee für end date berechnung: sollte so funktionieren!
    end_date_test = []
    
    for d in days_remaining:
        end_date_test.append(datetime.today() + timedelta(days=d))
        
    return end_date_test, days_remaining, names
        
        
    #return end_date, days_remaining, names

# calculate current streaks for habits  ->>>>>> testen!!!! sollte so funktionieren!
def calculate_current_streaks():
    habits = interface.get_habits()
    names = []
    daily_iter = []
    checkout_counter = []

    for habit in habits:
        names.append(habit.name)
        daily_iter.append(habit.daily_iter)
        checkout_counter.append(habit.checkout_counter)
        
    streaks = [x/y for (x,y) in zip(checkout_counter, daily_iter)]
    s_streaks = sorted(streaks, reverse=True)
    
    key_dict = dict(zip(names, streaks))
    names.sort(key=key_dict.get, reverse=True)
    
    return names, s_streaks
    

# create end statics when habit finished/reached --->>>>>>>> überprüfen!!!!!!! wurde geändert!!!!!!
def statistics(habit_name):
    habit = interface.get_single_habit(habit_name)
    
    start_time = datetime.strptime(habit.start_time, '%y-%m-%d %H:%M:%S')
    start_date = datetime.strftime(start_time, '%A, %d. of %B %Y') 
    
    end_date = datetime.strptime(habit.start_time, '%y-%m-%d %H:%M:%S') + timedelta(days=habit.general_goal) 
    end_date_str = datetime.strftime(end_date, '%A, %d. of %B %Y')
    
    if habit.date_broken == "not broken":
        #streak_since = datetime.strptime(habit.start_time, '%y-%m-%d %H:%M:%S')
        #streak_since = datetime.strftime(start_time, '%A, %d. of %B %Y') 
        streak_since = datetime.strftime(datetime.strptime(habit.start_time, '%y-%m-%d %H:%M:%S'), '%A, %d. of %B %Y')     # das ausprobieren, ggf fehler, dann anpassen an oben, ansonsten obere umschreiben
    else:
        streak_since = datetime.strftime(datetime.strptime(habit.date_broken, '%y-%m-%d %H:%M:%S'), '%A, %d. of %B %Y')
    
    total_time_h = round(habit.total_time_cost / 60, 2)
  
    message =  f"""
            \n    Your habit '{habit.name}' started on {start_date} and with a goal of {habit.general_goal} days it should have ended on {end_date_str}.
            \n    You've broken your habit {habit.broken_counter} times and finished with a streak since {streak_since}. 
            \n    With a daily cost of {habit.daily_cost} Euro the total costs saved or waisted have been {habit.total_cost} Euro.
            \n    The amount of time you've spent on your habit every time was {habit.time_wasted} minutes and depending on the habit you've either saved or waisted a total of {total_time_h} hours.

                """
                
    return message

