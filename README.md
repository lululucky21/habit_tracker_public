
# Habit Tracker IUBH
### Luca Stephan 04 / 2023

This is a habit tracker designed for usage within a terminal. Make sure that you have __git__ preinstalled

To get started you first have to create a new directory and clone the repository from Github. Run the following commands from you terminal in you desired directory (e.g., your Desktop):

> ``mkdir habit_tracker``
> 
> ``git clone https://github.com/lululucky21/habit_tracker_public.git``

With the following command you automatically initialize the virtual environment and install the packages necessary for running the program:

> ``source init.bash``

***

You are now ready to use the program. Enter it by typing the next command into your terminal.

> ``python3 main.py``

From now on the program shows you possible commands and within the second layer also descriptions of the functionaliy. 

At the first level of this application the command groups are set and at the second level the actual tasks. You can find an overview about possible commands below:

> __First Level of Application:__
> -----
> > ``actual-state``
> > 
> > ``analyzation``
> > 
> > ``manage-habits``

> __Second Level ``actual-state``:__
> -----
> > ``checkout-state`` 
> > ``get-all-habits`` 
> > ``get-habit``

> __Second Level ``analyzation``:__
> -----
> > ``closest-goal``
> > ``cost``
> > ``current-streaks``
> > ``longest-streak``
> > ``time-cost``

> __Second Level ``manage-habits``:__
> -----
> > ``break-habit``
> > ``change-attribute``
> > ``checkout``
> > ``create``
> > ``delete``
> > ``reset``

***

####Following you can find code examples to understand the workflow:

Creating a new habit and storing it in the database:

> ``python3 main.py manage-habits create`` 

Checkout an existing habit and update the database:

> ``python3 main.py manage-habits checkout`` 

Show current streaks of habits in the database:

> ``python3 main.py analyzation current-streaks`` 

Showing a list of all habits stored in the database:

> ``python3 main.py actual-state get-all-habits`` 