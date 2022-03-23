""" file for data base connection; writing data, loading data """ 

from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base =  declarative_base()
class Habit(Base):
        __tablename__ = 'habit'

        id = Column('id', Integer, primary_key=True)
        name = Column('name', String, unique=True)
        start_time = Column('start time', String) 
        daily_cost = Column('daily cost (€)', Float)
        total_cost = Column('total cost (€)', Float)
        time_wasted = Column('time wasted (min)', Integer)
        total_time_cost = Column('total time cost', Float) 
        general_goal = Column('general goal (days)', Integer)
        days_remaining = Column('remaining days', Float)
        daily_iter = Column('daily iterations', Integer)
        checkout_counter = Column('checkout', Integer) 
        last_checkout_time = Column('last checkout time', String)
        longest_streak = Column('longest streak (days)', Integer) #-->>>>>>> zu testen
        date_broken = Column('last time broken', String) #-->>>>>>>>>>> zu testen!
        broken_counter = Column('times broken', Integer) # ---->>>>> zu testen"!
        total_checkout = Column('total checkout counter', Integer) # ---->>>> zu testen (um alle checkouts hochzuzählen, auch wenn habit gebrochen), nur intern nciht in listen ausgeben
        

        def __init__(self, name, start_time, daily_cost, time_wasted, general_goal, daily_iter):
            self.name = name
            self.start_time = start_time
            self.daily_cost = daily_cost
            self.total_cost = 0
            self.time_wasted = time_wasted
            self.total_time_cost = 0
            self.general_goal = general_goal
            self.days_remaining = general_goal 
            self.daily_iter = daily_iter
            self.checkout_counter = 0
            self.last_checkout_time = "not checked out" # overwritten by checkout time
            self.longest_streak = 0
            self.date_broken = "not broken"
            self.broken_counter = 0
            self.total_checkout = 0


def create_tables(engine):
    Base.metadata.create_all(engine)

# create database with name habits.db
def get_db(name="habits.db"):
    engine = create_engine('sqlite:///' + name, echo = True)
    create_tables(engine) 
    Session = sessionmaker(bind=engine)
    session = Session()

    return session 

# get the session globally
session = get_db() 

# managing habits commands
# add a habit to db        
def add_habit(habit):
    session.add(habit)
    session.commit()

# get all habits as object 
def get_habits():
    habits = session.query(Habit).all() 
    return habits

# checkout predefined habit -------_>>>>>>>>>> prüfen!!!!
def checkout_habit(habit_name, count):
    habit = session.query(Habit).filter(Habit.name == habit_name).first()
    habit.checkout_counter += count
    habit.last_checkout_time = datetime.strftime(datetime.now(), '%y-%m-%d %H:%M:%S')
    habit.total_checkout += count
    
    #sollte so funktionienren! Prüfen! 
    actual_streak = habit.checkout_counter / habit.daily_iter
    if habit.longest_streak < actual_streak:       
        habit.longest_streak = actual_streak
    
    session.commit()
    
# break habit function u.a. zum updaten von longest streak ->>>>>>>> !!!!! 
# schauen, wie das so funktioniert; Sachen die checkout counter zur Analyse benutzen anpassen! ------>>>>> fehlen hier noch Variablen?
def break_habit(habit_name):
    habit = session.query(Habit).filter(Habit.name == habit_name).first()
    habit.date_broken = datetime.strftime(datetime.now(), '%y-%m-%d %H:%M:%S')
    habit.checkout_counter = 0
    habit.broken_counter += 1
    habit.days_remaining = habit.general_goal
    session.commit()
        

# reset start time to now, days remaining to general goal, count to 0, checkout time, longest streak and date broken of habit 
def reset_habit(habit_name):
    habit = session.query(Habit).filter(Habit.name == habit_name).first()    
    habit.start_time = datetime.strftime(datetime.now(), '%y-%m-%d %H:%M:%S')
    habit.days_remaining = habit.general_goal
    habit.total_cost = 0
    habit.total_time_cost = 0
    habit.checkout_counter = 0
    habit.last_checkout_time = "not checked out"
    habit.longest_streak = 0
    habit.date_broken = "not broken"
    habit.broken_counter = 0
    habit.total_checkout = 0
    session.commit()

# delete a habit 
def delete_habit(habit_name):
    habit = session.query(Habit).filter(Habit.name==habit_name).first()
    session.delete(habit)
    session.commit()

# changing an attribute of habit 
def change_attribute(habit_name, attribute, value):
    habit = session.query(Habit).filter(Habit.name==habit_name).first()
    setattr(habit, attribute, value)   
    session.commit()
       
# get values of specific habit stored in db 
def get_habit(habit_name):
    habit = session.query(Habit).filter(Habit.name==habit_name).first()                                                                                                                                                                                                     
    attribute_list = [
        ["Habit Name:", habit.name], ["Start Time:", habit.start_time], ["Daily Cost:", habit.daily_cost], ["Total Cost:", habit.total_cost]
        ["Time Wasted:", habit.time_wasted], ["Total Time Cost:", habit.total_time_cost],["General Goal:", habit.general_goal], ["Days Remaining:", habit.days_remaining], 
        ["Daily Iterations:", habit.daily_iter], ["Checkout:", habit.checkout_counter], ["Last Checkout:", habit.last_checkout_time],
        ["Longest Streak:", habit.longest_streak], ["Last Time Broken:", habit.date_broken], ["Times Broken:", habit.broken_counter]
        ]
    return attribute_list

#ggf. function get habit anpassen von obendrüber, in jedem Fall nach oben sortieren!
#get a single habit (as object) stored in db
def get_single_habit(habit_name):
    habit = session.query(Habit).filter(Habit.name==habit_name).first() 
    return habit