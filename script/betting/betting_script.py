from helper.http_helper import HttpHelper


class OddsApi:

    def __init__(self):
        self.api_key = "971ab9a183421468ae238560c8e88fd0"
        self.uri = "https://api.the-odds-api.com"

    def get_url(self, endpoint):
        return self.uri + endpoint % self.api_key


def call_odds_api_for_sport_key():
    endpoint = "/v4/sports/?apiKey=%s"
    key = "icehockey_nhl"
    url = OddsApi().get_url(endpoint)

    return HttpHelper.get(url)

def call_odds_api_for_sport():
    sport = "icehockey_nhl"
    region = "us"
    market = "totals"
    endpoint = f"/v4/sports/{sport}/odds/?apiKey=%s&regions={region}&markets={market}"
    url = OddsApi().get_url(endpoint)

    return HttpHelper.get(url)


if __name__ == '__main__':
    print(call_odds_api_for_sport())
