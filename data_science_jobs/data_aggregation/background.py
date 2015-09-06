import data_science_jobs
import data_science_jobs.scraping.models
import data_science_jobs.data_aggregation.models

def update_daily_summaries():
    previous_session = data_science_jobs.scraping.models.Session.get_previous_session()
    last_summary = data_science_jobs.data_aggregation.models.DailySummary.get_last_summary()
    dates_between = data_science_jobs.get_days_between(last_summary.date, previous_session.date)
    for date in dates_between:
        daily_summary = data_science_jobs.data_aggregation.models.DailySummary(date=date)
        daily_summary.save()
