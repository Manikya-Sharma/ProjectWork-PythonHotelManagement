"""============PRICING MODULE============
   Will identify the prices for a user
   l - luxury
   r - regular
   For extra days than mentioned, price is [price_per_hour_l]+50 for each month
   For no duration mentioned, price is [price_per_hour_l]+10 for each month
"""

from helper import inp

# CONSTANTS :-

disc_d = {"CODE1": 'guest', "CODE2": 'online', "CODE3": 'official_family'}
disc_prices = {'guest': 100.0, 'online': 10.0, 'official_family': 70.0}
services_available = {'Tourism': 1500.0, 'Online Meetings': 3000.0}

price_per_day_l = 1000
price_per_day_r = 500
price_per_month_l = 100000
price_per_month_r = 50000
price_per_year_l = 10000000
price_per_year_r = 500000
price_per_hour_l = 200
price_per_hour_r = 150

# Functions :-

def service_price(service):
    """ Will return price applicable according to service"""
    price = services_available.get(service)
    if price is None:  # No service applicable
        price = 0.0
    return price


def ask_discount():
    """To ask for discount"""
    print("Do you have code for discount?(y/n)")
    ch = inp(">")
    if ch.lower() == 'y':
        code = inp("Enter the discount code: ")
        auth = disc_d.get(code)
        if auth is not None:
            print("Code Approved")
        else:
            print("Code not Approved, please try again later")
    else:
        auth = 'customer'    # No code therefore general case
    return auth


def findprice(duration, TYPE):
    """To determine the price according to duration
    Doesnt take into account the extra prices
    *** duration to be in form of str as: <years> <months> <date> <hours>"""
    if duration == '':
        return 0  # Will be evaluated during check_out
    l = duration.split()

    # data from duration
    years = int(l[0])
    months = int(l[1])
    days = int(l[2])
    hours = int(l[3])

    if TYPE == 'l':
        yearly_cost = years * price_per_year_l
        monthly_cost = months * price_per_month_l
        daily_cost = days * price_per_day_l
        hourly_cost = hours * price_per_hour_l
    else:
        yearly_cost = years * price_per_year_r
        monthly_cost = months * price_per_month_r
        daily_cost = days * price_per_day_r
        hourly_cost = hours * price_per_hour_r

    total_cost = yearly_cost + monthly_cost + daily_cost + hourly_cost
    
    return total_cost


def discount(auth):
    """It will identify the discount applicable as per the authority of the customer
    returns discount as a percentage in form of float"""
    if auth in disc_prices.keys():
        discount = disc_prices.get(auth)
    else:
        discount = 0.0    # 0% discount
    return discount


def prices(duration, service, TYPE, num):
    auth = ask_discount()
    total_price = findprice(duration, TYPE)
    disc = discount(auth)
    service_p = service_price(service)
    final_price = num*(total_price - (total_price*(disc/100)) + service_p)
    # The final price decided
    return final_price, auth


def isleap(year):
    if year%400 == 0:
        leap = True
    else:
        if year%100 == 0:
            leap = False
        else:
            if year%4 == 0:
                leap = True
            else:
                leap = False
    return leap


def evaluate_price(price, checkin_time, duration):
    """To evaluate the final price to be payed during check-out"""
    import time
    global price_per_hour_l    # Reference for higher charges
    try:
        price = float(price)
    except ValueError:  # in case that happens - only possible if official changed it and is final
        return price
    now_time = time.localtime()
    checkout_time = time.strftime("%Y %m %d %H ", now_time)  # this will structure time
    l_in = checkin_time.split()
    l_out = checkout_time.split()
        # to type cast string to int
    for el in l_in:
        l_in.remove(el)
        el = int(el)
        l_in.insert(0, el)
    for el in l_out:
        l_out.remove(el)
        el = int(el)
        l_out.insert(0, el)
    year_diff = l_in[0] - l_out[0]
    month_diff = l_in[1] - l_out[1]
    day_diff = l_in[2] - l_out[2]
    hour_diff = l_in[3] - l_out[3]

    # actual_dur = "%u %u %u %u"%(year_diff,month_diff,day_diff,hour_diff)
    # This is the actual duration

    if l_out[1] in (1, 3, 5, 7, 8, 10, 12):
        month_days = 31
    elif l_out[1] in (2, 4, 6, 9, 11):
        month_days = 30
    else:  # in case
        month_days = 30

    if isleap(l_out[0]):
        year_days = 366
    else:
        year_days = 365
        
    actual_hours = hour_diff + day_diff*24 + month_diff*month_days + year_diff*year_days
    if duration == "":    # No duration was mentioned
        # Higher charges to be payed
        if actual_hours < 2:  # Stayed for very short duration
            price = 1000
        else:
            price = actual_hours*(price_per_hour_l+10)
        return price

    l_dur = duration.split()
    hour = int(l_dur[0])
    month = int(l_dur[1])
    day = int(l_dur[2])
    year = int(l_dur[3])
        
    if l_in[1] in (1, 3, 5, 7, 8, 10, 12):
        month_days = 31
    elif l_in[1] in (2, 4, 6, 9, 11):
        month_days = 30
        
    if isleap(l_in[0]):
        year_days = 366
    else:
        year_days = 365
    hours = hour + day*24 + month*month_days + year*year_days

    if actual_hours > (hours+24):    # Spent more time, even more than a day
        # Very high price to be charged
        price_per_hour_l += 50
        extra_charges = (actual_hours-hours)*price_per_hour_l
        price += extra_charges
    # If spent same or less time, no extra charges
    return price
