"""         =========MySQL Connection Handler========

    In order to make basic CRUD oprations in mysql database.
    Special functions also for output

   """

import mysql.connector


# Miscellaneous functions:-


def output_table(header, L_rows, separator = '  '):
    """ A function to display formatted output of a table"""
    L_lens = []
    for i in range(len(header)):
        L_col = []
        for row in L_rows:
            if row[i]:
                L_col.append(len(row[i]))
            else:
                L_col.append(0)
        L_lens.append(max(L_col))
    for i in L_lens:
        ind = L_lens.index(i)
        if i < len(header[ind]):
            L_lens[ind] = len(header[ind])    # For longer columns than values
    #
    l_sep = len(separator)
    total_length = sum(L_lens) + (len(L_lens)+1)*l_sep
    print("-"*total_length, sep = '')
    #
    k = 0
    print(separator, end = '')
    for j in L_lens:
        print(f'%{j}s'%header[k].ljust(j), sep = '', end = separator)
        k += 1
    print("\n", "-"*total_length, sep = '')
    for row in L_rows:
        print(separator, end = '')
        i = 0
        for column in row:
            magnitude = L_lens[i]
            if column is not None:       # ljust not defined for None
                print(f'%{magnitude}s'%(column).ljust(magnitude), end = separator)
            else:
                print(f'%{magnitude}s'%(column), end = separator)
            i += 1
        print()
    print("-"*total_length, sep = '')


def db_in_use(con, cur):
    """ To show the database currently in use"""
    try:
        cur.execute('SELECT DATABASE();')
        db = cur.fetchone()[0]
        return db
    except:
        return None


# Functions related to MySQL:-


def MAKE_CONNECTION():
    """ In order to make a connection, return ConnectorObject and Cursor"""
    con = mysql.connector.connect(host='localhost', user='root', password='tiger')  
    cur = con.cursor()
    return con, cur

    
def SHOW_DATABASES(con, cur):
    """ To return the databases already existing in form of list"""
    dbs = cur.execute("SHOW DATABASES;")
    return cur.fetchall()


def CREATE_DATABASE(db_name, con, cur):
    """ To create a database with the name `db_name`
        returns False in case db_name might already exist"""
    if db_name in SHOW_DATABASES(con, cur):
        return False
    stmt = "CREATE DATABASE " + db_name.strip() + ';'
    try:
        cur.execute(stmt)
        con.commit()
    except:
        return False
    else:
        return True


def USE_DATABASE(db_name, con, cur):
    """ To use a particular database
        creates the database in case it does not exists"""
    if db_name.lower() not in SHOW_DATABASES(con, cur):
        CREATE_DATABASE(db_name, con, cur)
    stmt = "USE " + db_name.strip() + ';'
    try:
        cur.execute(stmt)
    except:
        return False
    else:
        return True


def SHOW_TABLES(con, cur):
    """ To show the tables already existing
        returns False if no database selected
        else returns list of tables"""
    db = db_in_use(con, cur)
    if not db:    # Database is not selected
        #USE_DATABASE(db, con, cur)    # It will automatically deal in this case
        return False
    stmt = "SHOW TABLES;"
    try:
        cur.execute(stmt)
    except:
        return False
    else:
        tables = cur.fetchall()
        newL = []
        for row in tables:
            for column in row:
                newL.append(column)
        return newL

    
def CREATE_TABLE(name, columns, con, cur):
    """ To create a table with name `name` and columns described below
        `columns` is a dictionary with elements in form <column_name>:(<data_type>[,constraints])
        e.g. {'id':('int(2)','not null', 'primary key'), 'name':('varchar(20)',)}
        returns False in case table already exists
    """
    db = db_in_use(con, cur)
    tables = SHOW_TABLES(con, cur)
    if name in tables:
        return False
    c_name = list(columns.keys())
    c_type = []
    c_constraint = []
    for val in columns.values():
        data_type = val[0]
        try:
            constraint = val[1]
        except IndexError:
            constraint = None
        c_type.append(data_type)
        c_constraint.append(constraint)
    stmt = "CREATE TABLE " + name.strip() + "( "
    i = 0
    while i<len(c_name):
        stmt += c_name[i] + ' '
        stmt += c_type[i] + ' '
        if c_constraint[i]:
            stmt += c_constraint[i] + ', '
        else:
            stmt += ', '
        i += 1
    else:
        stmt = stmt[:-2]    # This is to remove the last comma before closing brackets
    stmt += ');'
    try:
        cur.execute(stmt)
        con.commit()
    except:
        return False
    else:
        return True


def DESCRIBE_TABLE(name, con, cur, out = False):
    """ returns the list of table structure
        if out=True, will also print the structure"""
    db = db_in_use(con,cur)
    if not db:
        # No database has been selected till now
        return False, False
    if name.lower() not in SHOW_TABLES(con, cur):
        # No table named `name` found
        return False, False
    stmt = "DESC " + name.strip() + ";"
    cur.execute(stmt)
    records = cur.fetchall()
    L_rows = []
    L_lens = []
    for row in records:
        L_col = []
        for column in row:
            L_col.append(column)
        L_rows.append(L_col)
    for i in range(6):
        t = ()
        for row in L_rows:
            if row[i] is not None:
                if row[i].isspace():
                    t += (1, )
                else:
                    t += (len(row[i]),)
            else:
                t += (1,)
    t = ('Field','Type','Null','Key','Default','Extra')
    if out:
        output_table(t, L_rows)
    return t, L_rows
    

