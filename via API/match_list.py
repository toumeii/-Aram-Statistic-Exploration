import requests
import time

# using matchv4 api which will be deprecated by sept 6, 2021
# matchv5 does not have the same functionality yet so until then matchv4 is used.


class MatchList:
    def __init__(self, api_key, account_id):
        """
        :param api_key: key for the api (string)
        :param account_id: encrypted account_id (string)
        """
        self.api_key = api_key
        self.account_id = account_id

    def get_select_matches(self, *args, **kwargs):
        """
        :param args: for 2 variables, beginIndex and endIndex, respectively.
        :param kwargs: see below
            :keyword Arguments:
                * beginIndex (inclusive)
                * endIndex (exclusive)
        :return: set of Aram matches as json.
        """
        if args:
            header = {"Origin": "https://developer.riotgames.com",
                    "api_key": self.api_key,
                    "queue": 450,
                    "beginIndex": args[0],
                    "endIndex": args[1]}
        if kwargs:
            header = {"Origin": "https://developer.riotgames.com",
                    "api_key": self.api_key,
                    "queue": 450,
                    "beginIndex": kwargs.get('beginIndex'),
                    "endIndex": kwargs.get('endIndex')}

        platform_route = 'https://na1.api.riotgames.com'
        response = requests.get(f'{platform_route}/lol/match/v4/matchlists/by-account/{self.account_id}',
                                params=header)
        data = response.json()['matches']

        return data

    def get_all_matches(self):
        """
        :return: all Aram matches found in the api for the summoner in json
        """
        datalist = []
        data = [{'': ''}]
        begin = 0
        end = 100
        while data:
            header = {"Origin": "https://developer.riotgames.com",
                        "api_key": self.api_key,
                        "queue": 450,
                        "beginIndex": begin,
                        "endIndex": end}

            platform_route = 'https://na1.api.riotgames.com'
            response = requests.get(f'{platform_route}/lol/match/v4/matchlists/by-account/{self.account_id}',
                                    params=header)
            data = response.json()['matches']
            datalist += data
            time.sleep(10)

            begin += 100
            end += 100

        time.sleep(20)
        return datalist
