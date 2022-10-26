import requests


class Connection():
    def __init__(self, token):
        self._throw_exception_when_token_beare_is_None(token)
        self._token = token

    def _throw_exception_when_token_beare_is_None(self, token):
        if token is None:
            raise Exception("Token bearer should not be none")


    def getUserById(self,id):
        print(id)
        url = "https://api.twitter.com/2/users/{}".format(id)
        params = { "user.fields":"created_at,description,entities,id,location,name,profile_image_url,public_metrics,protected,url,username"}
        headers = {"Authorization": "Bearer {}".format(self._token)}
        return  requests.get(url, headers = headers, params = params)