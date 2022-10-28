import unittest
import pandas as pd
import json
from src.twitterConnection.Connection import Connection

from src.twitterConnection.downoladers import TimeLineDownloader

def mocked_get_user_timeline(*args, **kwargs):
    print("Get mocked timeline")
    response = None
    with open('tests/test_resources/user_timeline_1', "r") as file:
        response = json.loads(file.read())
    return response


class DownloadersTest(unittest.TestCase):


    def setUp(self) -> None:
        self._user_id =  "1234555"
        self._conectionMock = Connection("Token Bearer")
        self._conectionMock.get_user_time_line = mocked_get_user_timeline
        self.downloader = TimeLineDownloader(self._user_id, self._conectionMock)

        # check if correctly created
        self.assertIsNotNone(self.downloader)
        self.assertEquals(self._user_id, self.downloader._user_id)
    
    
    def test_should_retrun_data_frame_with_usertimeline(self):
        frame = self.downloader.download()
        self.assertIsNotNone(frame)
        self.assertTrue(isinstance(frame, pd.DataFrame))
        self.assertTrue('id' in frame.columns)
    
   
    def test_should_retrun_data_frame_with_twitts_from_multiple_rquestes(self):
        self.downloader.download()
             
        # powinien wysłać jeszcze raz zapytanie jezeli w responsie jest next_token

    

