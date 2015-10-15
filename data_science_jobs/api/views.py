from dateutil.parser import parse as parse_datetime
from django.http import JsonResponse
from data_science_jobs.data_aggregation.models import DailySummary

def parse_date(date_string):
    datetime = parse_datetime(date_string)
    return datetime.date()

def n_posts(request):
    date_strings = request.GET.getlist('dates[]')
    dates = [parse_date(date_string) for date_string in date_strings]
    output = []
    for date in dates:
        daily_summary = DailySummary.objects.get(date=date)
        output += [{'date': date.isoformat(), 'n_posts': daily_summary.n_posts}]
    return JsonResponse(output, safe=False)
