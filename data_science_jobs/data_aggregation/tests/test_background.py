import mock
import datetime
from data_science_jobs import scraping
from data_science_jobs.models import JobListing
from data_science_jobs.data_aggregation import background
from data_science_jobs.data_aggregation.models import DailySummary, MonthlySummary
from django.test import TestCase
from django.utils import timezone

class UpdateMonthlySummariesIntegratedTest(TestCase):

    def test_uses_job_listings_to_create_monthly_summary(self):

        job1 = JobListing.objects.create(
            jobid=1,
            title='title1',
            description='description1',
            added=datetime.datetime(year=2015, month=9, day=1).date())
        
        job2 = JobListing.objects.create(
            jobid=2,
            title='title2',
            description='description2',
        added=datetime.datetime(year=2015, month=8, day=2).date())
        
        job3 = JobListing.objects.create(
            jobid=3,
            title='title3',
            description='description3',
        added=datetime.datetime(year=2015, month=8, day=17).date())

        session = scraping.models.Session.objects.create(datetime=datetime.datetime(year=2015, month=10, day=3))

        background.update_monthly_summaries()

        monthly_summary1 = MonthlySummary.objects.first()
        monthly_summary2 = MonthlySummary.objects.last()

        self.assertEqual(monthly_summary1.date, datetime.datetime(2015, 8, 1).date())
        self.assertEqual(monthly_summary2.date, datetime.datetime(2015, 9, 1).date())
        self.assertEqual(monthly_summary1.n_posts, 2)
        self.assertEqual(monthly_summary2.n_posts, 1)

class UpdatedMonthlySummariesUnitTest(TestCase):

    pass
        
class UpdateDailySummariesIntegratedTest(TestCase):

    def test_uses_job_listings_to_create_daily_summary(self):

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
        
        job3 = JobListing.objects.create(
            jobid=3,
            title='title3',
            description='description3',
        added=datetime.datetime(year=2015, month=9, day=2).date())

        session = scraping.models.Session.objects.create(datetime=datetime.datetime(year=2015, month=9, day=3))

        background.update_daily_summaries()

        daily_summary1 = DailySummary.objects.first()
        daily_summary2 = DailySummary.objects.last()
    
        self.assertEqual(daily_summary1.date, job1.added)
        self.assertEqual(daily_summary2.date, job2.added)
        self.assertEqual(daily_summary1.n_posts, 1)
        self.assertEqual(daily_summary2.n_posts, 2)

@mock.patch('data_science_jobs.data_aggregation.background.DailySummary')
@mock.patch('data_science_jobs.get_days_between')
@mock.patch('data_science_jobs.data_aggregation.background.ScrapingSession')
class UpdateDailySummariesUnitTest(TestCase):

    def test_gets_the_date_of_the_last_scraping_session(self, ScrapingSession, get_days_between, DailySummary):
        background.update_daily_summaries()

        ScrapingSession.get_previous_session.assert_called_once_with()

    def test_gets_the_last_daily_summary(self, ScrapingSession, get_days_between, DailySummary):
        background.update_daily_summaries()

        DailySummary.get_last_summary.assert_called_once_with()

    def test_gets_the_days_between_the_last_scraping_session_and_the_last_daily_summary(self, ScrapingSession, get_days_between, DailySummary):
        previous_scraping_session = mock.Mock()
        ScrapingSession.get_previous_session.return_value = previous_scraping_session
        last_summary = mock.Mock()
        DailySummary.get_last_summary.return_value = last_summary

        background.update_daily_summaries()

        get_days_between.assert_called_with(last_summary.date, previous_scraping_session.datetime.date())
        
    def test_creates_a_new_daily_summary_for_each_date(self, ScrapingSession, get_days_between, DailySummary):
        dates = [mock.Mock(), mock.Mock()]
        get_days_between.return_value = dates

        background.update_daily_summaries()

        DailySummary.create.has_calls([mock.call(date) for date in dates])

    def test_daily_summaries_are_saved(self, ScrapingSession, get_days_between, DailySummary):
        dates = [mock.Mock(), mock.Mock()]
        get_days_between.return_value = dates
        daily_summaries = [mock.Mock(), mock.Mock()]
        DailySummary.create.side_effect = daily_summaries

        background.update_daily_summaries()

        for daily_summary in daily_summaries:
            daily_summary.save.assert_called_once_with()

    @mock.patch('data_science_jobs.data_aggregation.background.JobListing')
    def test_last_summary_is_none_gets_the_first_job_listing(self, JobListing, ScrapingSession, get_days_between, DailySummary):
        last_summary = None
        DailySummary.get_last_summary.return_value = last_summary

        background.update_daily_summaries()

        JobListing.get_earliest_job_listing.assert_called_once_with()
        
    @mock.patch('data_science_jobs.data_aggregation.background.JobListing')
    def test_last_summary_is_none_uses_first_job_listing_as_start_date(self, JobListing, ScrapingSession, get_days_between, DailySummary):
        '''
        Actually uses the day before the job added date
        '''
        last_summary = None
        DailySummary.get_last_summary.return_value = last_summary
        session = mock.Mock()
        ScrapingSession.get_previous_session.return_value = session
        earliest_job = JobListing.get_earliest_job_listing()
        day_before = earliest_job.added - datetime.timedelta(days=1)

        background.update_daily_summaries()

        get_days_between.assert_called_once_with(day_before, session.datetime.date())
    
    def test_no_previous_scraping_sessions_doesnt_do_anything(self, ScrapingSession, get_days_between, DailySummary):
        previous_session = None
        ScrapingSession.get_previous_session.return_value = previous_session

        background.update_daily_summaries()

        DailySummary.create.has_calls([])
