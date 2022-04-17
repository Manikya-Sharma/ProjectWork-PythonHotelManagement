""" ================HELPER MODULE=============

    To initilize **help** whenever user demands for information

    Functions: guide -> its use depends on help_usr
               help_usr -> main function to provide interactive help
               inp -> a ubiquitous function to take sepecialized input
"""


hotel_map = r"""
 ____________________________________________________________________________
|           15           |            14           |            13           |
|                        |                         |                         |
|------------------------|-------------------------|-------------------------|
|           10           |            11           |            12           |
|------------------------|-------------------------|-------------------------|
|                        |      ______8______      |                         |
|           9            |     |GROUND FLOOR |     |            7            |
|------------------------|-------------------------|-------------------------|
|                        |                         |                         |
|           4            |            5            |            6            |
|------------------------|-------------------------|-------------------------|
|           3            |            2            |            1            |
|__________________ _____|____________________ ----|-------------------------|
|                  |                          |            |   WASHROOM      |
|                  |                  ________|            |_________________|
|                  |     Fire Escape | ------ |           |                  |
|    Dining        |                 | STAIRS ==         ==     ELEVATOR     |
|     Hall         |_________________|________|           |__________________|   ________
|      __          |                          |   Reception     |            |  |        |
|     |__|         |                          |              ___|            |  |You are |
|      --          |        Kitchen           |            (|___--->Interactive |  HERE  |
|                  |                          |__________       |     Machine|  |________|
|__________________|__________________       Kitchen     \      |            |
|          ----    ---    ---         |   Equipments     |      |            |
|                                     |__________________|      | Underground|
|       Guest Room                                  _____       |   Parking  |
|                                                        |      |            |
|_________________   _________________   ________________|      |____________|
                 /   \               /   \               |      |
                          WINDOWS                        /      \
                                                        /        \
                                                        ENTRY GATE

"""

def showprices():
    from price import price_per_day_l,price_per_day_r,\
         price_per_month_l,price_per_month_r,price_per_year_l,\
         price_per_year_r,price_per_hour_l,price_per_hour_r
    print("The prices are as follows :-(per head) ")
    print("The prices are :-")
    print("\nLUXURY:-")
    print("Price per hour: \u20B9",price_per_hour_l)
    print("Price per day: \u20B9",price_per_day_l)
    print("Price per month: \u20B9",price_per_month_l)
    print("Price per year: \u20B9",price_per_year_l)
    print("\nREGULAR:-")
    print("Price per hour: \u20B9",price_per_hour_r)
    print("Price per day: \u20B9",price_per_day_r)
    print("Price per month: \u20B9",price_per_month_r)
    print("Price per year: \u20B9",price_per_year_r)
    print("\nIn case you dont mention the price, you will have\
to pay \u20B9%u more than luxury per hour"%(10))
    print("In case more duration is stayed than mentioned, you\
will have to pay \u20B9%u more than luxury per hour"%(50))
    print("If no time mentioned and stayed less than 3 hours, \
you will have to pay fixed amount \u20B9%u"%(1000))
    print("In case you leave early, still you will have to pay \
as much according to duration mentioned")


def guide():
    print()
    print("What would you like to do?")
    print("1. Info about the menus of program")
    print("2. Rules for username and password")
    print("3. How to update the account")
    print("4. Lodging complaints")
    print("5. Pricing of hotel")
    ch = input("=>")
    if ch == "1":
        print("""
    The various menus of the program are:-
1. Check-in: This is for a new customer to check-in and open an account. The program
             will guide all the steps and also provide the room number.
2. Sign-up:  This is meant only for official persons who have applied for any post in
             the hotel. They will have to also provide the hotel password for security
             reasons
3. Login:    If the person already has an account, this menu will prompt to enter the
             username and password. If password is wrong more than 3 times, the account
             may get blocked, so kindly contact the officials to provide password if
             forgot.
4. QUIT:     It will quit the program.
             """)
    elif ch =="2":
        print('''VALIDITY OF USERNAME

            1. Should be unique
            2. No special symbols except _
            3. No Spaces''')
        print()
        print('e.g. Manikya_Sharma')
        print()
        print("""VALIDITY OF PASSWORD

            1. Atleast 6 characters length
            2. Atleast 1 number
            3. Atleast 1 special character
            4. Atleast 1 lowercase
            5. Atleast 1 uppercase
            6. No Spaces
            """)
        print()
        print("e.g. Manikya@123")
    elif ch == "3":
        print("""In order to update your account, you will have to consult authorities.
              You can simply lodge a complaint to any official or general grievance.""")
    elif ch == "4":
        print("""You will first have to login with your account. It will consist of a
              sub-menu to complain. Kindly enter your grievance and try to addresss it
              to relevant authority.""")
    elif ch == "5":
        showprices()


def help_usr():
    print('\n\n')
    print("===========================================================================")
    print("                       =| Welcome to our HELP UTILITY! |=                  ")
    print("         =| There are various topics for help which you can demand |=      ")
    print("                     =| quit help module by typing *q* |=                  ")
    print("\n                    =| The available topics are:- |=                     ")
    print("                __________________________________________________         ")
    print("               |   MAP |  PRICES  |  LOCATION  |  GUIDE | TOPICS  |        ")
    print("               |_______|__________|____________|________|_________|        ")
    print("===========================================================================")
    print()
    print("Type any topic to get its details, type `topics` for re-showing the topics")
    val = input("=>")
    while val != "*q*":
        if "q" in val.lower() and len(val)<=3:
            print("Did you mean to quit?(y/n)")
            ch = input(">")
            if ch.lower() == "y":
                print("Returning back to main program ...")
                print("Please input again the data which was asked")
                break
            else:
                print("Please enter the value again")
        if "MAP" in val.upper():
            print("The map of the hotel is as follows:-")
            print()
            print(hotel_map)
        if "PRICES" in val.upper():
            showprices()
        if "LOCATION" in val.upper():
            print("The location is:-")
            print("Hotel Luxury Palace, Chandni Chowk, New Delhi, 110006")
        if "GUIDE" in val.upper():
            guide()
        if "TOPICS" in val.upper():
            print("                     =| quit help module by typing *q* |=                  ")
            print("                __________________________________________________   ")
            print("               |   MAP |  PRICES  |  LOCATION  |  GUIDE | TOPICS  |  ")
            print("               |_______|__________|____________|________|_________|  ")
        val = input("=>")
    else:
        print("Thank you for using help module!")
        print("Returning back to main program ...")
        print("Please input again the data which was asked")

        
def inp(prompt = "",typ = str):
    """FUNCTION TO ACCESS INPUT
       ADDITIONAL FUNCTIONALITY BY ALLOWING TO INITIALIZE HELP MODULE
       OR TO QUIT
    """
    val = input(prompt).strip()
    if val == "**help**":
        help_usr()
        val = input(prompt)       # after leaving help module, input needs to be supplied
        return val
    elif "help" in val.lower():   # user might have typed wrong
        print("Did you mean to initialize help module?(y/n)")
        choose = input("->")
        if choose.lower == "y":
            help_usr()
            val = input(prompt)   # after leaving help module, input needs to be supplied
            return val
    elif val == "**quit**":
        print("Thank you for using our program!")
        import sys
        sys.exit()
    elif "quit" in val.lower():
        print("Did you mean to quit?(y/n)")
        choose = input("->")
        if choose.lower() == "y":
            import sys
            sys.exit()
    else:
        while True:
            try:
                val = typ(val)
            except:
                print("Invalid Data, please enter again")
                val = input(prompt)
            else:
                break
        return val

