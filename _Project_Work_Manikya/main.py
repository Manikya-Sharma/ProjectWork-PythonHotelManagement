""" ================MAIN MODULE=============
        The main module to show menus and sub-menus.
        The user-interface or front-end of the program 
        Forms a link between all the modules
"""

# Imports


import mysql_handler as m
from helper import inp

# Global Declarations

hotel_pwd = 'admin'
con, cur = m.MAKE_CONNECTION()
m.USE_DATABASE('Hotel_Luxury_Palace', con, cur)

logged = False
_type = "Customer"
L = []

# Contents of L:-
# uid, pwd, name, num, TYPE, room, duration, checkin_time, price, purpose, service, blocked
# user, pwd, name, post


# Making accounts

def check_in():
    import checkin, price
    import time
    global logged, L
    print("\nPlease enter your NAME: ")
    name = inp(">")
    print("\nWELCOME %s!"%name.upper())
    print("Let us begin by making your account")
    
    uid, pwd, num, TYPE, duration, purpose, service = checkin.ask()
    price, about = price.prices(duration, service, TYPE, int(num))
    room = checkin.room_num(TYPE)
    now_time = time.localtime()  # gives time in a particular format
    checkin_time = time.strftime("%Y %m %d %H ", now_time)  # this will structure time
    success = checkin.signup(uid, pwd, name, num, TYPE,
                             room, duration, checkin_time,
                             price, purpose, service)
    while not success:
        print("There was some problem!")
        print("Please make your account once again")
        print("Sorry for the inconvenience caused")
        success = True    # Assuming next attempt succeeds
        check_in()
    else:
        print("CONGRATULATIONS!")
        print("Your account has been created successfully!")
        print("Your room number is", room)
        L = [uid, pwd, name, _type, num, TYPE, room, duration,
             checkin_time, price, purpose, service, "NO"]
        logged = True


def off_sign_up():
    # for official person
    from checkin import ask_official as ask_off, offsignup
    global logged, _type, L
    corr = False
    chances = 3
    while not corr:
        if chances == 0:
            print("Your chances are over")
            print("Kindly contact the authorities")
            break
        pwd = inp("Please enter the hotel password: ")
        if pwd != hotel_pwd:
            print("WRONG HOTEL PASSWORD!")
            print("Please Try Again")
            print()
            print("Chances left:%u"%chances)
            chances -= 1
        else:
            corr = True
            _type = 'Official'
    else:
        print("\nPassword Accepted")
        user, pwd, name, post = ask_off(con, cur)
        done = offsignup(user, pwd, name, post)
        if done:
            print("Your account has been created successfully!")
            logged = True
            L = [user, pwd, name, post]
        else:
            print("Sorry an issue occured, please try again later")

# Login

def main_login():
    import login
    global logged, L, _type
    while True:
        print("Enter the username")
        user_id = inp(">")
        found, _type = login.find_uid(user_id)
        if not found:
            print("No such user name, please try again")
        else:
            break
    if _type == "Customer":
        uid, pwd, name, about, num, Type, room_num, duration, checkin_time, price, purpose, service, blocked = login.about_uid(user_id, _type)
        if blocked.upper() == "YES":
            print("THIS ACCOUNT IS BLOCKED")
            print("Please contact authorities to unblock")
            return
    elif _type == "Official":
        uid, pwd, name, post = login.about_uid(user_id, _type)
    print("Enter the password")
    new_pwd = inp('>')
    logged = login.corr_pwd(user_id, new_pwd, pwd, 3)
    L = login.about_uid(user_id, _type)
    
    
# Main user interface

    # For official personnel

        # Miscelleneous functions

