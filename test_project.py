"""file for testing project via pytest: It contains chain tests with multiple assertions per test"""

import interface
import logic
import unittest
from datetime import datetime


class TestProjectFunctions(unittest.TestCase):

    def setUp(self):
        """for initializing testing environment"""
        name = "name"
        cost = 3
        time_wasted = 2
        goal = 30
        iterations = 2

        start_time = datetime.strftime(datetime.now(), '%y-%m-%d %H:%M:%S')
        habit = interface.Habit(name=name, start_time=start_time, daily_cost=cost, time_wasted=time_wasted, general_goal=goal, daily_iter=iterations)
        interface.add_habit(habit)
    
    
    def test_create_habit(self):
        """create a new habit (directly deletes it after testing)"""
        name = "name_1"
        cost = 3
        time_wasted = 2
        goal = 10
        iterations = 2

        start_time = datetime.strftime(datetime.now(), '%y-%m-%d %H:%M:%S')
        habit = interface.Habit(name=name, start_time=start_time, daily_cost=cost, time_wasted=time_wasted, general_goal=goal, daily_iter=iterations)
        interface.add_habit(habit)
        print(f"    The habit '{name}' has been added to the database!")
    
        self.assertIsNotNone(interface.get_single_habit(name))

        interface.delete_habit("name_1")

    def test_checkout_habit(self):
        """checkout habit"""
        cli_name = "name"
        count = 1

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
                print(f"\n    Your habit '{name}' is already reached since {-(goal)} checkouts!\n    Please change your goal or reset habit.")

        habit = interface.get_single_habit("name")
        self.assertEqual(1, habit.checkout_counter)
        self.assertEqual(1, habit.total_checkout)
        self.assertEqual(0.5, habit.longest_streak)
    
    def test_break_habit(self):
        """break habit"""
        name = "name"
        option = "break"
        
        if option == "break":
            interface.break_habit(name)
            print(f"    Your habit '{name}' has been broken! You can continue checking it out!")
        
        habit = interface.get_single_habit("name")   
        self.assertEqual(0, habit.checkout_counter)
        self.assertEqual(1, habit.broken_counter)
        self.assertEqual(habit.general_goal, habit.days_remaining)
        
    def test_reset_habit(self):
        name = "name"
        
        interface.reset_habit(name)
        print(f"    The habit '{name}' has been reset!")
        
        habit = interface.get_single_habit("name") 
        self.assertEqual(habit.days_remaining, habit.general_goal)
        self.assertEqual(habit.total_cost, 0)
        self.assertEqual(habit.total_time_cost, 0)
        self.assertEqual(habit.checkout_counter, 0)
        self.assertEqual(habit.last_checkout_time, "not checked out")
        self.assertEqual(habit.longest_streak, 0)
        self.assertEqual(habit.date_broken, "not broken")
        self.assertEqual(habit.broken_counter, 0)
        self.assertEqual(habit.total_checkout, 0)
    
    def test_change_attribute(self):
        """change_attribute function of main module with underlying logic functions"""
        name = "name"
        attribute = "general_goal"
        value = "60"
        
        if attribute == "checkout_counter":
            print("Please checkout your habit within the checkout function!")
        elif attribute in [
            "total_cost", "total_time_cost", "days_remaining", "last_checkout_time", 
            "longest_streak", "date_broken", "broken_counter", "total_checkout", "start_time"
            ]:
            print("You cannot change this attribute!")
        else:
            interface.change_attribute(name, attribute, value)
            print(f"    The attribute '{attribute}' of the habit '{name}' has been changed to '{value}'!")
            
        habit = interface.get_single_habit("name") 
        self.assertEqual(60, habit.general_goal)
        
        # testing chain of calculate goal
        expected = 60 - habit.checkout_counter / habit.daily_iter
        if attribute in ["general_goal", "daily_iter"]:
            logic.calculate_goal()
        habit = interface.get_single_habit("name") 
        self.assertEqual(expected, habit.days_remaining)
        
        # testing chain of calculate total time cost
        expected = 60 * habit.checkout_counter
        attribute = "time_wasted"
        interface.change_attribute(name, attribute, value)
        logic.calculate_total_time_cost() 
        habit = interface.get_single_habit("name") 
        self.assertEqual(expected, habit.total_time_cost)
        
        # testing chain of calculate total cost
        expected = 60 * (habit.total_checkout / habit.daily_iter)
        attribute = "daily_cost"
        interface.change_attribute(name, attribute, value)
        logic.calculate_cost() 
        habit = interface.get_single_habit("name") 
        self.assertEqual(expected, habit.total_cost)
        
        interface.reset_habit(name)
        
    def test_calculate_streaks(self):
        """test streak calculation"""
        daily_iter = [2, 3, 1]
        checkout_counter = [74, 45, 187]
        
        streaks = [x/y for (x,y) in zip(checkout_counter, daily_iter)]

        self.assertEqual(streaks[2], 15)
                      

    def tearDown(self):
        interface.delete_habit("name")
        #interface.delete_habit("name_1")


if __name__ == '__main__':
    unittest.main()
    
    