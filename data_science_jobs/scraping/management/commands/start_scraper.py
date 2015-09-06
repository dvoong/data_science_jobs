import time
import datetime
from django.utils import timezone
from dateutil.parser import parse as parse_date
from django.core.management.base import BaseCommand
from data_science_jobs import scraping
from data_science_jobs.scraping import Scraper
from data_science_jobs.scraping.models import Session

def convert_start_to_datetime(start):
    if start == None:
        return timezone.now() #datetime.datetime.now()
    else:
        return parse_date(start)

def wait_till_start_time(start):
    now = scraping.get_now()
    if start - now < datetime.timedelta(seconds=0):
        time.sleep(0)
    else:
        time.sleep((start - now).total_seconds())

def wait_till_next_session(seconds):
    time.sleep(seconds)
        
class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('--start', help='Start datetime, ISO 8601 format (default: now)', default=None)
        parser.add_argument('--frequency', type=int, help='Scraping Frequency in seconds (default: 1 day)', default=86400)
        
    def handle(self, *args, **options):
        start_datetime = convert_start_to_datetime(start=options['start'])
        scraper = Scraper()
        wait_till_start_time(start_datetime)
        while True:
            previous_session = Session.get_previous_session()
            scraper.configure(start_datetime, previous_session)
            scraper.scrape()
            wait_till_next_session(options['frequency'])
