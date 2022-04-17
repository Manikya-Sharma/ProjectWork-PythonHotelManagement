"""============grievances Module============
   To recieve, show and resolve grievances
   L = [<uid>,<grievance>,<post>]
"""

# Imports

from helper import inp
import mysql_handler as m

# Global Declarations

con, cur = m.MAKE_CONNECTION()
m.USE_DATABASE('Hotel_Luxury_Palace', con, cur)
L = []    # In order to store [<uid>,<grievance>,<post>]

# Obtain Grievances from customer

def obtain_grievance(user_id):
    """ To input grievance from customer"""
    print("Please enter your grievance in brief:-")
    grievance = inp(">")
    print("Which authority to address?")
    
    # Existing official accounts

    existing = m.SELECT('Official_Details', con, cur, ('name','post','user_id'))[1]
    L_names = []
    L_posts = []
    L_uids = []
    for row in existing:
        L_names.append(row[0])
        L_posts.append(row[1])
        L_uids.append(row[2])
    i = len(L_names)
    print('1. General Grievance')
    for x in range(2, i+2):
        print("%u. %s (%s)"%(x, L_names[x-2], L_posts[x-2]))

    # Obtain the official
    
    print("Enter your choice")
    choice = inp(">", int)
    valid = False
    while not valid:
        if choice >=1 and choice <=(i+1):
            valid = True
            break
        else:
            valid = False
            print("Please enter valid input")
            choice = inp(">")
    if choice == 1:
        name = "_GENERAL_"
        post = "_GENERAL_"
    else:
        post = L_posts[choice-2]
        uid = L_uids[choice-2]

    # Add value to the table
    
    value_d = {'user_id':user_id, 'grievance':grievance, 'official_post':post}
    success = m.INSERT_VALUES('Grievances', value_d, con, cur)
    if not success:
        print("Some error occured, please try again later")
    
# Resolving grievances

    # Miscellenous


def get_grievances(post):
    """ Returns grievances as a dict"""
    global L
    L.append(post)
    existing = m.SELECT('Grievances', con, cur)[1]
    nested_list = []
    for row in existing:
        if (row[2].lower() == post.lower()) or ("general" in row[2].lower()):
            nested_list.append([row[0],row[1]]) #[[userid, grievance],[...]]
    return nested_list

def show_grievances(lis):
    """ It will print the existing grievances and obatin grievance_type
        lis : nested list containing [[userid, grievance],[...]] format"""
    global L
    if len(lis) == 0:
        print("Congratulations, you have no grievances!")
        L = ['NONE','NONE','NONE']
        return None,None,None
    print("Your grievances:-")
    L_uid, L_gr = [], []
    i = 1
    for row in lis:
        user_id, grievance = row
        L_uid.append(user_id)
        L_gr.append(grievance)
        print("%u. %s"%(i,grievance))
        print("FROM -- %s"%(user_id))
        i += 1
    print("Would you like to resolve any grievance?(y/n)")
    ch = inp(">")
    if ch.lower() == "n":
        L = ['NONE','NONE','NONE']
        return None, None, None
    print("Which grievance to be resolved (please enter grievance number)")
    valid = False
    while not valid:
        num = inp(">", typ=int)
        if num > 0 and num <= i:
            valid = True
        else:
            valid = False
            continue
        num -= 1
        user_id = L_uid[num]
        L.insert(0,user_id)
        grievance = L_gr[num]
        L.insert(1,grievance)
        L2 = m.SELECT('Customer_Details', con, cur, ('name','room_num'),'user_id = \'%s\''%user_id)[1]
        for row in L2:
            name = row[0]
            room_num = row[1]
        print("\nGRIEVANCE OF --", name)
        print()
        print("How would you like to resolve?")
        print("1. Call plumber")
        print("2. Call Electrician")
        print("3. Call room service")
        print("4. Update the data of an account")
        print("5. Unblock an account")
        print("6. Pass grievance to other relevant authority")
        print("7. Report the grievance as spam")
        valid_2 = False
        while not valid_2:
            valid_2 = True
            ch = inp(">")
            if ch == "1":  
                grievance_type = "Plumber"
            elif ch == "2":
                grievance_type = "Electrician"
            elif ch == "3":
                grievance_type = "Room Service"
            elif ch == "4":
                grievance_type = "Update Account"
            elif ch == "5":
                grievance_type = "Unblock Account"
            elif ch == "6":
                grievance_type = "Pass On"
            elif ch == "7":
                grievance_type = "Spam"
            else:
                valid_2 = False
                print("Please enter a valid option")
    return grievance_type, name, room_num


    # Resolution of grievances

        # Sub-functions to resolve