def get_acc():
    print("Please wait while we process...")
    h1, details, none = m.SELECT('Customer_Details', con, cur)
    h2, info, none = m.SELECT('Customer_Info', con, cur)
    if len(details) == len(info):
        num_records = len(details)
        if num_records == 0:
            print("No Customer accomodating")
            return
    else:
        print("There is some issue in data, sorry for inconvenience")
        return

    print("\nTOTAL NUMBER OF CUSTOMERS ACCOMODATING =", num_records)
    print("1. Tabular form")
    print("2. Tiles form")
    print("In which manner do you want data to be printed?[1 or  2]")
    q = inp(">",int)
    print("=====================================================")
    if q == 1:
        m.output_table(h1,details)
        m.output_table(h2,info)
        print("-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x")
        return
    # By defauls tiles mode is preferred
    i = 0
    while i<num_records:
        uid,pwd,name,about,num,TYPE,room_num = details[i]
        uid,duration,checkin_time,price,purpose,service,blocked = info[i]
        
        print("_"*50)
        print()

        print(i+1, '.', sep='')   # i+1th customer
        print("Room Number:", room_num)
        print("Name:", name, '(%s)'%about)
        print("User id:", uid)
        print("Password:", pwd)
        if blocked.upper() == "YES":    # Blocked account
            print("Status: BLOCKED")
        print()
        print("Type of accomodation:", end=" ")
        if TYPE == "l":
            print("Luxury")
        else:
            print("Regular")
        print("Duration to stay:", end=" ")
        lis = duration.split()
        t = ("Years", "Months", "Days", "Hours")
        for j in range(len(lis)):
            print(lis[j], t[j], end=' ')
        print()
        print("Number of people accompanying:", (int(num)-1))
        print("Check-in time:", end=" ")
        lis = checkin_time.split()
        lis.reverse()
        for x in range(1, len(lis)-1):
            print(lis[x], end='/')
        x+=1
        print(lis[x], end=",")
        print("time:", lis[0])
        print()
        print()
        if price != 0.0:
            print("Price to be payed:", price)
        else:
            print("Price to be payed at check-out")
        print("Purpose of visit:", end=' ')
        if purpose is not None:
            if not(purpose.isspace()):
                print(purpose)
        print("Service demanded:", service)        
        i += 1
        

def del_acc(user_id):
    import grievance
    existing = m.SELECT('Customer_Details',con,cur,('user_id',))[1]
    for row in existing:
        for column in row:
            if column == user_id:
                found = True
                break
            else:
                found = False
        if found:
            break
    else:
        found = False
    if not found:
        return False    # No such record found
    else:
        # Remove any existing grievance
        existing = m.SELECT('Grievances',con,cur,condition = "user_id = '%s'"%user_id)[1]
        for row in existing:
            user, gr, pos = row
            grievance.delete_grievance(user, gr, pos)
        # Remove account
        stmt1 = "DELETE FROM Customer_Details where user_id = '%s';"%(user_id)
        stmt2 = "DELETE FROM Customer_Info where user_id = '%s';"%(user_id)
        d1 = m.UPDATE(stmt1,con, cur)
        d2 = m.UPDATE(stmt2,con, cur)
        return (d1 and d2)   # True only in case both true


def manage_grievance(post):
    import grievance as g
    g.central_link(post)    # pass on to this module
    


def see_feedbacks():
    print("Feedbacks:-")
    feeds = m.SELECT('Feedback', con, cur)[1]
    i = 1
    for feed in feeds:
        feed = feed[0]    # feed will originally be a list
        print("%u. %s"%(i, feed))
        i += 1
    if i == 1:
        print("No feedbacks uploaded till now")

        # Main user interface
        
def ask_official(uid, pwd, name, post):
    print()
    print("="*50)
    print("Welcome %s!"%name)
    print()
    print("Authority:", post, sep='')
    print()
    print("What would you like to do?")
    print("1. Obtain all the accounts and info")
    print("2. Delete any existing account")
    print("3. Manage grievances")
    print("4. See the feedbacks from customers")
    print("5. Quit Program")
    print()
    valid_choice = False
    while not valid_choice:
        valid_choice = True
        choice = inp(">")
        if choice == "1":
            get_acc()
        elif choice == "2":
            from login import find_uid
            user_id = inp("Enter user id:")
            if find_uid(user_id)[0]:
                done = del_acc(user_id)    # Further ensures only correct user id
                if not done:
                    print("Sorry, the account could not be deleted")
                else:
                    print("Account deleted successfully")
        elif choice == "3":
            manage_grievance(post)
        elif choice == "4":
            see_feedbacks()
        elif choice == "5":
            print("Exiting program")
            import sys
            sys.exit()
        else:
            valid_choice = False
            print("Invalid choice")
            print("Please enter your choice again!")


    # For customers

        # Miscelleneous functions


