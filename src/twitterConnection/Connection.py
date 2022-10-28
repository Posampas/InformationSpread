from email import message
from re import S
import requests
import logging
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)



class Connection():
    def __init__(self, token):
        logging.info("Creating Connection with token {}".format(token))
        self._throw_exception_when_token_beare_is_None(token)
        self._token = token
        self._params = {"user.fields":"created_at,description,entities,id,location,name,profile_image_url,public_metrics,protected,url,username"}
        self._headers = {"Authorization": "Bearer {}".format(self._token)}
        self._twitt_parms = {   "tweet.fields":"created_at,text,geo,source,lang",
                                "max_results" : 30,
                                "place.fields" : "contained_within,country,country_code,full_name,geo,id,name,place_type",
                                "expansions" : "geo.place_id",
                                # "place.fields" : "country_code,full_name,geo,id,name,place_type"
                            }

    def _throw_exception_when_token_beare_is_None(self, token):
        if token is None:
            raise Exception("Token bearer should not be none")

    def _sent_get(self, url, headers, params) -> requests.models.Response:
        response = requests.get(url, headers = headers, params = params)
        logging.info("Response:\n{}".format(response.json()))
        if (response.status_code != 200):
            raise RuntimeError("""Request failed with code {},
                                    response json:
                                    {}
                                """.format(response.status_code,response.json()))
        return response


    def getUserById(self,id):
        url = "https://api.twitter.com/2/users/{}".format(id)  
        logging.info("Sending get request to {} with {}".format(url, self._params))
        return  self._sent_get(url, headers = self._headers, params = self._params)

    def get_user_time_line(self, id, next_token = None, max_results = 100):
        twitt_params = self._twitt_parms.copy()
        self._add_pagination_token_if_exists(next_token, twitt_params)
        twitt_params['max_results'] = max_results
        url = "https://api.twitter.com/2/users/{}/tweets".format(id)
        logging.error("Sending get request to {} with {}".format(url, self._params))
        return self._sent_get(url, headers = self._headers, params = twitt_params)
    
    def get_user_who_liked_the_twitt(self,twitt_id, pagination_token = None, max_results = 100):
        twitt_params = self._twitt_parms.copy()
        self._add_pagination_token_if_exists(pagination_token, twitt_params)
        twitt_params['max_results'] = max_results
        url = "https://api.twitter.com/2/tweets/{}/liking_users".format(twitt_id)
        logging.info("Sending get request to {} with {}".format(url, self._params))
        return self._sent_get(url, headers = self._headers, params = twitt_params)

    def _add_pagination_token_if_exists(self, pagination_token, params):
        if pagination_token:
            params['pagination_token'] = pagination_token
            pagination_token = None
        return params
