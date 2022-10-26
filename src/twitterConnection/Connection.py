from re import S
import requests


class Connection():
    def __init__(self, token):
        self._throw_exception_when_token_beare_is_None(token)
        self._token = token
        self._params = {"user.fields":"created_at,description,entities,id,location,name,profile_image_url,public_metrics,protected,url,username"}
        self._headers = {"Authorization": "Bearer {}".format(self._token)}
        self._twitt_parms = {   "tweet.fields":"created_at,text,geo,source,lang",
                                "max_results" : 100,
                                "place.fields" : "contained_within,country,country_code,full_name,geo,id,name,place_type",
                                "expansions" : "geo.place_id"
                            }

    def _throw_exception_when_token_beare_is_None(self, token):
        if token is None:
            raise Exception("Token bearer should not be none")


    def getUserById(self,id):
        url = "https://api.twitter.com/2/users/{}".format(id)  
        return  requests.get(url, headers = self._headers, params = self._params)

    def get_user_time_line(self, id, next_token = None):
        twitt_params = self._twitt_parms.copy()
        self._add_pagination_token_if_exists(next_token, twitt_params)
        url = "https://api.twitter.com/2/tweets/{}".format(id)
        return requests.get(url, headers = self._headers, params = twitt_params)
    
    def get_user_who_liked_the(self,twitt_id, pagination_token = None):
        twitt_params = self._twitt_parms.copy()
        self._add_pagination_token_if_exists(pagination_token, twitt_params)
        url = "https://api.twitter.com/2/tweets/{}/liking_users".format(twitt_id)
        return requests.get(url, headers = self._headers, params = twitt_params)

    def _add_pagination_token_if_exists(self, pagination_token, params):
        if pagination_token:
            params['pagination_token'] = pagination_token
            pagination_token = None
        return params