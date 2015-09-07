import datetime
import mock
from data_science_jobs.models import JobListing
from data_science_jobs.data_aggregation.models import DailySummary, MonthlySummary
from django.test import TestCase

class DailySummaryTest(TestCase):

    @mock.patch('data_science_jobs.data_aggregation.models.JobListing')
    def test_create_initialises_n_posts(self, mock_JobListing):

        mock_date = mock.Mock()
        mock_n_posts = mock.Mock()
        mock_get_n_posts = mock.Mock()
        mock_get_n_posts.return_value = mock_n_posts
        mock_JobListing.get_n_posts = mock_get_n_posts

        daily_summary = DailySummary.create(mock_date)

        mock_get_n_posts.assert_called_once_with(mock_date)
        self.assertEqual(daily_summary.n_posts, mock_n_posts)

class GetLastSummaryTest(TestCase):

    def test_returns_last_summary(self):

        summary1 = DailySummary.create(date=datetime.datetime(2015, 9, 1))
        summary1.save()
        summary2 = DailySummary.create(date=datetime.datetime(2015, 9, 2))
        summary2.save()
        summary3 = DailySummary.create(date=datetime.datetime(2015, 8, 20))
        summary3.save()

        summary = DailySummary.get_last_summary()

        self.assertEqual(summary, summary2)

    def test_returns_none_if_no_summaries(self):

        summary = DailySummary.get_last_summary()

        self.assertIsNone(summary)
