"""   
         ===========SIGN-UP============

Module storing functions for signing up

Functions-> valid_usname : checks validity of username
            valid_pwd    : checks validity of password
            room_num     : assigns available room number
            findtime     : tells the current time
            signup       : adds account of customer
            offsignup    : ads account of official
            |take_uid_pwd: for input
            |take_purpose_service: for input
            |ask         : for input
            |ask_official: for input
"""

# Imports


import mysql_handler as m
from helper import inp

# Miscelleneous functions

def valid_usname(username, con=False, cur=False):
    """Checks whether username is valid or not
       Returns (valid,reason)
       
       VALIDITY OF USERNAME
       
       1. Should be unique
       2. No special symbols except _
       3. No Spaces
    """
    # con and cur are only meant for efficiency and not necessary

    valid = True    # Assuming that the username input is valid
    reason = "" 

    # Check uniqueness
    if (not con) or (not cur):
        con, cur = m.MAKE_CONNECTION()
    if not(m.db_in_use(con, cur)):
        m.USE_DATABASE('Hotel_Luxury_Palace', con, cur)
    existing1 = m.SELECT('Customer_Details', con, cur, ('user_id',))[1]
    existing2 = m.SELECT('Official_Details', con, cur, ('user_id',))[1]
    existing = existing1 + existing2
    for row in existing:
        for column in row:
            if username.lower() == column.lower():
                valid = False
                reason = "User Name already taken, please try another"
                break
        if not valid:
            break
    # Check characters
    for char in username:
        if char in '\'\"\\@`~!#$%^&*()-+=}{[]|;:<>,./?':
            valid = False
            reason = "Cannot use special symbols in username except _"
            break
        elif char == ' ':
            valid = False
            reason = "Spaces are invalid in username"
            break
    return valid, reason


def valid_pwd(password):
    """Checks whether password is valid or not
       Returns (valid,reason)
       
       VALIDITY OF PASSWORD
       
       1. At least 6 characters length
       2. At least 1 number
       3. At least 1 special character
       4. At least 1 lowercase
       5. At least 1 uppercase
       6. No Spaces
       """
    if len(password) < 6:
        valid = False
        reason = "Password length should be at least 6"
        return valid, reason
    valid = True   # Assuming valid password
    reason = ""
    uppers, lowers, specials, nums = 0, 0, 0, 0
    for char in password:
        if char in '\'\"\\@`~!#$%^&*()-+=}{[]|;:<>,./?':
            specials += 1
        elif char.isupper():
            uppers += 1
        elif char.islower():
            lowers += 1
        elif char.isdigit():
            nums += 1
        elif char == ' ':
            valid = False
            reason = "Spaces are invalid in username"
            break
    if nums == 0:
        valid = False
        reason = "At least one number is needed in password"
    if specials == 0:
        valid = False
        reason = "At least one special character is needed in password"
    if (uppers == 0) or (lowers == 0):
        valid = False
        reason = "At least one uppercase and one lowercase character is needed in password"
    return valid, reason



def room_num(type, con = False, cur = False):
    r""" To find a random room number. Also checks if room number is already occupied.
            Parameter-> type: "l" or r" 
            Returns  -> Room number
        /--------------------------------------------\
        | Room numbers follow the following rule:-   |
        |    Each floor has 15 rooms                 |
        |    There are 6 floors of the hotel         |
        |    The top three floors are for luxury     |
        |    The three ground floors are for regular |
        \--------------------------------------------/
        Will return None if no more rooms left
    """
    from random import randint

    if (not con) or (not cur):
        con, cur = m.MAKE_CONNECTION()
    if not(m.db_in_use(con, cur)):
        m.USE_DATABASE('Hotel_Luxury_Palace', con, cur)

    L_rows = m.SELECT('Customer_Details',con,cur,('room_num',))[1]
    if len(L_rows) == 0:   # means this is the first customer
        if type == 'l':
            return '1'
        else:
            return '300'
    existing = ()
    for row in L_rows:
        for column in row:
            existing += (column, )
    if len(existing) == 90:
        roomnum = 1
        return roomnum    # no more rooms - out of scope
    isexisting = True
    if type == 'l':       # Luxury
        while isexisting:
            roomnum = str(randint(300, 315))
            if roomnum not in existing:
                isexisting = False
            else:
                roomnum = str(randint(400, 415))
                if roomnum not in existing:
                    isexisting = False
                else:
                    roomnum = str(randint(500, 515))
                    if roomnum not in existing:
                        isexisting = False
    elif type == 'r':     # Regular
        while isexisting:
            roomnum = str(randint(1, 15))
            if roomnum not in existing:
                isexisting = False
            else:
                roomnum = str(randint(100, 115))
                if roomnum not in existing:
                    isexisting = False
                else:
                    roomnum = str(randint(200, 215))
                    if roomnum not in existing:
                        isexisting = False
                    else:
                        isexisting = True
    return roomnum


