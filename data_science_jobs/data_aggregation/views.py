from django.utils import timezone
from data_science_jobs.data_aggregation.models import DailySummary
from django.http import HttpResponse, JsonResponse

def daily_summary(request):

    content = []
    for daily_summary in DailySummary.objects.all():
        x = {
            'date': str(daily_summary.date),
            'n_posts': daily_summary.n_posts,
        }
        content += [x]
    
    return JsonResponse({
        'status': 200,
        'content': content,
    })
