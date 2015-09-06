import mock
import datetime
from data_science_jobs.models import JobListing
from data_science_jobs.data_aggregation import background
from data_science_jobs.data_aggregation.models import DailySummary
from django.test import TestCase

class UpdateDailySummariesTest(TestCase):

    def test_main(self):

        job1 = JobListing.objects.create(
            jobid=1,
            title='title1',
            description='description1',
            added=datetime.datetime(year=2015, month=9, day=1).date())
        
        job2 = JobListing.objects.create(
            jobid=2,
            title='title2',
            description='description2',
        added=datetime.datetime(year=2015, month=9, day=2).date())
        
        background.update_daily_summaries()
        
        daily_summary1 = DailySummary.objects.first()
        daily_summary2 = DailySummary.objects.last()
    
        self.assertEqual(daily_summary1.date, job1.added)
        self.assertEqual(daily_summary2.date, job2.added)
        self.assertEqual(daily_summary1.n_posts, 1)
        self.assertEqual(daily_summary2.n_posts, 1)

    @mock.patch('data_science_jobs.data_aggregation.models.DailySummary')
    @mock.patch('data_science_jobs.get_days_between')
    @mock.patch('data_science_jobs.scraping.models.Session.get_previous_session')
    def test_unit(self, mock_get_previous_session, mock_get_days_between, mock_DailySummary):

        # find the date of the last scraping session
        mock_previous_session = mock.Mock()
        mock_get_previous_session.return_value = mock_previous_session
        # find the date of the last dailysummary
        mock_last_summary = mock.Mock()
        mock_get_last_summary = mock.Mock()
        mock_DailySummary.get_last_summary = mock_get_last_summary
        mock_get_last_summary.return_value = mock_last_summary
        # for each date between the last dailysummary and the last scraping session (but not including these dates)
        mock_days_between = [mock.Mock(), mock.Mock()]
        mock_get_days_between.return_value = mock_days_between
        # produce a daily summary
        mock_daily_summary1 = mock.Mock()
        mock_daily_summary2 = mock.Mock()
        mock_DailySummary.side_effect = [mock_daily_summary1, mock_daily_summary2]
        # save the daily summary

        background.update_daily_summaries()
        
        mock_get_previous_session.assert_called_once_with()
        mock_get_last_summary.assert_called_once_with()
        mock_get_days_between.assert_called_once_with(mock_last_summary.date, mock_previous_session.date)
        mock_DailySummary.assert_has_calls([
            mock.call(date=mock_days_between[0]),
            mock.call(date=mock_days_between[1])])
        for daily_summary in [mock_daily_summary1, mock_daily_summary2]:
            daily_summary.save.assert_called_once_with()
                