def findtime():
    """Returns time in format '<years> <months> <days> <hours>'"""
    while True:
        print("TERMS AND CONDITIONS\n")
        print("In case uncertain about stay higher charges of $10 per hour will be applicable")
        print("* Stay less than 3 hours -> $1000 fixed charge")
        print("* In case of extension of duration of stay, additional charges of $50 per hour will be applied.")
        print("* For early check-out, no refund.\n")
        print("Type **notsure** if you are uncertain")
        print("Format to enter: ____ years ____ months ____ days ____ hours")
        duration = inp(">")
        if "notsure" in duration:
            time = ""
        else:
            lis = duration.split()
            time = ""

            if "years" in lis:
                ind = lis.index("years")
                time += (lis[ind-1]+" ")
            else:
                time += "0 "

            if "months" in lis:
                ind = lis.index("months")
                time += (lis[ind-1]+" ")
            else:
                time += "0 "

            if "days" in lis:
                ind = lis.index("days")
                time += (lis[ind-1]+" ")
            else:
                time += "0 "

            if "hours" in lis:
                ind = lis.index("hours")
                time += lis[ind-1]
            else:
                time += "0"
        if time == "0 0 0 0":
            print("Invalid duration, please check any typos and enter again\n")
        else:
            break
    return time


# Final adding of data


def signup(uid, pwd, name, num, type, room_num, duration,
           checkin_time, price, purpose, service,
           about="customer", blocked="NO", con=False, cur=False):
    """Final signup - customer"""
    # Database
    if (not con) or (not cur):
        con, cur = m.MAKE_CONNECTION()
    if not(m.db_in_use(con, cur)):
        m.USE_DATABASE('Hotel_Luxury_Palace', con, cur)
    # Sign_up
    success = True    # assuming successful sign-up
    valid_uid, reason_uid = valid_usname(uid)
    valid_pass, reason_pwd = valid_pwd(pwd)
    if (not valid_uid) or (not valid_pass):   # in case it happens
        success = False
        return success
    value_d_1 = {'user_id':uid,
               'password':pwd,
               'name':name,
               'about':about,
               'number_of_people':num,
               'type':type,
               'room_num':room_num}
    value_d_2 = {'user_id':uid,
                 'duration':duration,
                 'checkin_time':checkin_time,
                 'price':price,
                 'purpose':purpose,
                 'service':service,
                 'blocked':blocked}
    s1 = m.INSERT_VALUES('Customer_Details',value_d_1,con,cur)
    s2 = m.INSERT_VALUES('Customer_Info',value_d_2,con,cur)
    if s1 and s2:
        success = True
    else:
        success = False
    return success


def offsignup(user, pwd, name, post, con = False, cur = False):
    """Final signup - official"""
    if (not con) or (not cur):
        con, cur = m.MAKE_CONNECTION()
    if not(m.db_in_use(con, cur)):
        m.USE_DATABASE('Hotel_Luxury_Palace', con, cur)
        
    value_d = {'user_id':user,
               'password':pwd,
               'name':name,
               'post':post}
    s = m.INSERT_VALUES('Official_Details',value_d,con,cur)
    return s


# Functions for taking input


def take_uid_pwd():
    print("Please enter your USERNAME:-", '\n')
    print('''VALIDITY OF USERNAME

            1. Should be unique
            2. No special symbols except _
            3. No Spaces''')
    valid_uid = False
    while not valid_uid:
        uid = inp(">")
        valid_uid, st = valid_usname(uid)
        if not valid_uid:
            print("INVALID USERNAME!")
            print(st)
    print("THANK YOU!", '\n')
    print("Please enter your PASSWORD:-", '\n')
    print("""VALIDITY OF PASSWORD

            1. At least 6 characters length
            2. At least 1 number
            3. At least 1 special character
            4. At least 1 lowercase
            5. At least 1 uppercase
            6. No Spaces
            """)
    v_pwd = False
    while not v_pwd:
        pwd = inp(">")
        v_pwd, st = valid_pwd(pwd)
        if not v_pwd:
            print("INVALID PASSWORD!")
            print(st)
    return uid, pwd


