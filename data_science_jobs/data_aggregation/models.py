from data_science_jobs.models import JobListing
from django.db.models import Model, DateField, IntegerField

class DailySummary(Model):

    date = DateField()
    n_posts = IntegerField()

    @classmethod
    def create(cls, date):
        n_posts = JobListing.get_n_posts(date)
        daily_summary = cls(date=date, n_posts=n_posts)
        return daily_summary

    @classmethod
    def get_last_summary(cls):
        return cls.objects.order_by('date').last()

