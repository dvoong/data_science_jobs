import django
import mock
import unittest
import datetime
import cPickle
from data_science_jobs.models import JobListing
from data_science_jobs import scraping
from data_science_jobs.scraping.models import Session
from data_science_jobs.scraping.management.commands.start_scraper import convert_start_to_datetime
from data_science_jobs.scraping.management.commands.start_scraper import wait_till_start_time
from data_science_jobs.scraping.management.commands.start_scraper import Command

f = open('data_science_jobs/scraping/tests/example_response.pkl', 'rb')
example_response = cPickle.load(f)


class TestGetDaysSinceLastScrape(unittest.TestCase):

    def test_no_last_session_returns_None(self):
        output = scraping.get_days_since_last_scrape(last_session=None)
        self.assertEqual(output, None)

    @mock.patch('datetime.datetime')
    def test_last_session_not_None(self, mock_datetime):
        yesterday = mock.Mock()
        today = mock.Mock()
        days_since = mock.Mock()

        today.__sub__ = mock.Mock(return_value=days_since)
        days_since.days = 1

        last_session = mock.Mock()
        last_session.datetime = mock.Mock(date=yesterday)
        mock_datetime.today = mock.Mock(return_value=mock.Mock(date=mock.Mock(return_value=today)))

        output = scraping.get_days_since_last_scrape(last_session=last_session)

        self.assertEqual(output, 1)

class TestGetDateFilter(unittest.TestCase):

    def setUp(self):
        self.mock_session = mock.Mock()

    def test_no_last_session_returns_minus_1(self):
        output = scraping.get_date_filter(None)
        self.assertEqual(output, -1)

    def test_days(self):
        test_vals = [
            (1, 1),
            (2, 3),
            (3, 3),
            (4, 7),
            (5, 7),
            (6, 7),
            (7, 7),
        ]
        for i in range(8, 15):
            test_vals.append((i, 14),)
        for i in range(15, 31):
            test_vals.append((i, 30),)
        for i in range(31, 50):
            test_vals.append((i, -1),)
        test_vals.extend([(None, -1), (-1, -1)])

        for days, expected_filter in test_vals:
            output = scraping.get_date_filter(days)
            self.assertEqual(output, expected_filter)

class ErrorAfter(object):
    '''
    Callable that will raise `CallableExhausted`
    exception after `limit` calls
    
    '''
    def __init__(self, limit):
        self.limit = limit
        self.calls = 0
        
    def __call__(self, *args, **kwargs):
        self.calls += 1
        if self.calls > self.limit:
            raise CallableExhausted
            
class CallableExhausted(Exception):
    pass
            