def update_acc(uid):
    """ In order to update the account of a customer"""
    header1, values1, types1 = m.SELECT('Customer_details', con, cur,
                                        condition = "user_id = '%s'"%uid)
    header2, values2, types2 = m.SELECT('Customer_info', con, cur,
                                        condition = "user_id = '%s'"%uid)
    print("Which value to be modified?")
    L_vals = []
    i = 0
    for column in header1:
        print('%u. %s'%(i+1,column))
        L_vals.insert(i, column)
        i += 1
    for column in header2:
        if column == 'user_id':
            continue    # Already taken in first table
        print('%u. %s'%(i+1,column))
        L_vals.insert(i, column)
        i += 1
    i += 1    # Because values printed starting from 1
    x = inp('>',int)
    valid = False
    while not valid:
        valid = True
        if x in range(1,x+1):
            c_name = L_vals[x-1]
            try:
                ind = header1.index(c_name)
                first = True
            except ValueError:
                ind = header2.index(c_name)
                first = False
            if first:
                for row in values1:
                    value = row[ind]
                typ = types1[ind]
            else:
                for row in values2:
                    value = row[ind]
                typ = types2[ind]
        else:
            print("Invalid input, try again")
            valid = False
    print("DATA TYPE OF %s = %s"%(c_name,typ))
    print("OLD DATA = %s"%(value))
    print("Please enter the new value, take care of data type")
    new_value = inp(">")
    if first:
        stmt = "UPDATE Customer_Details SET %s = "%c_name
    else:
        stmt = "UPDATE Customer_Info SET %s = "%c_name
    if 'char' in typ.lower():
        stmt += '\'%s\''%new_value + ' '
    else:
        stmt += new_value + ' '
    stmt += "WHERE user_id = '%s';"%uid
    return m.UPDATE(stmt, con, cur)


def unblock_account(uid):
    stmt = "UPDATE customer_info SET blocked = 'NO' where user_id="+'\''+uid+'\''+";"
    return m.UPDATE(stmt, con, cur)


def block_account(uid):
    stmt = "UPDATE customer_info SET blocked = 'YES' where user_id="+'\''+uid+'\''+";"
    # Add it as a grievance by default
    value_d = {'user_id':uid,'grievance':'BLOCKED ACCOUNT','official_post':'_GENERAL_'}
    m.INSERT_VALUES('grievances', value_d, con, cur)
    return m.UPDATE(stmt, con, cur)


def pass_on(uid, grievance, post):
    print("Which authority to address?")
    
    # Existing official accounts

    existing = m.SELECT('Official_Details', con, cur, ('name','post','user_id'))[1]
    L_names = []
    L_posts = []
    L_uids = []
    for row in existing:
        L_names.append(row[0])
        L_posts.append(row[1])
        L_uids.append(row[2])
    i = len(L_names)
    print('1. General Grievance')
    for x in range(2, i+2):
        print("%u. %s (%s)"%(x, L_names[x-2], L_posts[x-2]))

    # Obtain the official
    print("Enter your choice")
    choice = inp(">", int)
    while choice>=1 and choice <=(i+1):
        if choice == 1:
            name = "_GENERAL_"
            new_post = "_GENERAL_"
        else:
            new_post = L_names[choice-2]
            uid = L_uids[choice-2]
        break
    stmt = "UPDATE grievances SET official_post = '%s' where (user_id='%s' and \
grievance='%s' and official_post='%s');"%(new_post, uid, grievance, post)
    return m.UPDATE(stmt, con, cur)


def delete_grievance(user_id, grievance, post):
    stmt = "DELETE FROM grievances WHERE (user_id = '%s' and \
grievance = '%s' and (official_post in ('%s','_GENERAL_')));"%(user_id, grievance, post)
    return m.UPDATE(stmt, con, cur)

        # Final resolution

        
def resolve(grievance_type, uid, room_num):
    global L
    uid, grievance, post = L
    done = True
    if grievance_type == "Plumber":  
        print("Plumber called for room number",room_num)
    elif grievance_type == "Electrician":
        print("Electrician called for room number",room_num)
    elif grievance_type == "Room Service":
        print("Room service called for room number",room_num)
    elif grievance_type == "Update Account":
        done = update_acc(uid)
        if done:
            print("Update Succesful")
        else:
            print("Update unsuccessful, plee try again")
    elif grievance_type == "Unblock Account":
        done = unblock_account(uid)
        if done:
            print("Account unblocked successfully")
        else:
            print("Unsuccesful, please try again later")
    elif grievance_type == "Pass On":
        done = pass_on(uid, grievance, post)
        if done:
            print("Grievance passed on")
        else:
            print("Some problem occured, please try again")
    elif grievance_type == "Spam":
        delete_grievance(uid, grievance, post)
        print("The spam grievance has been removed successfully")
    elif grievance_type == "NONE":
        return False
    else:
        print("There was an error!")
        return False
    return True

# Main program

    # For officials
def central_link(post):
    """ This function makes final link for all above """
    global L
    d = get_grievances(post)
    grievance_type, name, room_num = show_grievances(d)
    user_id, grievance, post = L
    if user_id == grievance == post == "NONE":  # No grievance selected
        return
    success = resolve(grievance_type, user_id, room_num)
    if success:
        delete_grievance(user_id, grievance, post)
        L = []    # To ensure list not still containg info before adding next datas
    else:
        print("No grievance resolved")
