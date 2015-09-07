import datetime
import data_science_jobs
from django.test import TestCase

class GetDaysBetweenTest(TestCase):

    def test_main(self):

        date1 = datetime.datetime(2015, 9, 10).date()
        date2 = datetime.datetime(2015, 9, 15).date()
        
        days_between = data_science_jobs.get_days_between(date1, date2)

        expected_days_between = [
            datetime.datetime(2015, 9, 11).date(),
            datetime.datetime(2015, 9, 12).date(),
            datetime.datetime(2015, 9, 13).date(),
            datetime.datetime(2015, 9, 14).date(),
        ]
        self.assertEqual(days_between, expected_days_between)

class GetMonthsBetweenTest(TestCase):

    def test_gets_months_between_dates(self):

        date1 = datetime.datetime(2015, 9, 10).date()
        date2 = datetime.datetime(2015, 9, 15).date()
        
        months_between = data_science_jobs.get_months_between(date1, date2)

        expected_months_between = []
        self.assertEqual(months_between, expected_months_between)

    def test_get_months_between_difference_months(self):
        date1 = datetime.datetime(2015, 7, 10).date()
        date2 = datetime.datetime(2015, 9, 15).date()
        
        months_between = data_science_jobs.get_months_between(date1, date2)

        expected_months_between = [datetime.datetime(2015, 8, 1).date()]
        self.assertEqual(months_between, expected_months_between)

        
