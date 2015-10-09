import dateutil
import requests
import datetime
import logging
from data_science_jobs.models import JobListing
from data_science_jobs.scraping.models import Session
from lxml import html
from django.utils import timezone

logger = logging.getLogger(__name__)

class JobCreationFailed(Exception):
    pass

def get_table(response):
    tree = html.fromstring(response.content)
    table = tree.xpath('//*[@id="aspnetForm"]/div/div[2]/div[7]/table')[0]
    return table
    
def get_rows(table):
    rows = table.findall('tr')[1:]
    return rows

def get_link(row):
    column_element = row.findall('td')[2]
    link_element = column_element.find('a')
    link_text = link_element.attrib['href']
    return link_text

def create_job_listing(link):
    response = requests.get(link)
    tree = html.fromstring(response.content)
    job = {}

    try:
        job['jobid'] = int(tree.xpath('//*[@id="aspnetForm"]/div/div[2]/div[4]/div/div[4]/dl/dd[1]')[0].text)
    except IndexError:
        try:
            job['jobid'] = int(tree.xpath('//*[@id="aspnetForm"]/div/div[2]/div[4]/div/div[3]/dl/dd[1]')[0].text)
        except IndexError:
            raise JobCreationFailed('Could not find the job id:', link)
    try:
        job['title'] = tree.xpath('//*[@id="aspnetForm"]/div/div[2]/div[5]/div[2]/h2[2]')[0].text_content()
        try:
            job['title'] = job['title'].encode('latin-1').decode('utf8')
        except UnicodeDecodeError:
            pass
    except IndexError:
        raise JobCreationFailed('Could not find the job title:', link)
    try:
        job['description'] = tree.xpath('//*[@id="aspnetForm"]/div/div[2]/div[5]/div[2]/div[1]')[0].text_content()
    except IndexError:
        raise JobCreationFailed('Could not find the job description:', link)
    try:
        job['company'] = tree.xpath('//*[@id="aspnetForm"]/div/div[2]/div[5]/div[2]/h2[1]')[0].text_content()
    except IndexError:
        pass

    job_summary = tree.cssselect('div.jobViewSummary')[0]
    dl = job_summary.cssselect('dl')[0]
    dts = dl.cssselect('dt')
    dds = dl.cssselect('dd')
    descrips = zip(dts, dds)
    for key, val in descrips:
        if key.text.lower() == 'posting date':
            job['added'] = dateutil.parser.parse(val.text, dayfirst=True)
        elif key.text.lower() == 'location':
            job['location'] = val.text
        elif key.text.lower() == 'industries':
            job['industry'] = val.text
        elif key.text.lower() == 'job type':
            job['job_type'] = val.text
        elif key.text.lower() == 'salary':
            job['salary'] = val.text

    if 'added' not in job:
        raise JobCreationFailed('Could not find the date added')

    job['link'] = link
    job = JobListing(**job)
    return job
        
def get_job_links(response):
    table = get_table(response)
    rows = get_rows(table)
    links = []
    for row in rows:
        link = get_link(row)
        links.append(link)
    return links

def populate_db(response):
    summary = {'success': [], 'failed': [], 'retry': []}
    job_links = get_job_links(response)
    failed_jobs = []
    for job_link in job_links:
        try:
            job_listing = create_job_listing(job_link)
            job_listing.save()
            summary['success'].append(job_link)
        except JobCreationFailed as e:
            summary['failed'].append((job_link, e),)
    return summary

def get_n_pages(response):
    tree = html.fromstring(response.content)
    page_summary = tree.cssselect('div.pagesSummary span')[0].text
    n_pages = int(page_summary.split(' ')[-1])
    return n_pages

def get_url(date_filter, page):
    url_template = 'https://jobsearch.direct.gov.uk/JobSearch/PowerSearch.aspx?redirect=http%3A%2F%2Fjobsearch.direct.gov.uk%2Fhome.aspx&pp=25&sort=rv.dt.di&re=3&tm={date_filter}&pg={page_number}&q=%22Data%20Science%22'
    return url_template.format(page_number=page, date_filter=date_filter)

def get_days_between(first, second):
    if first != None and second != None:
        return (second.date() - first.date()).days

def get_now():
    return timezone.now()

def get_days_since_last_scrape(last_session):
    if last_session:
        today = datetime.datetime.today().date()
        timedelta = today - last_session.datetime.date
        return timedelta.days

def get_date_filter(days_since):
    # if days_since == 0:
    #     return 0
    # if days_since == 1:
    #     return 1
    # elif days_since > 1 and days_since <= 3:
    #     return 3
    # ensure previous days are rescraped because the jobsearch site is weird
    if days_since <= 3:
        return 3
    elif days_since > 3 and days_since <= 7:
        return 7
    elif days_since > 7 and days_since <= 14:
        return 14
    elif days_since > 14 and days_since <= 30:
        return 30
    return -1

class Scraper(object):

    def scrape(self):
        logger.info('Beginning Scraper:')
        session = Session(datetime=timezone.now())
        url = get_url(date_filter=self.date_filter, page=1)
        logger.info('URL: {}'.format(url))
        response = requests.get(url)
        n_pages = get_n_pages(response)
        logger.info('n_pages: {}'.format(n_pages))
        logger.info('page 1/{}'.format(n_pages))
        summary = populate_db(response)
        logger.info('{} successfully read, {} failed, {} to retry'.format(len(summary['success']), len(summary['failed']), len(summary['retry'])))
        for page in range(2, n_pages + 1):
            logger.info('page {}/{}'.format(page, n_pages))
            url = get_url(date_filter=self.date_filter, page=page)
            response = requests.get(url)
            summary_ = populate_db(response)
            logger.info('{} successfully read, {} failed, {} to retry'.format(len(summary_['success']), len(summary_['failed']), len(summary_['retry'])))
            for key, val in summary_.iteritems():
                summary[key].extend(val)
        session.save()
        logger.info('----------' * 5)
        logger.info('Total Summary')
        logger.info('{} successfully read, {} failed, {} to retry'.format(len(summary['success']),len(summary['failed']), len(summary['retry'])))
        logger.info('----------' * 5)

    def configure(self, next_session_datetime, last_session):
        logger.info('Configuring scraper')
        days_since = get_days_between(last_session.datetime if last_session else None, next_session_datetime)
        logger.info('Days since last scrape: {}'.format(days_since))
        self.date_filter = get_date_filter(days_since)
        logger.info('Date Filter: {}'.format(self.date_filter))
