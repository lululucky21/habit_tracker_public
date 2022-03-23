""" file for CLI """
 
import click
import interface
import logic
from tabulate import tabulate
from datetime import datetime, timedelta


@click.group()
def cli():
    pass

@cli.group()
def analyzation():
    pass

@cli.group()
def manage_habits():
    pass

@cli.group()
def actual_state():
    pass

# managing habits commands
# create and add a new habit to db
@manage_habits.command()
@click.option('--name',prompt='    type in the habit name')
@click.option('--cost',prompt='    type in the daily cost in euros')
@click.option('--time_wasted',prompt='    type in the time you waste on the habit in minutes')
@click.option('--goal',prompt='    type in the goal in days')
@click.option('--iterations',prompt='    type in the times you want to checkout the habit per day')
def create(name, cost, time_wasted, goal, iterations):
    """create and add  new habit to db"""
    start_time = datetime.strftime(datetime.now(), '%y-%m-%d %H:%M:%S')
    habit = interface.Habit(name=name, start_time=start_time, daily_cost=cost, time_wasted=time_wasted, general_goal=goal, daily_iter=iterations)
    interface.add_habit(habit)
    print(f"    The habit '{name}' has been added to the database!")

# checkout predefined habit and directly update goal, time cost and total cost >>>>>> ich glaube message ist noch nicht getestet!, sollte so passen!!!!
@manage_habits.command()
@click.option('--cli_name',prompt='    type in the name of the habit you want to checkout')
@click.option('--count', prompt='    type in the times you want to checkout the habit')
def checkout(cli_name, count):
    """checkout habit and update data"""
    count_int = int(count)
    interface.checkout_habit(cli_name, count_int)
    names, new_goal = logic.calculate_goal()
    logic.calculate_total_time_cost()
    logic.calculate_cost()

    print(f"    The habit '{cli_name}' has been checked out!")

    for goal, name in zip(new_goal, names):
        if goal == 0:
            message = logic.statistics(name)
            print(message)
            #print(f"Congratulations! Goal reached for the habit '{name}' and goal has been checked out!")      das rausnehmen, wenn alles soweit funktioniert!
        elif goal < 0:
            print(f"\n    Your habit '{name}' is already reached since {-(goal)} checkouts!\n    Please change your goal or reset habit.")

# break a habit ------>>>>>> die hier muss RICHTIG ANGEPASST werden!!!!!! --> break hinzufügen
@manage_habits.command()
@click.option('--name',prompt='    type in the name of the habit you have broken')
@click.option('--option',prompt='    type in "delete" to delete the habit or "reset" for resetting or "break" to continue')
def break_habit(name, option):
    """break habit, delete, reset or break"""
    if option == "delete" and click.confirm("    Please confirm to continue"):
        interface.delete_habit(name)
        print(f"The habit '{name}' has been deleted and is no longer available in the database!")
    elif option == "reset" and click.confirm("    Please confirm to continue"):
        interface.reset_habit(name)
        print(f"    Your habit '{name}' has been reset!")
    elif option == "break" and click.confirm("    Please confirm to continue"):
        interface.break_habit(name)
        print(f"    Your habit '{name}' has been broken! You can continue checking it out!")
    else:
        print("    Please try again!") 
        
# reset habit 
@manage_habits.command()
@click.option('--name',prompt='    type in the name of the habit you want to reset')
def reset(name):
    """reset habit""" 
    if click.confirm("    Please confirm to continue"):
        interface.reset_habit(name)
        print(f"    The habit '{name}' has been reset!")
    else:
        print(f"    The habit '{name}' has not been reset!")

# delete a habit 
@manage_habits.command()
@click.option('--name', prompt='    type in the name of the habit you want to delete')
def delete(name):
    """delete habit from db"""
    if click.confirm("    Please confirm to continue"):
        interface.delete_habit(name)
        print(f"    The habit '{name}' has been deleted and is no longer available in the database!")
    else:
        print(f"    The habit '{name}' has not been deleted!")

# changing an attribute of habit ---->>>> Anpassungen überprüfen! sollte so funktionieren!
@manage_habits.command()
@click.option('--name', prompt='    type in the name of the habit on which you want to modify an attribute'
              '\n    (you can view the current habits with the get-habit-list function)')
@click.option('--attribute', prompt='    type in the name of the attribute you want to change.' 
              '\n    (changeable attributes are "name, start_time, daily_cost, time_wasted, general_goal and daily_iter")') 
