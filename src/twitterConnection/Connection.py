import requests


class Connection():
    def __init__(self, token):
        self._throw_exception_when_token_beare_is_None(token)
        self._token = token
        self._params = {"user.fields":"created_at,description,entities,id,location,name,profile_image_url,public_metrics,protected,url,username"}
        self._headers = {"Authorization": "Bearer {}".format(self._token)}
    def _throw_exception_when_token_beare_is_None(self, token):
        if token is None:
            raise Exception("Token bearer should not be none")


    def getUserById(self,id):
        url = "https://api.twitter.com/2/users/{}".format(id)  
        return  requests.get(url, headers = self._headers, params = self._params)

    def get_user_time_line(self, id):
        url = "https://api.twitter.com/2/tweets/{}".format(id)
        return requests.get(url, headers = self._headers, params = self._params)