def INSERT_VALUES(table_name, value_d, con, cur):
    """ It will add values to a table
        value_d is a dict in form {column_name: value} - columns missing will be taken as Null
        returns False in case table not already existing or no database selected or some error"""
    db = db_in_use(con, cur)
    if not db:
        return False
    tables = SHOW_TABLES(con, cur)
    if table_name.lower() not in tables:
        return False
    t, L_rows = DESCRIBE_TABLE(table_name, con, cur)
    L_types = []
    for row in L_rows:
        _type = row[1]
        L_types.append(_type)    # This stores data type of all fields
    stmt = "INSERT INTO " + table_name.strip() + "("
    for key in value_d.keys():
        stmt += key + ', '
    stmt = stmt[:-2] + ") VALUES("
    i = 0    # We need to iterate acc to data type
    for val in value_d.values():
        if val == None:
            val = ''    # To avoid error in concatenation
        # type :-
        _type = L_types[i]
        if _type.lower() == "date":
            quotes = True
        elif 'char' in _type.lower():
            quotes = True
        else:
            quotes = False
        # statement :-
        if not quotes:
            stmt += str(val) + ', '
        else:
            stmt += "\'" + val + "\', "
        i += 1
    stmt = stmt[:-2]+');'
    try:
        cur.execute(stmt)
        con.commit()
    except:
        return False
    else:
        return True

    
def SELECT (table_name, con, cur, col_names = (),
            condition = '', group = '', having = '',
            order = '', order_type = 'ASC', output = False,
            separator = '  '):
    """ Function to select values according to conditions
        output = True will also print the values """
    db = db_in_use(con, cur)
    if not db:
        print('no db')
        return False
    tables = SHOW_TABLES(con, cur)
    if table_name.lower() not in tables:
        print('no table')
        return False
    stmt = "SELECT "
    if len(col_names):
        # header
        header = list(col_names)
        # types
        types = []
        L_2 = DESCRIBE_TABLE(table_name, con, cur)[1]
        for _row in L_2:
            types.append(_row[1])
        # stmt
        for col in col_names:
            stmt += col.strip() + ', '
        stmt = stmt[:-2]
    else:
        # header and types
        header = []
        types = []
        L_2 = DESCRIBE_TABLE(table_name, con, cur)[1]
        for _row in L_2:
            header.append(_row[0])
            types.append(_row[1])
        # stmt
        stmt += '*'
    stmt += " FROM " + table_name.strip()
    if bool(condition):
        stmt += " WHERE " + condition.strip()
    if bool(group):
        stmt += " GROUP BY " + group.strip()
    if bool(having):
        stmt += " HAVING " + having.strip()
    if bool(order):
        stmt += " ORDER BY " + order.strip()\
                + ' ' + order_type
    stmt += ';'
    try:
        cur.execute(stmt)
    except:
        return False
    else:
        L = cur.fetchall()
        L_rows = []
        for row in L:
            col = []
            for column in row:
                col.append(str(column))
            L_rows.append(col)
        if output:
            output_table(header, L_rows, separator = separator)
        return header,L_rows,types
        

def UPDATE(stmt, con, cur):
    """ In order to update/delete the contents of a table,
        since this function is too specific, add statement according to situation"""
    try:
        cur.execute(stmt)
        con.commit()
    except:
        return False
    else:
        return True


def ALTER(stmt, con, cur):
    """ In order to alter the structure of a table,
        since this function is rarely used, add statement according to situation"""
    try:
        cur.execute(stmt)
        con.commit()
    except:
        return False
    else:
        return True


def TRUNCATE_TABLE(table_name, con, cur):
    """ In order to truncate the contents of table without affecting data structure"""
    db = db_in_use(con, cur)
    if not db:
        return False
    tables = SHOW_TABLES(con, cur)
    if table_name.lower() not in tables:
        return False
    stmt = "TRUNCATE TABLE " + table_name + ";"
    try:
        cur.execute(stmt)
        con.commit()
    except:
        return False
    else:
        return True


def DROP_TABLE(table_name, con, cur):
    """ In order to drop the table"""
    db = db_in_use(con, cur)
    if not db:
        return False
    tables = SHOW_TABLES(con, cur)
    if table_name.lower() not in tables:
        return False
    stmt = "DROP TABLE " + table_name + ";"
    try:
        cur.execute(stmt)
        con.commit()
    except:
        return False
    else:
        return True

    
def DROP_DATABASE(db_name, con, cur):
    """ In order to drop the database"""
    stmt = "DROP DATABASE " + db_name + ";"
    try:
        cur.execute(stmt)
        con.commit()
    except:
        return False
    else:
        return True
