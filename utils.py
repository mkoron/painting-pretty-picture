'''
Various utility functions.
'''
from datetime import datetime, timedelta


def formatter(number):
    '''
    Format a decimal year into a mm-yyyy data type
    '''
    year = int(number)
    d = timedelta(days=(number - year) * 365)
    day_one = datetime(year, 1, 1)
    date = d + day_one

    return str(date.month) + '-' + str(date.year)
