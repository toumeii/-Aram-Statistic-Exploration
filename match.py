import requests


class Match:
    def __init__(self, api_key):
        self.api_key = api_key
        self.match_list = None
        self.requested_summoner = None

    def find_match_ids(self, match_list):
        """

        :param match_list: an instance of the match_list class
        :return: list of match ids from the match_list
        """
        self.match_list = match_list
        match_elements = []
        for item in self.match_list:
            match_item_search = {'gameId': item['gameId']}
            match_elements.append(match_item_search)

        return match_elements

    def match_info(self, match_id):
        """

        :param match_id: match id (long) obtained from the find_match_ids function
        :return: json with match info
        """
        platform_route = 'https://na1.api.riotgames.com'
        header = {"Origin": "https://developer.riotgames.com",
                  "api_key": self.api_key}
        response = requests.get(f'{platform_route}/lol/match/v4/matches/{match_id}',
                                params=header)
        data = response.json()
        return data

    def find_summoner_stats(self, requested_player, *args):
        """

        :param requested_player: the path/location of the summoner in the match_info json.
        :param args: the statistic you would like to look for.
        :return: dictionary of queried stats.
        """
        self.requested_summoner = requested_player
        stat_element_dict = {'champion': self.requested_summoner['championId']}
        for arg in args:
            try:
                stat_element_dict[arg] = self.requested_summoner['stats'][arg]
            except KeyError:
                continue

        return stat_element_dict
