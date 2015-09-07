import datetime

def get_days_between(date_earlier, date_later):
    dates = []
    n_days = (date_later - date_earlier).days - 1
    for i in range(1, n_days + 1):
        date = date_earlier + datetime.timedelta(days=i)
        dates += [date]
    return dates
