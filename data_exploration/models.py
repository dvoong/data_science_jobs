from django.db import models

class JobListing(models.Model):
    jobid = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    salary = models.CharField(max_length=300)
    career = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)
    job_type = models.CharField(max_length=100)
    education = models.CharField(max_length=100)
    description = models.CharField(max_length=10000)
    apply = models.CharField(max_length=500)
    reference = models.CharField(max_length=100)
#    contact = models.CharField(max_length=)
    added = models.DateField()
    noted = models.CharField(max_length=100)


