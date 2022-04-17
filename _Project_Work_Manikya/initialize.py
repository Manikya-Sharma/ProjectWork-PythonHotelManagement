""" ============INITIALIZER MODULE==========

    To initialize the package 
    It is to build minimum database before employing the program.
        
    CAUTION: Should run only for creating new files without accounts.
        
    Contains code to make account of manager

"""

# Imports

import mysql_handler as m
from helper import inp
from checkin import offsignup, take_uid_pwd

# Globals

hotel_pwd = "admin"   # Not to be disclosed

# User interface

print()
print("                 =============WELCOME==============                ")
print()
print("        Initialisation of module with basic requirements           ")
print()

allow = False
tries = 3
while not allow:
    if tries == 0:
        print("No more tries left , try again later")
        break
    print("Enter HOTEL PASSWORD")
    pwd = inp(">")
    if pwd == hotel_pwd:
        allow = True
    else:
        print("Invalid Password, please try again")
        print(tries-1, "tries left")
    tries -= 1

if allow:
    # This will also truncate previous entries if any
    con, cur = m.MAKE_CONNECTION()
    done = m.CREATE_DATABASE('Hotel_Luxury_Palace', con, cur)
    if not done:
        m.DROP_DATABASE('Hotel_Luxury_Palace', con, cur)
        m.CREATE_DATABASE('Hotel_Luxury_Palace', con, cur)        
    m.USE_DATABASE('Hotel_Luxury_Palace', con, cur)
    # TABLE - 1: Customer_Details
    cust_d_1 = {'user_id':('VARCHAR(20)','PRIMARY KEY'),
                'password':('VARCHAR(20)',),
                'name':('VARCHAR(20)',),
                'about':('VARCHAR(20)',),
                'number_of_people':('INT(2)',),
                'type':('CHAR(1)',),
                'room_num':('INT(3)',)}
    # TABLE - 2: Customer_Info
    cust_d_2 = {'user_id':('VARCHAR(20)','PRIMARY KEY'),
                'duration':('VARCHAR(12)',),
                'checkin_time':('VARCHAR(20)',),
                'price':('decimal(15,2)',),
                'purpose':('VARCHAR(20)',),
                'service': ('VARCHAR(20)',),
                'blocked':('VARCHAR(3)' ,)}
    # TABLE - 3: Official_Details
    off_d = {'user_id':('VARCHAR(20)','PRIMARY KEY'),
             'password':('VARCHAR(20)',),
             'name':('VARCHAR(20)',),
             'post':('VARCHAR(10)','UNIQUE')}
    # TABLE - 4: Grievances
    grievances_d = {'user_id':('VARCHAR(20)',),
                    'grievance':('VARCHAR(50)',),
                    'official_post':('VARCHAR(10)',)}
    # TABLE - 5: Feedback
    feedback_d = {'feedbacks':('VARCHAR(50)',)}
    # MAKE TABLES
    m.CREATE_TABLE('Customer_Details',cust_d_1,con,cur)
    m.CREATE_TABLE('Customer_Info',cust_d_2,con,cur)
    m.CREATE_TABLE('Official_Details',off_d,con,cur)
    m.CREATE_TABLE('Grievances',grievances_d,con,cur)
    m.CREATE_TABLE('Feedback',feedback_d,con,cur)
else:
    print("You are not allowed to make any modifications.")
    import sys
    sys.exit()


print("Enter the NAME of the manager:-")
name = inp(">")
print()

usname, pwd = take_uid_pwd()

offsignup(usname, pwd, name, 'Manager', con, cur)

print("\nThe initialization of module was successful, now we can begin with the main module")

import main   # Main program will begin from here