@mock.patch('data_science_jobs.scraping.management.commands.start_scraper.timezone')
@mock.patch('data_science_jobs.scraping.management.commands.start_scraper.convert_start_to_datetime')
@mock.patch('data_science_jobs.scraping.management.commands.start_scraper.Scraper')
@mock.patch('data_science_jobs.scraping.management.commands.start_scraper.wait_till_start_time')
@mock.patch('data_science_jobs.scraping.management.commands.start_scraper.datetime')
@mock.patch('data_science_jobs.scraping.management.commands.start_scraper.wait_till_next_session')
class HandleTest(unittest.TestCase):

    def test_handle_calls_convert_start_time(self, wait_till_next_session,
                                             datetime,
                                             wait_till_start_time,
                                             Scraper,
                                             convert_start_to_datetime,
                                             timezone):

        wait_till_next_session.side_effect = ErrorAfter(0)

        command = Command()
        try:
            command.handle(**{'start': None, 'frequency': 86400})
        except CallableExhausted:
            pass

        convert_start_to_datetime.assert_called_once_with(start=None)

    def test_scraper_object_created(self, wait_till_next_session, datetime, wait_till_start_time, Scraper, *args, **kwargs):

        wait_till_next_session.side_effect = ErrorAfter(0)

        command = Command()
        try:
            command.handle(**{'start': None, 'frequency': 86400})
        except CallableExhausted:
            pass

        Scraper.assert_called_once_with()

    def test_waits_till_start_time_called(self,
                                          wait_till_next_session,
                                          datetime,
                                          wait_till_start_time,
                                          Scraper,
                                          convert_start_to_datetime,
                                          timezone):

        wait_till_next_session.side_effect = ErrorAfter(0)

        command = Command()
        try:
            command.handle(**{'start': None, 'frequency': 86400})
        except CallableExhausted:
            pass
        
        wait_till_start_time.assert_called_once_with(convert_start_to_datetime.return_value)

    @mock.patch('data_science_jobs.scraping.management.commands.start_scraper.Session')
    def test_get_previous_session_called(self,
                                         Session,
                                         wait_till_next_session,
                                         datetime,
                                         wait_till_start_time,
                                         Scraper,
                                         convert_start_to_datetime,
                                         timezone):
        
        wait_till_next_session.side_effect = ErrorAfter(2)

        command = Command()
        try:
            command.handle(**{'start': None, 'frequency': 86400})
        except CallableExhausted:
            pass
        
        Session.get_previous_session.assert_has_calls([mock.call(), mock.call(), mock.call()])
        
    @mock.patch('data_science_jobs.scraping.management.commands.start_scraper.Session')
    def test_scraper_calls_configure(self,
                                     Session,
                                     wait_till_next_session,
                                     datetime,
                                     wait_till_start_time,
                                     Scraper,
                                     convert_start_to_datetime,
                                     timezone):

        wait_till_next_session.side_effect = ErrorAfter(2)

        command = Command()
        try:
            command.handle(**{'start': None, 'frequency': 86400})
        except CallableExhausted:
            pass

        Scraper().configure.assert_has_calls([
            mock.call(convert_start_to_datetime.return_value, Session.get_previous_session.return_value),
            mock.call(convert_start_to_datetime.return_value, Session.get_previous_session.return_value),
            mock.call(convert_start_to_datetime.return_value, Session.get_previous_session.return_value),
        ])

    def test_scraper_calls_scrape(self,
                                  wait_till_next_session,
                                  datetime,
                                  wait_till_start_time,
                                  Scraper,
                                  convert_start_to_datetime,
                                  timezone):
        
        wait_till_next_session.side_effect = ErrorAfter(2)
        
        command = Command()
        try:
            command.handle(**{'start': None, 'frequency': 86400})
        except CallableExhausted:
            pass

        Scraper().scrape.assert_has_calls([
            mock.call(),
            mock.call(),
            mock.call()])

    def test_waits_till_next_session(self,
                                     wait_till_next_session,
                                     datetime,
                                     wait_till_start_time,
                                     Scraper,
                                     convert_start_to_datetime,
                                     timezone):
    
        wait_till_next_session.side_effect = ErrorAfter(2)
        
        command = Command()
        try:
            command.handle(**{'start': None, 'frequency': 86400})
        except CallableExhausted:
            pass
        
        self.assertEqual(wait_till_next_session.call_count, 3)
        
@mock.patch('data_science_jobs.scraping.management.commands.start_scraper.parse_date')
@mock.patch('data_science_jobs.scraping.management.commands.start_scraper.timezone')
class TestConvertStartToDatetime(unittest.TestCase):

    def test_start_is_none_returns_now(self, mock_datetime, mock_parse):
        mock_now = mock.Mock()
        mock_datetime.now = mock_now
        now = mock.Mock()
        mock_now.return_value = now
        
        output = convert_start_to_datetime(None)

        mock_now.assert_called_once_with()
        self.assertEqual(output, now)
    
    def test_start_is_valid_format(self, mock_datetime, mock_parse):
        parse_datetime = mock.Mock()
        mock_parse.return_value = parse_datetime
        
        output = convert_start_to_datetime('2015-01-01')

        mock_parse.assert_called_once_with('2015-01-01')
        self.assertEqual(output, parse_datetime)

class TestScraper(django.test.TestCase):

    pass

@mock.patch('data_science_jobs.scraping.get_now')
@mock.patch('time.sleep')
class TestWaitTillStartTime(django.test.TestCase):

    def test_start_time_is_earlier_than_now(self, mock_sleep, mock_get_now):
        mock_get_now.return_value = datetime.datetime(year=2015, month=1, day=2)
        start = datetime.datetime(year=2015, month=1, day=1)

        wait_till_start_time(start)

        mock_sleep.assert_called_once_with(0)

    def test_start_time_later_than_now(self, mock_sleep, mock_get_now):
        mock_get_now.return_value = datetime.datetime(year=2015, month=1, day=1)
        start = datetime.datetime(year=2015, month=1, day=2)

        wait_till_start_time(start)

        mock_sleep.assert_called_once_with(86400.0)

