import django
from django.db import models

class JobListing(django.db.models.Model):
    jobid = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=10000)
    company = models.CharField(max_length=100)
    added = models.DateField()
    location = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)
    job_type = models.CharField(max_length=100)
    salary = models.CharField(max_length=300)
    link = models.URLField()
    def __str__(self):
        return '{}: {}: {}'.format(self.__class__.__name__, self.jobid, self.title)
    pass

