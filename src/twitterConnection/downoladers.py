import pandas as pd
import logging
from  src.twitterConnection.Connection import Connection

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

class TimeLineDownloader:
    """
    Object for downloading whole timeline user with id given in constructor
    """
    def __init__(self, user_id : str, connection) -> None:
        self._user_id = user_id
        logging.debug("Creating Timeline downloader for user with id = {}".format(self._user_id))
        self.connection = connection
    
    def download(self) -> pd.DataFrame:
        logging.debug("Starting downoading timeline for with id = {}".format(self._user_id))
        self.connection.get_user_time_line(self._user_id)
        return pd.DataFrame({'text':['text','text'], 'id':[1234,123]})
