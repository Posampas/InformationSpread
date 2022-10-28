import unittest
from src.twitterConnection import Connection as con
from unittest import mock
from tests.twitterConnection.test_helpers import MockResponse


_user_id = 1460303834790731778

_error_json = {
        'errors': [{'parameters': {'id': ['ddd']}, 'message': 'The `id` query param... not valid'}],
        'title': 'Invalid Request',
        'detail': 'One or more paramete...s invalid.',
        'type': 'https://api.twitter....id-request'
        }

_unauthroised_json = {
                                "title": "Unauthorized",
                                "type": "about:blank",
                                "status": 401,
                                "detail": "Unauthorized"
                    }

_user_data_json = {
                                "data": {
                                    "name": "Piotr",
                                    "created_at": "2021-11-15T17:49:39.000Z",
                                    "protected": False,
                                    "username": "Piotr63632005",
                                    "id": "1460303834790731778",
                                    "description": "",
                                    "verified": False,
                                    "public_metrics": {
                                        "followers_count": 1,
                                        "following_count": 27,
                                        "tweet_count": 96,
                                        "listed_count": 0
                                    }
                                    }
                                }
# In *arg there is a url specified and **kwargs contains  dict with keys {header, params}
def mocked__request_get_user_by_id(*args, **kwargs):

    url = "https://api.twitter.com/2/users/{}".format(_user_id)
    print(kwargs['headers'])
    if args[0] != url:
        return 
    if kwargs['headers'] == {'Authorization': 'Bearer Invalid'}:
        return MockResponse(_unauthroised_json, 401)
    elif kwargs['headers'] == {'Authorization': 'Bearer Token'}:
        return MockResponse(_user_data_json, 200)

    return MockResponse({"key":"val"}, 400)
    
def mocked__request_get_user_timeline_id(*args, **kwargs):
    return MockResponse({"key":"val"}, 200)

def mocked__request_return_error(*args, **kwargs):
    return MockResponse( _error_json ,400)