class TestGetPreviousSession(django.test.TestCase):

    def test_no_previous_session_returns_none(self):
        session = Session.get_previous_session()
        self.assertEqual(session, None)

    def test_returns_previous_session(self):
        session = Session.objects.create(datetime=datetime.datetime(year=2015, month=1, day=1))
        output = Session.get_previous_session()
        self.assertEqual(output, session)

@mock.patch('data_science_jobs.scraping.get_date_filter')
@mock.patch('data_science_jobs.scraping.get_days_between')        
class TestConfigureScraper(django.test.TestCase):

    def setUp(self):
        self.scraper = scraping.Scraper()

    def test_configure(self, mock_get_days_between, mock_get_date_filter):
        start = mock.Mock()
        last_session = mock.Mock()

        mock_days_since = mock.Mock()
        mock_get_days_between.return_value = mock_days_since

        mock_date_filter = mock.Mock()
        mock_get_date_filter.return_value = mock_date_filter
        
        self.scraper.configure(start, last_session)

        mock_get_days_between.assert_called_once_with(last_session.datetime, start)
        mock_get_date_filter.assert_called_once_with(mock_days_since)

        self.assertEqual(self.scraper.date_filter, mock_date_filter)

    def test_configure_if_last_session_is_none(self, mock_get_days_between, mock_get_date_filter):
        start = mock.Mock()
        last_session = None

        mock_days_since = mock.Mock()
        mock_get_days_between.return_value = mock_days_since
        
        mock_date_filter = mock.Mock()
        mock_get_date_filter.return_value = mock_date_filter
        
        self.scraper.configure(start, last_session)

        mock_get_days_between.assert_called_once_with(last_session, start) # instead of last_session.datetime
        mock_get_date_filter.assert_called_once_with(mock_days_since)

        self.assertEqual(self.scraper.date_filter, mock_date_filter)

@mock.patch('data_science_jobs.scraping.get_url')
@mock.patch('requests.get')
@mock.patch('data_science_jobs.scraping.get_n_pages')
@mock.patch('data_science_jobs.scraping.populate_db')
class TestScrape(django.test.TestCase):

    def test_main(self, mock_populate_db, mock_get_n_pages, mock_requests_get, mock_get_url):

        # get url for page 1
        mock_url = mock.Mock()
        mock_get_url.side_effect = [mock_url]
        # get response for page 1
        mock_response = mock.Mock()
        mock_requests_get.side_effect = [mock_response] # will need more responses later
        # get n pages
        mock_n_pages = 2
        mock_get_n_pages.return_value = mock_n_pages
        # populate database with response from page 1
        # get url for page i
        mock_url_2 = mock.Mock()
        mock_get_url.side_effect = [mock_url, mock_url_2]
        # get response for page i
        mock_response_2 = mock.Mock()
        mock_requests_get.side_effect = [mock_response, mock_response_2]
        # populate database with response from page i

        scraper = scraping.Scraper()
        scraper.date_filter = 1
        scraper.scrape()

        # get urls
        mock_get_url.assert_has_calls([
            mock.call(date_filter=scraper.date_filter, page=1),
            mock.call(date_filter=scraper.date_filter, page=2),
        ])
        # get responses
        mock_requests_get.assert_has_calls([
            mock.call(mock_url),
            mock.call(mock_url_2)
        ])
        # get n pages
        mock_get_n_pages.assert_called_once_with(mock_response)
        # populate database with response
        mock_populate_db.assert_has_calls([
            mock.call(mock_response),
            mock.call(mock_response_2),
        ])

class TestGetUrl(django.test.TestCase):

    def test_main(self):

        url = scraping.get_url(date_filter=1, page=1)

        self.assertEqual(url, 'https://jobsearch.direct.gov.uk/JobSearch/PowerSearch.aspx?redirect=http%3A%2F%2Fjobsearch.direct.gov.uk%2Fhome.aspx&pp=25&sort=rv.dt.di&re=3&tm=1&pg=1&q=%22Data%20Science%22')

