import requests


class Summoner:
    def __init__(self, **kwargs):
        """

        :param kwargs:
            see below.
        :keyword Arguments:
            * summoner_id
            * account_id
            * puuid
            * summoner_name
            * api_key
        """
        self.summoner_id = kwargs.get('summoner_id')
        self.account_id = kwargs.get('account_id')
        self.puuid = kwargs.get('puuid')
        self.summoner_name = kwargs.get('summoner_name')
        self.summoner_level = 0
        self.api_key = kwargs.get('api_key')

    def get_info(self, name):
        """

        :param name: League of Legends in-game name (string).
        :return: None
        """
        header = {"Origin": "https://developer.riotgames.com",
                  "api_key": self.api_key}
        platform_route = 'https://na1.api.riotgames.com'

        response = requests.get(f'{platform_route}/lol/summoner/v4/summoners/by-name/{name}',
                                params=header)
        data = response.json()
        self.summoner_id = data['id']
        self.account_id = data['accountId']
        self.puuid = data['puuid']
        self.summoner_level = data['summonerLevel']
        self.summoner_name = data['name']

        # if kwargs.get('summoner_name'):
        #     response = requests.get(f'{platform_route}/lol/summoner/v4/summoners/by-name/{self.summoner_name}',
        #                             params=header)
        #     data = response.json()
        #     self.summoner_id = data['id']
        #     self.account_id = data['accountId']
        #     self.puuid = data['puuid']
        #     self.summoner_level = data['summonerLevel']
        #     self.summoner_name = data['name']
        # elif kwargs.get('summoner_id'):
        #     response = requests.get(f'{platform_route}/lol/summoner/v4/summoners/{self.summoner_id}',
        #                             params=header)
        #     data = response.json()
        #     self.summoner_name = data['name']
        #     self.account_id = data['accountId']
        #     self.puuid = data['puuid']
        #     self.summoner_level = data['summonerLevel']
        #     self.summoner_id = data['id']
        # elif kwargs.get('account_id'):
        #     response = requests.get(f'{platform_route}/lol/summoner/v4/summoners/by-account/{self.account_id}',
        #                             params=header)
        #     data = response.json()
        #     self.summoner_id = data['id']
        #     self.summoner_name = data['name']
        #     self.puuid = data['puuid']
        #     self.summoner_level = data['summonerLevel']
        #     self.summoner_level = data['accountId']
        # elif kwargs.get('puuid'):
        #     response = requests.get(f'{platform_route}/lol/summoner/v4/summoners/by-puuid/{self.puuid}',
        #                             params=header)
        #     data = response.json()
        #     self.summoner_id = data['id']
        #     self.account_id = data['accountId']
        #     self.summoner_name = data['name']
        #     self.summoner_level = data['summonerLevel']
        #     self.puuid = data['puuid']