def take_purpose_service():
    import price
    print("Please enter the purpose of your visit")
    print("Press enter if don't want to mention")
    purpose = inp(">")
    if purpose == "":
        service = None    # Assuming user will not give purpose
        choice = 'n'
        while choice.lower() == 'n':
            print("We will not be able to provide you personalized service.. do you want continue without purpose?(y/n)")
            choice = inp(">")
            if choice.lower() == 'y':
                print("Account inputted without purpose, you can ask for updating it later")
                return purpose, service
            else:
                purpose = inp("Please enter purpose> ")
                if purpose != '':
                    choice = "y"
    print()
    print("Please enter the service you wish to have:-")
    services_available = price.services_available
    services_available['No Service'] = None
    i = 1
    l = []
    for k in services_available.keys():
        print(str(i)+'.'+k)
        l += [k]
        i += 1
    serv = inp(">", int)
    valid = False
    while not valid:
        if serv < 1 or serv > len(l):
            print("Please enter the purpose again")
        else:
            valid = True
    service = l[serv-1]
    return purpose, service


def ask():
    """Asks customer about all the details
       returns uid, pwd, num, TYPE, duration, purpose, service"""
    print()
    uid, pwd = take_uid_pwd()
    print("Thank You!", '\n')
    print("Please enter the number of people:-")
    num = str(inp(">", typ=int))
    print()
    print("Which type of accomodation would you like?")
    print("Press 1 for Luxury, 2 for Regular")	
    print("1.Luxury")
    print("2.Regular")
    from price import price_per_day_l, price_per_day_r,\
         price_per_month_l, price_per_month_r, price_per_year_l,\
         price_per_year_r, price_per_hour_l, price_per_hour_r
    print("\tThe prices are :-\n")
    print("\tLUXURY:-")
    print("\t\tPrice per hour: \u20B9", price_per_hour_l)
    print("\t\tPrice per day: \u20B9", price_per_day_l)
    print("\t\tPrice per month: \u20B9", price_per_month_l)
    print("\t\tPrice per year: \u20B9", price_per_year_l)
    print("\tREGULAR:-")
    print("\t\tPrice per hour: \u20B9", price_per_hour_r)
    print("\t\tPrice per day: \u20B9", price_per_day_r)
    print("\t\tPrice per month: \u20B9", price_per_month_r)
    print("\t\tPrice per year: \u20B9", price_per_year_r)
    print()
    choice_type = inp(">", typ=int)
    if choice_type == 1:
        TYPE = 'l'
    else:
        TYPE = 'r'
    duration = findtime()
    print()
    purpose, service = take_purpose_service()
    return uid, pwd, num, TYPE, duration, purpose, service


def ask_official(con, cur):
    """To ask official personnel
       returns: name,usr,pwd,post"""
    name = inp("Please enter your NAME: ")
    print("Welcome %s!"%name.upper(), '\n')
    usr = inp("Please enter USERNAME: ")
    validity, reason = valid_usname(usr)
    while not validity:
        print("INVALID USERNAME")
        print(reason)
        print()
        print("Please enter username again")
        usr = inp(">")
        validity, reason = valid_usname(usr)
    print("Username Accepted!", '\n')
    pwd = inp("Please enter PASSWORD: ")
    validity, reason = valid_pwd(pwd)
    while not validity:
        print("INVALID PASSWORD")
        print(reason)
        print()
        print("Please enter password again")
        pwd = inp(">")
        validity, reason = valid_pwd(pwd)
    print("Password Accepted!", '\n')
    post = inp("Please enter your POST: ")
    # Validity of post:-
    valid = False
    existing = m.SELECT('Official_Details',con,cur,col_names = ('post',))[1]
    while not valid:
        for row in existing:
            if row[0] == post:
                valid = False
                print("Post already occupied, please try again")
                post = inp(">")
                break
        else:
            valid = True
    print("Your post of %s has been accepted"%post, '\n')
    return usr, pwd, name, post
    
