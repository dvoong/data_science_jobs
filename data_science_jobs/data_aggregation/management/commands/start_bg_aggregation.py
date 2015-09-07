import time
import datetime
from django.core.management.base import BaseCommand
from data_science_jobs.data_aggregation.background import update_daily_summaries
                
class Command(BaseCommand):
    help = 'Closes the specified poll for voting'
                    
    def add_arguments(self, parser):
        pass
        # parser.add_argument('--start', help='Start datetime, ISO 8601 format (default: now)', default=None)
        # parser.add_argument('--frequency', type=int, help='Scraping Frequency in seconds (default: 1 day)', default=86400)
                
    def handle(self, *args, **options):
        while True:
            update_daily_summaries()
            time.sleep(86400.0)
        # start_datetime = convert_start_to_datetime(start=options['start'])
        # scraper = Scraper()
        # wait_till_start_time(start_datetime)
        # while True:
        #     previous_session = Session.get_previous_session()
        #     scraper.configure(start_datetime, previous_session)
        #     scraper.scrape()
        #     wait_till_next_session(options['frequency'])
