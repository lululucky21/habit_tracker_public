"""file for testing project via pytest"""

from interface import delete_habit
from interface import Habit, get_habits, break_habit, checkout_habit, delete_habit

#from main import checkout, get_all_habits, checkout_state
import click
import interface
import logic
from tabulate import tabulate
from datetime import datetime, timedelta

# class Test_Habit:
#     id = int
#     name = str
#     start_time = str
#     daily_cost = float
#     total_cost = float
#     time_wasted = int
#     total_time_cost = float
#     general_goal = int
#     days_remaining = float
#     daily_iter = int
#     checkout_counter = int
#     last_checkout_time = str
#     longest_streak = int
#     date_broken = str
#     broken_counter = int
#     total_checkout = int


#     def test_habit(self):
#         #habit = Habit("habit_1", "habit_2", 2, 2, 2, 2)
        
#         get_habits()
#         #habit = Habit(name="name", start_time="time", daily_cost=2, time_wasted=23, general_goal=2, daily_iter=1)
#         #add_habit(habit)
#         #break_habit("name")
#         checkout_habit("name", 2)

# def test_checkout():
#     checkout("name", 2)

def test_x():
    delete_habit("name")