class TwitterConncectionTest(unittest.TestCase):
    

    def setUp(self) -> None:
        self.correctToken = "Token"
        self.invalid_token = "Invalid"
        self._twitter_connection = con.Connection(self.correctToken)
        self.assertIsNotNone(self._twitter_connection)

  
    
    def test_should_throw_exception_when_token_beare_is_none(self):
        with self.assertRaises(Exception) as context:
            con.Connection(None)
        self.assertEqual(str(context.exception), "Token bearer should not be none")

    @mock.patch('requests.get', side_effect=mocked__request_get_user_by_id)
    def test_should_get_401_response_and_unauthorised_json(self, mock_get):
        twitter_connection = con.Connection(self.invalid_token)
        with self.assertRaises(Exception) as contex:
            twitter_connection.getUserById(_user_id)
        self.assertTrue("with code 401" in str(contex.exception))
        self.assertTrue(str(_unauthroised_json) in  str(contex.exception))

    @mock.patch('requests.get', side_effect=mocked__request_get_user_by_id)
    def test_should_get_data_of_the_user(self, mock_get):
        response = self._twitter_connection.getUserById(_user_id)
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
                                "data": {
                                    "name": "Piotr",
                                    "created_at": "2021-11-15T17:49:39.000Z",
                                    "protected": False,
                                    "username": "Piotr63632005",
                                    "id": "1460303834790731778",
                                    "description": "",
                                    "verified": False,
                                    "public_metrics": {
                                        "followers_count": 1,
                                        "following_count": 27,
                                        "tweet_count": 96,
                                        "listed_count": 0
                                        }
                                    }
                                })
    
    @mock.patch('requests.get', side_effect=mocked__request_get_user_by_id)
    def test_should_return_create_url_with_specified_user_id(self, mock_get):

        self._twitter_connection.getUserById(_user_id)
        url = "https://api.twitter.com/2/users/{}".format(_user_id)
        self.assertEqual(url,mock_get.call_args_list[0][0][0], "Url not correctly created")

    

    @mock.patch('requests.get', side_effect=mocked__request_get_user_timeline_id)
    def test_should_get_user_time_line(self, mock_get):
        response = self._twitter_connection.get_user_time_line(_user_id)
        self.assertIsNotNone(response)
        url = "https://api.twitter.com/2/users/{}/tweets".format(_user_id)
        self.assertEqual(url,mock_get.call_args_list[0][0][0], "Url not correctly created")
    
    @mock.patch('requests.get', side_effect=mocked__request_get_user_timeline_id)
    def test_should_add_to_request_all_twitt_params(self, mock_get):
        self._twitter_connection.get_user_time_line(_user_id)
        all_twitt_params = {    "tweet.fields":"created_at,text,geo,source,lang",
                                "max_results" : 100,
                                "place.fields" : "contained_within,country,country_code,full_name,geo,id,name,place_type",
                                "expansions" : "geo.place_id"}
        self.assertDictEqual(all_twitt_params, mock_get.call_args_list[0][1]['params'])

    @mock.patch('requests.get', side_effect=mocked__request_get_user_timeline_id)
    def test_should_query_user_timeline_from_specfied_token(self, mock_get):
        next_token = "7140dibdnow9c7btw423wysghff0nn2wdepybrvft9d88"
        self._twitter_connection.get_user_time_line(_user_id, next_token= next_token)
        print(mock_get.call_args_list[0][1]['params'])
        self.assertEqual(next_token, mock_get.call_args_list[0][1]['params']['pagination_token'], "Should add connection token to params when specified")
        
        self._twitter_connection.get_user_time_line(_user_id)
        self.assertNotIn('pagination_token', mock_get.call_args_list[1][1]['params'] )

    @mock.patch('requests.get', side_effect=mocked__request_get_user_timeline_id)
    def test_should_create_correct_url_when_calling_for_tweet_likers(self,mock_get):
        twitt_id = "1234123123"
        expected_url = "https://api.twitter.com/2/tweets/{}/liking_users".format(twitt_id)

        self._twitter_connection.get_user_who_liked_the_twitt(twitt_id)

        # Then
        self.assertEquals(expected_url,mock_get.call_args_list[0][0][0], "Url not corretly created" )


    @mock.patch('requests.get', side_effect=mocked__request_get_user_timeline_id)
    def test_should_have_all_twitt_param_when_calling_for_tweet_likers(self,mock_get):
        twitt_id = "1234123123"
        response = self._twitter_connection.get_user_who_liked_the_twitt(twitt_id)
        self.assertIsNotNone(response)
        all_twitt_params = {    "tweet.fields":"created_at,text,geo,source,lang",
                                "max_results" : 100,
                                "place.fields" : "contained_within,country,country_code,full_name,geo,id,name,place_type",
                                "expansions" : "geo.place_id"}
        self.assertDictEqual(all_twitt_params, mock_get.call_args_list[0][1]['params'])
    # Co ja teraz chece zrobić? Chce zeby łączył się do twittera i pobierał informacje na temat uzytkownikow

    @mock.patch('requests.get', side_effect=mocked__request_get_user_timeline_id)
    def test_should_add_next_token_parm_only_when_specified(self, mock_get):
        next_token = "7140dibdnow9c7btw423wysghff0nn2wdepybrvft9d88"
        twitt_id = "1234123123"
        self._twitter_connection.get_user_who_liked_the_twitt(twitt_id,  pagination_token= next_token)

 
        self.assertEqual(next_token, mock_get.call_args_list[0][1]['params']['pagination_token'], "Should add connection token to params when specified")
        self._twitter_connection.get_user_time_line(_user_id)
        self.assertNotIn('pagination_token', mock_get.call_args_list[1][1]['params'] )

    @mock.patch('requests.get', side_effect=mocked__request_return_error)
    def test_should_raise_error_when_respose_code_diffrent_then_200(self, mock_get):
        with self.assertRaises(Exception) as context:
            self._twitter_connection.get_user_time_line(123)
        self.assertTrue( str(_error_json) in str(context.exception))

        with self.assertRaises(Exception) as context:
            self._twitter_connection.get_user_who_liked_the_twitt(123)
        self.assertTrue( str(_error_json) in str(context.exception))

        with self.assertRaises(Exception) as context:
            self._twitter_connection.getUserById(123)
        self.assertTrue( str(_error_json) in str(context.exception))
