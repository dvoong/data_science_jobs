from django.db.models import Model, DateField, IntegerField

class DailySummary(Model):

    date = DateField()
    n_posts = IntegerField()

    @staticmethod
    def get_last_summary():
        pass