def dineout(roomnum):
    dishes = {'Tandoori Bharwa Aloo': 210.00, 'Tandoori Gobi': 210.00,
              'Paneer Tikka': 250.00, 'Malai Paneer Tikka': 250.00,
              'Lasuni Paneer Tikka': 250.00, 'Paneer ke Sholay': 250.00,
              'Veg Kadai': 220.00, 'Veg Masala': 220.00,
              'Veg Kolhapuri': 220.00, 'Tawa Sabzi': 220.00,
              'Paneer Butter Masala': 240.00, 'Paneer Jalfarezi': 240.00,
              'Paneer Kolhapuri': 240.00, 'Aloo Mattar': 220.00,
              'Dal Fry': 200.00, 'Dal Tadka': 200.00,
              'Tandoori Roti': 25.00, 'Butter Nan': 50.00,
              'Rumali Roti': 40.00, 'Cheese Nan': 50.00,
              'Veg Biryani': 225.00, 'Veg Pulao': 225.00,
              'Jeera Rice': 70.00}
    menu = """
    STARTERS:-                                        Price(in Rs.)

    Tandoori Bharwa Aloo ................................210.00
    Tandoori Gobi ........................................210.00
    Paneer Tikka .........................................250.00
    Malai Paneer Tikka ...................................250.00
    Lasuni Paneer Tikka ..................................250.00
    Paneer Ke Sholay .....................................250.00

    MAIN COURSE:-

    Veg Kadai ............................................220.00
    Veg Masala ...........................................220.00
    Veg Kolhapuri ........................................220.00
    Tawa Sabzi ...........................................220.00
    Paneer Butter Masala .................................240.00
    Paneer Jalfarezi .....................................240.00
    Paneer Kolhapuri .....................................240.00
    Aloo Mattar ..........................................220.00
    Dal Fry ..............................................200.00
    Dal Tadka ............................................200.00

    ROTI:-

    Tandoori Roti ........................................25.00
    Butter Nan ...........................................50.00
    Garlic Nan ...........................................50.00
    Rumali Roti ..........................................40.00
    Cheese Nan ...........................................50.00

    RICE:-

    Veg Biryani ..........................................225.00
    Veg Pulao ............................................225.00
    Jeera Rice ...........................................70.00"""
    
    cost = 0.0
    print()
    print("         ===================== MENU=====================        ")
    print(menu)
    print("\nPlease enter the dishes name you would like to order, type **nomore** to stop\n")
    while True:
        dish = inp(">").title()
        if "nomore" in dish.lower():
            break
        if dish in dishes.keys():
            print("How many %s to be ordered?"%dish)
            num = inp(">", int)
            cost += (num*dishes.get(dish))
            print("Order noted, what else? (Type 'nomore' to stop)")
            print()
        else:
            print("There seems to be a typo, please enter again\n")
    print("\nYour order has been placed, we will soon send the food at your room %s"%roomnum)
    print("Your final cost to be payed is \u20B9%u, kindly pay at reception"%cost)


def roomservice(roomnum):
    print("The room service has been called for room number:", roomnum)
    


def complain(uid):
    import grievance
    grievance.obtain_grievance(uid)


def checkout(uid):
    import price as p
    import grievance
    print()
    print(" "*7, "="*65, end='')
    print(r"""
      _____ _   _    _    _   _ _  _   _   _  ___    
        |   |   |   / \   |\  | | /    \   / |   | |   |  |
        |   |---|  /---\  | \ | |<      \ /  |   | |   |  |
        |   |   | /     \ |  \| | \_     |   |___| |___|  .
    """)
    print(" "*7, "="*65, end='')
    print()
    # FEEDBACK
    print("Please give us a feedback on the visit:-")
    feedback = inp(">")
        # It will be stored anonymously
    feedback_d = {'feedbacks':feedback}
    m.INSERT_VALUES('feedback',feedback_d,con,cur)
    # REMOVE EXISTING GRIEVANCES
    existing = m.SELECT('Grievances',con,cur,condition = "user_id = '%s'"%uid)[1]
    for row in existing:
        user, gr, pos = row
        grievance.delete_grievance(user, gr, pos)
    # PRICE TO BE PAYED
    lis = m.SELECT('Customer_Info',con,cur,('price','checkin_time','duration'),condition="user_id='%s'"%uid)[1]
    for row in lis:
            price, checkin_time, duration = row
    price = p.evaluate_price(price, checkin_time, duration)
    print("\nYou have to pay \u20B9 %u"%price)
    print("Kindly pay the above amount at the reception\n")

    # REMOVING ACCOUNT
    del_acc(uid)
    
    # PROGRAM ENDS
    print("We hope you visit again!")
    import sys
    sys.exit()

        # Main user inteface

