import time
import datetime
import logging
from django.utils import timezone
from dateutil.parser import parse as parse_date
from django.core.management.base import BaseCommand
from data_science_jobs import scraping
from data_science_jobs.scraping import Scraper
from data_science_jobs.scraping.models import Session

logger = logging.getLogger(__name__)

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
        parser.add_argument('--log', type=str, help='Log filepath', default='scraper.log')
        
    def handle(self, *args, **options):
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        logger.addHandler(handler)
        formatter = logging.Formatter('%(levelname)s: %(name)s: %(message)s')
        handler.setFormatter(formatter)
        scraping.logger.setLevel(logging.INFO)
        scraping.logger.addHandler(handler)
        logger.propagate = False
        file_handler = logging.FileHandler(options['log'])
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        scraping.logger.addHandler(file_handler)

        start_datetime = convert_start_to_datetime(start=options['start'])
        scraper = Scraper()
        wait_till_start_time(start_datetime)
        while True:
            logger.info('Current datetime: {}'.format(datetime.datetime.now()))
            previous_session = Session.get_previous_session()
            logger.info('Previous Session: {}'.format(previous_session.datetime if previous_session else previous_session))
            logger.info('Configure scraper')
            scraper.configure(start_datetime, previous_session)
            days_since = scraping.get_days_between(previous_session.datetime if previous_session else None, start_datetime)
            logger.info('Days since last scrape: {}'.format(days_since))
            logger.info('Date Filter: {}'.format(scraper.date_filter))
            logger.info('Beginning Scraper:')
            scraper.scrape()
            next_datetime = start_datetime + datetime.timedelta(seconds=options['frequency'])
            start_datetime = next_datetime
            logger.info('next scraping session: {}\n'.format(next_datetime))
            if timezone.now() > next_datetime:
                continue
            wait_till_next_session((next_datetime - timezone.now()).total_seconds())
