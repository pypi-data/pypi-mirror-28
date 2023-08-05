import requests
import urllib
import urllib.parse


class Client:

    API_BASE_URL = "https://api.utopian.io/api/"

    def _generate_url(self, action, query_params=None):

        if query_params:
            if not isinstance(query_params, dict):
                raise TypeError(
                    "query_string variable should be a dictionary.")

        if query_params:
            action = "{}/?{}".format(
                action, urllib.parse.urlencode(query_params))

        abs_url = urllib.parse.urljoin(self.API_BASE_URL, action)

        return abs_url

    @property
    def moderators(self):
        return requests.get(self._generate_url("moderators")).json()

    @property
    def sponsors(self):
        return requests.get(self._generate_url("sponsors")).json()

    def is_moderator(self, account):
        return account in [m["account"] for m in self.moderators["results"]]

    def is_sponsor(self, account):
        return account in [m["account"] for m in self.sponsors["results"]]

    def posts(self, query_params=None):
        if not query_params:
            query_params = {}

        return requests.get(
            self._generate_url("posts", query_params=query_params)).json()

    def post(self, account, permlink):
        return requests.get(
            self._generate_url("posts/%s/%s" % (account, permlink))).json()

    @property
    def stats(self):
        return requests.get(self._generate_url("stats")).json()["stats"]

    @property
    def bot_is_voting(self):
        return self.stats["bot_is_voting"]

    def count(self, query_params=None):
        if not query_params:
            query_params = {"limit": 1}
        else:
            query_params.update({"limit": 1})

        return self.posts(query_params)["total"]