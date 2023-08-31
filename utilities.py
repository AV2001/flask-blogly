from datetime import datetime


def get_current_date_time():
    '''
    Returns the current date time in the following format:
    Sun Feb 4 2018, 11:30 AM
    '''
    now = datetime.now()
    return now.strftime('%a %b %d %Y, %I:%M %p')
