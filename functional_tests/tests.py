from django.test import LiveServerTestCase, TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest, pdb

class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    
class NewVisitorTest(FunctionalTest):

    def test_main(self):
        # User goes to homepage and sees the title, author and date
        self.browser.get(self.live_server_url)
        # self.assertIn('Analysis of Data Science Jobs', self.browser.title)
        # header_text = self.browser.find_element_by_tag_name('h1').text
        # self.assertEqual(header_text, 'Analysis of Data Science Jobs')

        # # The user sees the introduction section
        # sections = self.browser.find_elements_by_tag_name('section')
        # introduction_section = [x for x in sections if x.get_attribute('id') == 'introduction'][0]
        # introduction_header = introduction_section.find_element_by_tag_name('h2')
        # self.assertEqual('Introduction', introduction_header.text)

        # # The user reads the introduction section
        # paragraphs = introduction_section.find_elements_by_tag_name('p')
        # self.assertGreaterEqual(len(paragraphs), 1)

        # # The user scrolls down to the salaries section
        # salaries_section = [x for x in sections if x.get_attribute('id') == 'salaries'][0]
        # salaries_header = salaries_section.find_element_by_tag_name('h2')
        # self.assertEqual('Salaries', salaries_header.text)

        # # The user reads the salaries section
        # paragraphs = salaries_section.find_elements_by_tag_name('p')
        # self.assertGreaterEqual(len(paragraphs), 1)
        
        # # The user sees a histogram of salaries
        # salaries_histogram = salaries_section.find_element_by_id("salaries-histogram")
        # self.assertIsNotNone(salaries_histogram)
        # self.fail('generate the histogram')

        # # The user sees a heat map of the salaries as a function of geolocation
        # salaries_geoloc = salaries_section.find_element_by_id("salaries-by-geolocation")
        # self.assertIsNotNone(salaries_geoloc)
        # self.fail('generate the histogram')

        # # User sees a bar chart of skills vs mean salary
        # salaries_skills = salaries_section.find_element_by_id("salaries-by-skills")
        # self.assertIsNotNone(salaries_skills)
        # self.fail('generate the histogram')

        # # User continues...
        # self.fail('finish test!!!')