@click.option('--value', prompt='    type in the value you want to assign to the attribute')
def change_attribute(name, attribute, value):
    """change attribute of habit"""
    if attribute == "checkout_counter":
        print("Please checkout your habit within the checkout function!")
    elif attribute in [
        "total_cost", "total_time_cost", "days_remaining", "last_checkout_time", 
        "longest_streak", "date_broken", "broken_counter", "total_checkout"
        ]:
        print("You cannot change this attribute!")
    else:
        interface.change_attribute(name, attribute, value)
        print(f"    The attribute '{attribute}' of the habit '{name}' has been changed to '{value}'!")

    if attribute in ["general_goal", "daily_iter"]:
        logic.calculate_goal()
    if attribute == "time_wasted":
        logic.calculate_total_time_cost()        
    if attribute in ["daily_cost", "daily_iter"]:
        logic.calculate_cost()


# actual state commands
# get list of all habits stored in db 
@actual_state.command()
def get_all_habits():
    """show all current habits"""
    print(tabulate(logic.habit_list_creator(), headers='firstrow', tablefmt='github'))  

# get values of specific habit stored in db
@actual_state.command()
@click.option('--name', prompt='    type in the name of the habit you want to see')
def get_habit(name):
    """show a single habit"""
    attribute_list = interface.get_habit(name)
    print(tabulate(attribute_list, headers='firstrow', tablefmt='github'))
    
# calculate checkout state of each habit -----_>>>>>> sollte so hoffentlich angepasst funktionieren mit neuen Variablen, noch nicht ganz sicher, ausführlich testen!!!!
@actual_state.command()
def checkout_state():
    """calculate checkout state of each habit"""
    end_date, days_remaining, names = logic.calculate_checkout_state()
    actual_time = datetime.now()
    
    for end, remaining, name in zip(end_date, days_remaining, names):
        if end.date() - actual_time.date() < timedelta(days=remaining):
            print(f"    Please manage your checkouts for habit '{name}' or call break habit function from CLI")
        elif end.date() - actual_time.date() > timedelta(days=remaining) + timedelta(days=1):
            print(f"    You've checked out an event in the future of habit '{name}'." 
                 "\n    This message is shown if habit was checked out more than one day in the future. Please review your habits!")


# analyzation commands
# get list of habits sorted by closest goal 
@analyzation.command()
def closest_goal():
    """show closest goal"""
    habit_list = logic.habit_list_creator('days_remaining')
    print(tabulate(habit_list, headers='firstrow', tablefmt='github'))
    print(f"    The closest goal is reached in {habit_list[7][1]} days from habit '{habit_list[0][1]}'")

# show the current streaks of all habits -------_>>>>>> testen!!!!!!!   sollte so hoffentlich funktionieren!
@analyzation.command() 
def current_streaks():
    """show current streaks"""
    names, streaks = logic.calculate_current_streaks()
    
    for n, s in zip(names, streaks):                 # ------_>>>>>>>> muss ich das zippen oder geht das auch so? Testen!
        print(f"    The current streak from habit '{n}' is {s} days!")

# get a list of habits sorted by the longest streak ------_>>>>>>>>>> testen!"!!!"   sollte hoffentlich so funktionieren!
@analyzation.command()
def longest_streak():
    """show longest streak"""
    habit_list = logic.habit_list_creator('longest_streak', True) 
    print(tabulate(habit_list, headers='firstrow', tablefmt='github'))
    
    print(f"    The longest streak is achieved from habit '{habit_list[0][1]}' and is {habit_list[11][1]} days in a row! It was broken {habit_list[13][1]} times.")        

# get a list of habits sorted by the total time wasted from high to low 
@analyzation.command()
def time_cost():
    """show total time cost"""
    habit_list = logic.habit_list_creator('total_time_cost', True)
    print(tabulate(habit_list, headers='firstrow', tablefmt='github'))
    print(f"    The highest time cosumption is {habit_list[5][1]} minutes from habit '{habit_list[0][1]}'")

# get a list of habits sorted by the total cost from high to low 
@analyzation.command()
def cost():
    """show total cost"""
    habit_list = logic.habit_list_creator('total_cost', True)
    print(tabulate(habit_list, headers='firstrow', tablefmt='github'))
    print(f"    The highest total cost is {habit_list[3][1]} Euros from habit '{habit_list[0][1]}'")


# test-function for logic --> needs to be deleted!!
@actual_state.command()
def test_function(): 
    """test function"""

    # break habit function umschreiben; reset anders designen

    #was muss ich was anpasssen mit den zwei neuen variablen? wo assigne ich longest streak variable?
    
    #jetzt weitere punkte hier abarbeiten, sollte angepasst sein, Datenbank updaten und ausprobieren!


    # function schreiben: muss ich mich heute noch um habits kümmern opder erledigt
    
    # next step, wenn prg mit neuen variablen läuft wenn habit vorbei testen was passiert mit test variable von db



if __name__ == '__main__':
    cli()

