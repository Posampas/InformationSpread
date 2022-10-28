import unittest
import pandas as pd
import json

from src.twitterConnection.Connection import Connection
from tests.twitterConnection.test_helpers import MockResponse
from src.twitterConnection.downoladers import TimeLineDownloader

def get_test_response_from_file(file_name):
    with open(file_name, "r") as file:
        response = json.loads(file.read())
        print(response)
    return MockResponse(response, 200)

def mocked_get_user_timeline(*args, **kwargs):
    response = None
    print(args)
    if len(args) == 1: # nie ma podanego next_token:
        return get_test_response_from_file('tests/test_resources/user_timeline_1')
    elif args[1] =="7140dibdnow9c7btw420jpwbt9wmymda1a3snunjakt2x":
        return get_test_response_from_file('tests/test_resources/user_timeline_2')
    elif args[1] =="7140dibdnow9c7btw3z3q3hel9tvq54dnkct8vtahdfli":
        return get_test_response_from_file('tests/test_resources/user_timeline_3')
    elif args[1] =="7140dibdnow9c7btw3z3al40a1f3wlmppej16o8i1kf8w":
        return get_test_response_from_file('tests/test_resources/user_timeline_4')

class DownloadersTest(unittest.TestCase):

    def setUp(self) -> None:
        self._user_id = "1234555"
        self._conectionMock = Connection("Token Bearer")
        self._conectionMock.get_user_time_line = mocked_get_user_timeline
        self.downloader = TimeLineDownloader(
            self._user_id, self._conectionMock)

        # check if correctly created
        self.assertIsNotNone(self.downloader)
        self.assertEquals(self._user_id, self.downloader._user_id)

    def test_should_retrun_data_frame_with_usertimeline(self):
        frame = self.downloader.download()
        self.assertIsNotNone(frame)
        self.assertTrue(isinstance(frame, pd.DataFrame))
        self.assertTrue('id' in frame.columns)

    def test_should_retrun_data_frame_with_twitts_from_multiple_rquestes(self):

        frame = self.downloader.download()
        print(frame.head())
        print(frame.columns)
        self.assertEqual(len(frame), 96)



    def test_should_remove_by_defaoult_column_edit_tweet_hisotry(self):
        columns = ['text', 'created_at', 'geo', 'lang', 'id', 'source']
        frame = self.downloader.download()
        self.assertListEqual(columns, frame.columns.to_list())
