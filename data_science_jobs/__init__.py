import datetime

def get_days_between(date_earlier, date_later):
    dates = []
    n_days = (date_later - date_earlier).days - 1
    for i in range(1, n_days + 1):
        date = date_earlier + datetime.timedelta(days=i)
        dates += [date]
    return dates

def get_months_between(date_earlier, date_later):
    months = []
    date_earlier = date_earlier - datetime.timedelta(days=date_earlier.day -1)
    date_later = date_later - datetime.timedelta(days=date_later.day -1)
    while True:
        date_later = date_later - datetime.timedelta(days=1)
        date_later = date_later - datetime.timedelta(days=date_later.day -1)
        if date_later > date_earlier:
            months += [date_later]
        else:
            break
    months.reverse()
    return months
    
