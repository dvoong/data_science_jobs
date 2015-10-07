import logging
import datetime
import data_science_jobs
from  data_science_jobs.scraping.models import Session as ScrapingSession
from data_science_jobs.data_aggregation.models import DailySummary, MonthlySummary
from data_science_jobs.models import JobListing

logger = logging.getLogger(__name__)

def update_daily_summaries():
    logger.info('Update Daily Summaries: {}'.format(previous_session.datetime))
    previous_session = ScrapingSession.get_previous_session()
    logger.info('Previous Scraping Session: {}'.format(previous_session.datetime))
    if previous_session == None:
        return
    last_summary = DailySummary.get_last_summary()
    logger.info('Last Daily Summary: {}'.format(last_summary.date if last_summary else None))    
    if last_summary == None:
        start_date = JobListing.get_earliest_job_listing().added - datetime.timedelta(days=1)
    else:
        start_date = last_summary.date
    dates_between = data_science_jobs.get_days_between(
        start_date,
        previous_session.datetime.date())
    if len(dates_between):
        logger.info('Getting Daily Summaries Between: {} - {}'.format(dates_between[0], dates_between[-1]))
    else:
        logger.info('Daily Summaries Up-To-Date')
    for date in dates_between:
        logger.info('Creating daily summary for date: {}'.format(date))
        daily_summary = DailySummary.create(date=date)
        logger.info('n_posts: {}'.format(daily_summary.n_posts))
        daily_summary.save()

def update_monthly_summaries():
    logger.info('Update Monthly Summaries: {}'.format(previous_session.datetime))
    previous_session = ScrapingSession.get_previous_session()
    logger.info('Previous Scraping Session: {}'.format(previous_session.datetime))
    if previous_session == None:
        return
    last_summary = MonthlySummary.get_last_summary()
    logger.info('Last Monthly Summary: {}'.format(last_summary.date if last_summary else last_summary))
    if last_summary == None:
        start_date = JobListing.get_earliest_job_listing().added
        start_date = start_date - datetime.timedelta(days=start_date.day)
        start_date = datetime.datetime(year=start_date.year, month=start_date.month, day=1).date()
    else:
        start_date = last_summary.date
    previous_session_month = previous_session.datetime.date()
    previous_session_month = previous_session_month - datetime.timedelta(days=previous_session_month.day - 1)
    months_between = data_science_jobs.get_months_between(
        start_date,
        previous_session.datetime.date())
    logger.info('Months between: {}'.format(months_between))
    for date in months_between:
        logger.info('Creating monthly summary for date: {}'.format(date))
        monthly_summary = MonthlySummary.create(date=date)
        logger.info('n_posts: {}'.format(monthly_summary.n_posts))
        monthly_summary.save()

