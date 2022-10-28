from operator import concat
import pandas as pd
import logging

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)


class TimeLineDownloader:
    """
    Object for downloading whole timeline user with id given in constructor
    """

    def __init__(self, user_id: str, connection) -> None:
        self._user_id = user_id
        logging.info(
            "Creating Timeline downloader for user with id = {}".format(self._user_id))
        self._connection = connection
        self._frame = None
        self._pagination_token = None

    def download(self, columns_to_drop=['edit_history_tweet_ids']) -> pd.DataFrame:
        """
            Input:
            columns_to_drop - columns that will be droped from result if are present in data

            Output:
            dataframe containg all usertimeline tweet that can be downloaded
        """
        logging.info(
            "Starting downoading timeline for with id = {}".format(self._user_id))

        send_request = True
        while send_request:
            response = self._send_request(self._pagination_token)
            if ('data' in response.json()):
                frame = self._create_frame(response.json()['data'], columns_to_drop)
                self._append_to_final_dataframe(frame)
                if ('meta' in response.json() and 'next_token' in response.json()['meta']):
                    logging.info("Pagination token found. Download continues")
                    self._pagination_token = response.json()['meta']['next_token']
                else:
                    logging.info("Pagination token not found. Download terminated")
                    send_request = False
        return self._frame 



    def _send_request(self, pagination_token):
        if pagination_token:
            logging.info("Sending timeline request with pagination token {} ".format(pagination_token))
            return self._connection.get_user_time_line(self._user_id, pagination_token)
        else:
            logging.info("Sending timeline request without pagination token.")
            return self._connection.get_user_time_line(self._user_id)

    def _create_frame(self, data, columns_to_drop):
        logging.info("Create dataframe with {}".format(data))
        frame = pd.DataFrame(data)
        logging.info("Columns in dataframe {}, and columns to drop {}".format(frame.columns, columns_to_drop))
        for column in columns_to_drop:
            logging.info("Checking if column {} is in {}".format(column, frame.columns))
            if column in frame.columns:
                logging.info("Droping column {}".format( column))
                frame = frame.drop([column], axis=1)
        logging.info("Resulting columns {}".format(frame.columns))
        logging.info("Downloaded {} twitts".format(len(frame)))
        return frame

    def _append_to_final_dataframe(self, frame):
        logging.info("Appending to finalData frame")
        if self._frame is None:
            self._frame = frame
        else:
            self._frame = pd.concat([self._frame,frame ], axis=0, ignore_index=True)
        logging.info("Result dataframe length {}".format(len(self._frame)))