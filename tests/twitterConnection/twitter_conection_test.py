import unittest
from src.twitterConnection import Connection as con
from unittest import mock

class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code
    def json(self):
        return self.json_data

_user_id = 1460303834790731778

# In *arg there is a url specified and **kwargs contains  dict with keys {header, params}
def mocked__request_get_user_by_id(*args, **kwargs):

    url = "https://api.twitter.com/2/users/1460303834790731778"
    print(kwargs['headers'])
    if args[0] != url:
        return ""
    if kwargs['headers'] == {'Authorization': 'Bearer Invalid'}:
        return MockResponse({
                                "title": "Unauthorized",
                                "type": "about:blank",
                                "status": 401,
                                "detail": "Unauthorized"
                            }, 401)
    elif kwargs['headers'] == {'Authorization': 'Bearer Token'}:
        return MockResponse({
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
                                }, 200)

    return MockResponse({"key":"val"}, 400)
    

class TwitterConncectionTest(unittest.TestCase):
    

    def setUp(self) -> None:
        self.correctToken = "Token"
        self.invalidToken = "Invalid"
        self._twitterConnection = con.Connection(self.correctToken)
        self.assertIsNotNone(self._twitterConnection)

  
        

    def test_should_throw_exception_when_token_beare_is_none(self):
        with self.assertRaises(Exception) as context:
            con.Connection(None)
        self.assertEqual(str(context.exception), "Token bearer should not be none")

    @mock.patch('requests.get', side_effect=mocked__request_get_user_by_id)
    def test_should_get_401_response_and_unauthorised_json(self, mock_get):
        bearer_token = "Invalid"
        twitterConnection = con.Connection(bearer_token)
        response = twitterConnection.getUserById(_user_id)
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {
                                "title": "Unauthorized",
                                "type": "about:blank",
                                "status": 401,
                                "detail": "Unauthorized"
                            })

    @mock.patch('requests.get', side_effect=mocked__request_get_user_by_id)
    def test_should_get_data_of_the_user(self, mock_get):
        bearer_token = "Token"
        twitterConnection = con.Connection(bearer_token)
        response = twitterConnection.getUserById(_user_id)
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
        bearer_token = "Token"
        user_id = 122333333
        twitterConnection = con.Connection(bearer_token)
        twitterConnection.getUserById(user_id)
        url = "https://api.twitter.com/2/users/{}".format(user_id)
        self.assertEqual(url,mock_get.call_args_list[0][0][0], "Url not correctly created")

    

    # def test_should_get_user_time_line(self):


    # Co ja teraz chece zrobić? Chce zeby łączył się do twittera i pobierał informacje na temat uzytkownikow
        








    # Co ja teraz chece zrobić? Chce zeby łączył się do twittera i pobierał informacje na temat uzytkownikow