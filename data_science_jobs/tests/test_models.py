import datetime
from django.test import TestCase
from data_science_jobs.models import JobListing

class GetEarliestJobListingTest(TestCase):

    def test_returns_none_if_no_job_listings(self):

        job_listing = JobListing.get_earliest_job_listing()

        self.assertEqual(job_listing, None)

    def test_returns_ealiest_job(self):

        job1 = JobListing.objects.create(jobid=1, title='Job 1', added=datetime.datetime(year=2015, month=9, day=1).date())
        job2 = JobListing.objects.create(jobid=2, title='Job 2', added=datetime.datetime(year=2015, month=8, day=1).date())
        job3 = JobListing.objects.create(jobid=3, title='Job 3', added=datetime.datetime(year=2015, month=10, day=1).date())

        job_listing = JobListing.get_earliest_job_listing()

        self.assertEqual(job_listing, job2)

class GetNPostsTest(TestCase):

    def test_get_n_posts_returns_n_job_listings_for_a_date(self):
        
        job1 = JobListing.objects.create(jobid=1,
                                         title='Title 1',
                                         description='Description 1',
                                         added=datetime.datetime(2015, 9, 1).date())
        job2 = JobListing.objects.create(jobid=2,
                                         title='Title 2',
                                         description='Description 2',
                                         added=datetime.datetime(2015, 9, 2).date())
        job3 = JobListing.objects.create(jobid=3,
                                         title='Title 3',
                                         description='Description 3',
                                         added=datetime.datetime(2015, 9, 2).date())

        n_posts = JobListing.get_n_posts(datetime.datetime(2015, 9, 1).date())
        self.assertEqual(n_posts, 1)
        n_posts = JobListing.get_n_posts(datetime.datetime(2015, 9, 2).date())
        self.assertEqual(n_posts, 2)
        n_posts = JobListing.get_n_posts(datetime.datetime(2015, 9, 3).date())
        self.assertEqual(n_posts, 0)
            
        
