import sys

import arrow


def parse_date_str(date_str=None):
    """
    The date_str is interpreted as follows:

    * if None the current day is returned

    * "today" is an alias of "m0", see below for meaning

    * a string starting with m is always parsed as "m<number>" (e.g. m1, m3,
      etc.). it is then interpreted as <number> days before today, so "m1" is
      yesterday (minus 1), "m2" is the day before (minus 2), etc.

    * a string of length one or two is always parsed as a number, which is then
      interpreted as the nth day of the current month. so 1, 11, 12, etc. is the
      1st, 11th and 12th of the current month.

    * a string of length 4 is always parsed as MMDD

    * a string of length 8 is always parsed as YYYYMMDD

    * all other inputs result in an error and the program exiting.

    :param date_str: The date string to be parsed
    :return: An Arrow instance pointing to the parsed date
    """
    arr = arrow.now()
    if date_str is not None:
        # make "today" an alias for "m0", which is the same ;)
        if date_str == "today":
            date_str = "m0"
        if date_str[0] == "m":
            arr = arr.replace(days=-int(date_str[1:]))
        elif len(date_str) < 3:
            arr = arr.replace(day=int(date_str))
        elif len(date_str) == 4:
            arr = arr.replace(month=int(date_str[0:2]), day=int(date_str[2:]))
        elif len(date_str) == 8:
            arr = arr.replace(year=int(date_str[0:4]),
                              month=int(date_str[4:6]),
                              day=int(date_str[6:]))
        else:
            print("ERROR: Cannot parse date string '{}'!".format(date_str))
            sys.exit(-2)
    return arr.floor('day')


def parse_time_str(start):
    """
    Parses a string as HHMM and returns it as (HH, MM) tuple.

    :param start: The string to be parsed.
    :return: The parsed (int, int) tuple
    """
    if len(start) != 4:
        print("ERROR: start time *must* be in the form '1234'. Aborting.")
        sys.exit(-2)
    return int(start[0:2]), int(start[2:])


def parse_date_and_time_str(datestr: str, timestr: str) -> arrow.Arrow:
    """
    Creates an arrow object from a datestr and a timestr, so we get a day
    and an hour and a minute set.

    :param datestr: The datestring to parse
    :param timestr: The timestring to parse
    :return: Arrow object
    """
    date_obj = parse_date_str(datestr)
    start_h, start_m = parse_time_str(timestr)
    return date_obj.floor('day').replace(hour=start_h, minute=start_m)
