""" ==============Login Module==============
   To login a user
   
   Functions-> search   : to simplify find_uid
               find_uid : if username exists
               about_uid: info about the account
               corr_pwd : input password according to tries
"""

# Imports

from helper import inp
import mysql_handler as m

# Make Connection with MySQL

con, cur = m.MAKE_CONNECTION()
m.USE_DATABASE('Hotel_luxury_palace',con,cur)

# misc
def search(existing, value):
    for row in existing:
        for column in row:
            if column == value:
                found = True
                break
            else:
                found = False
        if found:
            break
    else:
        found = False
    return found

# main

def find_uid(uid):
    """Finds if user id is present or not
       returns: found,T,auth"""
    existing1 = m.SELECT('Customer_Details',con,cur,('user_id',))[1]
    existing2 = m.SELECT('Official_Details',con,cur,('user_id',))[1]
    if search(existing1,uid):
        return True, "Customer"
    elif search(existing2,uid):
        return True, "Official"
    else:
        return False, ''


def about_uid(uid, _type):
    """ Gives all the data existing for the uid
        _type if either 'official' or 'customer'"""
    condition = "user_id='%s'"%uid
    if _type.lower() == "customer":
        L1 = m.SELECT('Customer_Details',con,cur,condition=condition)[1]
        L2 = m.SELECT('Customer_info',con,cur,condition=condition)[1]
        for row in L1:
            uid, pwd, name, about, num, Type, room_num = row
        for row in L2:
            uid, duration, checkin_time, price, purpose, service, blocked = row
        return (uid, pwd, name, about, num, Type, room_num,
                duration, checkin_time, price, purpose, service, blocked)
    elif _type.lower() == "official":
        L = m.SELECT('Official_Details',con, cur, condition=condition)[1]
        for row in L:
            uid, pwd, name, post = row
        return uid, pwd, name, post
    
    
def corr_pwd(user_id, pwd, orig_pwd, tries):
    logged = False
    if pwd == orig_pwd:
        return True
    print("Wrong Password")
    print("Please try again (Chances left: %u)"%tries)
    tries -= 1
    pwd = inp(">")
    while tries >= 0:
        if pwd != orig_pwd:
            print("Wrong Password")
            print("Please try again (Chances left: %u)"%tries)
            pwd = inp(">")
        else:
            print("Login Successful!")
            logged = True
            break
        tries -= 1
    else:  # Block Account
        from grievance import block_account
        block_account(user_id)
        print("=====================================================================")
        print("SORRY THIS ACCOUNT HAS BEEN BLOCKED, WE WILL TRY TO RESOLVE ISSUE ASAP")
        print("=====================================================================")
    return logged