class TestGetNPages(django.test.TestCase):

    def test_main(self):

        response = example_response # defined earlier
        
        n_pages = scraping.get_n_pages(response)

        self.assertEqual(n_pages, 3)

class TestPopulateDb(django.test.TestCase):

    @mock.patch('data_science_jobs.scraping.create_job_listing')
    @mock.patch('data_science_jobs.scraping.get_job_links')
    def test_main(self, mock_get_job_links, mock_create_job_listing):

        response = example_response # defined earlier
        mock_job_links = [mock.Mock(), mock.Mock()]
        mock_get_job_links.return_value = mock_job_links
        mock_jobs = [mock.Mock(), mock.Mock()]
        mock_create_job_listing.side_effect = mock_jobs
        
        scraping.populate_db(response)

        mock_get_job_links.assert_called_once_with(response)
        mock_create_job_listing.assert_has_calls([mock.call(i) for i in mock_job_links])
        for job in mock_jobs:
            job.save.assert_called_once_with()

    @mock.patch('data_science_jobs.scraping.create_job_listing')
    @mock.patch('data_science_jobs.scraping.get_job_links')

    def test_create_job_fails(self, mock_get_job_links, mock_create_job_listing):

        response = example_response
        mock_job_links = [mock.Mock(), mock.Mock(), mock.Mock()]
        mock_get_job_links.return_value = mock_job_links
        mock_jobs = [mock.Mock(), None, mock.Mock()]
        class Test:
            def __init__(self):
                self.calls = 0
            def __call__(self, response):
                if self.calls != 1:
                    self.calls += 1
                    return mock_jobs[self.calls - 1]
                else:
                    self.calls += 1
                    raise scraping.JobCreationFailed()
        mock_create_job_listing.side_effect = Test()
        
        scraping.populate_db(response)

        mock_get_job_links.assert_called_once_with(response)
        mock_create_job_listing.assert_has_calls([mock.call(i) for i in mock_job_links])
        for job in mock_jobs:
            if job != None:
                job.save.assert_called_once_with()

class TestGetJobLinks(django.test.TestCase):

    @mock.patch('data_science_jobs.scraping.get_link')
    @mock.patch('data_science_jobs.scraping.get_rows')
    @mock.patch('data_science_jobs.scraping.get_table')
    def test_main(self, mock_get_table, mock_get_rows, mock_get_link):

        response = example_response
        mock_table = mock.Mock()
        mock_get_table.return_value = mock_table
        mock_rows = [mock.Mock(), mock.Mock()]
        mock_get_rows.return_value = mock_rows
        mock_links = [mock.Mock(), mock.Mock()]
        mock_get_link.side_effect = mock_links
        
        links = scraping.get_job_links(response)

        mock_get_table.assert_called_once_with(response)
        mock_get_rows.assert_called_once_with(mock_table)
        mock_get_link.assert_has_calls([mock.call(i) for i in mock_rows])

        self.assertEqual(links, mock_links)

class TestGetTable(django.test.TestCase):

    @mock.patch('data_science_jobs.scraping.html.fromstring')
    def test_main(self, mock_fromstring):

        response = example_response
        mock_tree = mock.Mock()
        mock_fromstring.return_value = mock_tree
        mock_table = mock.Mock()
        mock_tree.xpath.return_value = [mock_table]
        
        table = scraping.get_table(response)

        mock_fromstring.assert_called_once_with(response.content)
        mock_tree.xpath.assert_called_once_with('//*[@id="aspnetForm"]/div/div[2]/div[7]/table')
        self.assertEqual(table, mock_table)

class TestGetRows(django.test.TestCase):

    def test_main(self):
        mock_table = mock.Mock()
        mock_rows = [mock.Mock(), mock.Mock()]
        mock_table.findall.return_value = [mock.Mock()] + mock_rows
    
        rows = scraping.get_rows(mock_table)
        
        mock_table.findall.assert_called_once_with('tr')
        self.assertEqual(rows, mock_rows)


# class TestCreateJobListing(django.test.TestCase):

#     def test_main(self):
#         self.fail('TODO')

if __name__ == '__main__':
    unittest.main()

    
