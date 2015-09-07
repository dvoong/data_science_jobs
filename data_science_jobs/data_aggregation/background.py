import datetime
import data_science_jobs
from  data_science_jobs.scraping.models import Session as ScrapingSession
from data_science_jobs.data_aggregation.models import DailySummary
from data_science_jobs.models import JobListing

def update_daily_summaries():
    previous_session = ScrapingSession.get_previous_session()
    if previous_session == None:
        return
    last_summary = DailySummary.get_last_summary()
    if last_summary == None:
        start_date = JobListing.get_earliest_job_listing().added - datetime.timedelta(days=1)
    else:
        start_date = last_summary.date
    dates_between = data_science_jobs.get_days_between(
        start_date,
        previous_session.datetime.date())
    for date in dates_between:
        daily_summary = DailySummary.create(date=date)
        daily_summary.save()