def ask_customer(uid, pwd, name, about, num, TYPE, room, duration,
             checkin_time, price, purpose, service, blocked):
    """"Will ask the logged-in customer for the services required"""
    print()
    print("="*50)
    print()
    print("Welcome %s!"%name)
    print("What would you ,like to do?")
    print()
    print("1. Dine out")
    print("2. Room service")
    print("3. Register complaint or request updation of account")
    print("4. Check-out")
    print("5. Close the program")
    print()
    valid_choice = False
    while not valid_choice:
        valid_choice = True
        choice = inp(">")
        if choice == "1":
            dineout(room)
        elif choice == "2":
            roomservice(room)
        elif choice == "3":
            complain(uid)
        elif choice == "4":
            print("Are you sure you want to check out?(y/n)")
            ques = inp(">")
            if ques.lower() == 'y':
                checkout(uid)
            else:
                print("Please enter your choice again!(y/n)")
                valid_choice = False
        elif choice == "5":
            import sys
            sys.exit()    
        else:
            valid_choice = False
            print("Invalid choice")
            print("Please enter your choice again!")

# Starting of the program

def start():
    print(" "*16, "="*50, end='')
    print(r'''
                 _          _  ____  _      _____   ____   _    _   ____    
                  \        /  |      |     |       |    |  |\  /|  |        |
                   \  /\  /   |----  |     |       |    |  | \/ |  |---     |
                    \/  \/    |____  |____ |_____  |____|  |    |  |____    .
          ''')
    print(" "*16, "="*50)
    print('\n\n')
    print(' '*9, "#"*22, "\t%20s\t"%"Hotel Luxury Palace", "#"*22, sep='')
    print('\n\n')
    
    print("           _____________________________________________________________________")
    print("          |                                                                     |")
    print("          |      NOTE: You can type **help** anytime to get interactive help    |")
    print("          |            You can also type **quit** anytime to quit               |")
    print("          |_____________________________________________________________________|")
    
    print()
    
    print("What would you like to do?")
    
    print("1.Check-in")
    print("2.Sign-up [for Official Personnel]")
    print("3.Login")
    print("4.Quit")
    print()
    
    valid = False
    while not valid:
        valid = True    # assuming correct input
        choice = inp(">")
        if choice == '1':
            check_in()
        elif choice == "2":
            off_sign_up()
        elif choice == "3":
            main_login()
        elif choice == "4":
            print("Thank you for using our program!")
            import sys
            sys.exit()
        else:
            print()
            print("Please Enter a Valid Option!")
            valid = False

    # After Welcoming
        
    if logged:
        if _type == "Customer":
            uid, pwd, name, about, num, TYPE, room, duration, checkin_time, price, purpose, service, blocked = L
            ask_customer(uid, pwd, name, about,num, TYPE,
                         room, duration, checkin_time,
                         price, purpose, service, blocked)
        elif _type == "Official":
            user, pwd, name, post = L
            ask_official(user, pwd, name, post)
    else:    # if somehow
        print("Seems like you aren't logged in..")
        print("Would you like to login?(y/n)")
        log_choice = inp(">")
        if log_choice == "n":
            import sys
            sys.exit()
        else:
            main_login()
    # now the function has ended and program is over
    while True:
        print("\nWould you like to do anything else?(y/n)")
        choice = inp(">")
        if choice == "y":
            if _type == "Customer":
                uid, pwd, name, about, num, TYPE, room, duration, checkin_time, price, purpose, service, blocked = L
                ask_customer(uid, pwd, name, about, num, TYPE,
                             room, duration, checkin_time,
                             price, purpose, service, blocked)
            elif _type == "Official":
                user, pwd, name, post = L
                ask_official(user, pwd, name, post)
        else:
            print("Thank you for using our program!")
            break


start()  # Function call and BEGINNING OF PROGRAM
