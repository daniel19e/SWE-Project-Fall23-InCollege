from os import name, system, get_terminal_size
import re
from datetime import datetime, timedelta
import pytz

def format_date(date_str):
    # Parse the input date string into a datetime object
    input_date = datetime.strptime(date_str, "%Y-%m-%d")
    utc = pytz.utc.localize(input_date)
    est = pytz.timezone("US/Eastern")
    input_date = utc.astimezone(est)
    today = datetime.now().date()
    if input_date.date() == today:
        return "Today at"
    elif input_date.date() == today - timedelta(days=1):
        return "Yesterday at"
    else:
        return input_date.date()
       
def compute_utc_to_est_offset():
    est = pytz.timezone('US/Eastern')
    offset = est.utcoffset(datetime.utcnow())
    seconds = (offset.days * 86400) + offset.seconds
    return seconds // 3600 # hours

def convert_24_hour_to_12_hour(time_str):
    time_str = time_str[:5] # get rid of seconds
    time_obj = datetime.strptime(time_str, "%H:%M")
    est = time_obj + timedelta(hours=compute_utc_to_est_offset())
    time_12_hour_format = est.strftime("%I:%M %p")
    return time_12_hour_format

def clear_terminal():
  _ = system('cls') if name == 'nt' else system('clear')

def inspect_input(input):
  cancel = (input.upper() == 'X')
  return cancel

def format_string(s):
    '''Returns the string with only the first letter of each word capitalized and the rest lowercase.'''
    return ' '.join(word.capitalize() for word in s.split())


def validate_date(input_date):
    '''Check if the date matches the YYYY-MM-DD format.'''
    if not input_date:
        return True  # Empty string is considered valid here.
    pattern = re.compile("^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
    return bool(pattern.match(input_date))

def input_with_prefill(prompt, prefill=''):
    '''Input function to handle default text.'''
    if prefill:
        user_input = input(f"{prompt} [{prefill}]: ").strip()
        return user_input or prefill
    return input(prompt).strip()