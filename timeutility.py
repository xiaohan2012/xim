from datetime import datetime,timedelta

def get_range_from_string(tstr):
    """
    get time range from string => get_tr_fstr
    `tstr` can be:
        today
        yesterday

        week
        month

        last n days
        last n weeks
        last n months
    """
    time_diff_dict = {
        "today" : timedelta(days = 0),
        "yesterday" : timedelta(days = 1),
        "week" : timedelta(days = 7),
        "month" : timedelta(days = 30),
    }

    time_diff = time_diff_dict[tstr] 

    to_t = datetime.now()
    to_t = datetime(to_t.year,to_t.month,to_t.day)
    from_t = to_t  - time_diff
    to_t = datetime(to_t.year,to_t.month,to_t.day) + timedelta(days = 1)

    print from_t,to_t

    return from_t,to_t

