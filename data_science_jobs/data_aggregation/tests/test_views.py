import json
import datetime
from django.utils import timezone
from data_science_jobs.data_aggregation.models import DailySummary
from django.test import TestCase

class TestDailySummaryView(TestCase):

    def test_main(self):

        date1 = datetime.datetime(year=2015, month=9, day=6).date()
        n_posts1 = 5
        date2 = datetime.datetime(year=2015, month=9, day=5).date()
        n_posts2 = 3
        
        daily_summary1 = DailySummary.objects.create(date=date1, n_posts=n_posts1)
        daily_summary2 = DailySummary.objects.create(date=date2, n_posts=n_posts2)
        
        response = self.client.get('/daily-summary')
        response = json.loads(response.content)

        expected_response = [
            {
                'date': str(date1),
                'n_posts': 5,
            },
            {
                'date': str(date2),
                'n_posts': 3,
            },
        ]
        
        self.assertEqual(response['status'], 200)
        self.assertEqual(response['content'], expected_response)
    
