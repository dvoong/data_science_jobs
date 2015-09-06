import django

class Session(django.db.models.Model):

    datetime = django.db.models.DateTimeField()
    
    @staticmethod
    def get_previous_session():
        try:
            return Session.objects.latest('datetime')
        except Session.DoesNotExist:
            pass
    
