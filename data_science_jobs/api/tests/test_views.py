import mock
from django.test import TestCase
from data_science_jobs.api.views import n_posts

@mock.patch('data_science_jobs.api.views.JsonResponse')
@mock.patch('data_science_jobs.api.views.DailySummary')
@mock.patch('data_science_jobs.api.views.parse_date')
class TestNPosts(TestCase):

    def setUp(self):
        self.request = mock.Mock()
        self.date_strings = [mock.Mock(), mock.Mock()]
        self.request.GET.getlist.return_value = self.date_strings
        
    def test_gets_dates_from_request(self, parse_date, DailySummary, JsonResponse):

        n_posts(self.request)

        self.request.GET.getlist.assert_called_with('dates')

    def test_converts_date_strings_to_date_objects(self, parse_date, DailySummary, JsonResponse):

        n_posts(self.request)

        parse_date.assert_has_calls([mock.call(x) for x in self.date_strings])

    def test_gets_daily_summaries_with_date(self, parse_date, DailySummary, JsonResponse):

        dates = [mock.Mock(), mock.Mock()]
        parse_date.side_effect = dates
        
        n_posts(self.request)

        DailySummary.objects.get.assert_has_calls([mock.call(date=date) for date in dates])

    def test_returns_list_of_json_objects(self, parse_date, DailySummary, JsonResponse):

        dates = [mock.Mock(), mock.Mock()]
        parse_date.side_effect = dates
        daily_summaries = [mock.Mock(), mock.Mock()]
        DailySummary.objects.get.side_effect = daily_summaries

        expected_output = {}
        for date, daily_summary in zip(dates, daily_summaries):
            expected_output[date.isoformat()] = daily_summary.n_posts

        json_response = n_posts(self.request)

        JsonResponse.assert_called_once_with(expected_output)
        self.assertEqual(json_response, JsonResponse.return_value)

    def test_todo(self):
        self.fail('TODO')

        # TODO: invalid dates, incorrect format, future, excessively large ranges
        # TODO: daily summary for a date does not exist
        
