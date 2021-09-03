from match import Match
from match_list import MatchList
from summoner_id import Summoner
import csv
import os
import pandas as pd
import time

stats_available = ['win', 'kills', 'deaths', 'assists', 'largestKillingSpree', 'largestMultiKill', 'killingSprees',
                   'longestTimeSpentLiving', 'doubleKills', 'tripleKills', 'quadraKills', 'pentaKills',
                   'totalDamageDealt', 'magicDamageDealt', 'physicalDamageDealt', 'trueDamageDealt',
                   'totalDamageDealtToChampions', 'magicDamageDealtToChampions', 'physicalDamageDealtToChampions',
                   'trueDamageDealtToChampions', 'totalHeal', 'damageSelfMitigated', 'timeCCingOthers',
                   'totalDamageTaken', 'goldEarned', 'goldSpent', 'totalTimeCrowdControlDealt']

# Intro asking for needed information
API_KEY = os.environ['API_KEY']

summoner = Summoner(api_key=API_KEY)

# get summoner name
ign = input('What is you League in-game name?: ')
summoner.get_info(ign)
account_id = summoner.account_id

match_list = MatchList(API_KEY, account_id)
match = Match(API_KEY)


def create_new_dataset():
    choice1 = True
    match_listing = []
    while choice1:
        choice = input('Type "all" if you want to see all ARAM matches, or "select" for a selection: ').lower()

        # Selecting type of search
        if choice == 'select':
            choice_start = input('Where would you like to start the selection? (most recent is "0"): ')
            choice_end = input('Where would you like to end the selection? (not inclusive): ')
            match_listing = match_list.get_select_matches(choice_start, choice_end)
            choice1 = False
        elif choice == 'all':
            match_listing = match_list.get_all_matches()
            choice1 = False
        else:
            print('Please enter a valid answer.')

    match_listing = match.find_match_ids(match_listing)
    match_stats = []
    counter = 0

    # loop for finding info for each match
    for item in match_listing:
        # # finding info for particular match and adding initial info
        match_info = match.match_info(item['gameId'])
        participant_num = ''
        stat = {'game_id': item['gameId'],
                'game_duration': match_info.get('gameDuration')}

        # # finding player number in json data
        for y in range(10):
            if match_info['participantIdentities'][y]['player'].get('accountId') == account_id:
                participant_num = y
                break
        # # getting summoner stats
        requested_summoner = match_info['participants'][participant_num]
        stat.update(match.find_summoner_stats(requested_summoner, *stats_available))

        # # append to match_stats list
        match_stats.append(stat)

        counter += 1
        if counter == 100:
            time.sleep(125)
            counter = 0
        else:
            time.sleep(0.5)

    # write data into .csv file
    csv_header = ['game_id', 'game_duration', 'champion', *stats_available]

    with open('aram-data1.csv', newline="", mode='w', encoding='utf8') as file:
        writer = csv.DictWriter(file, fieldnames=csv_header)
        writer.writeheader()
        for x in range(0, len(match_stats)):
            stat_to_write = {header: match_stats[x][header] for header in csv_header}
            writer.writerow(stat_to_write)

    return print('\nTask Completed.')


def update_dataset():
    try:
        data = pd.read_csv('aram-data1.csv')
    except FileNotFoundError:
        return print('File Not Found. Try creating a dataset instead.')
    else:
        most_recent_game = data.game_id[0]

    choice2 = True
    match_listing = []
    while choice2:
        choice = input('Type "all" if you want to select all ARAM matches, or "select" for a selection: ').lower()

        # Selecting type of search
        if choice == 'select':
            choice_start = input('Where would you like to start the selection? (most recent is "0"): ')
            choice_end = input('Where would you like to end the selection? (not inclusive): ')
            match_listing = match_list.get_select_matches(choice_start, choice_end)
            choice2 = False
        elif choice == 'all':
            match_listing = match_list.get_all_matches()
            choice2 = False
        else:
            print('Please enter a valid answer.')

    match_listing = match.find_match_ids(match_listing)

    # checking if the most recent game in dataset is present in the search
    recent_game_index = match_listing.index({'gameId': most_recent_game})
    if recent_game_index:
        match_listing = match_listing[:recent_game_index]

    match_stats = []

    # loop for finding info for each match
    for item in match_listing:
        # # finding info for particular match and adding initial info
        match_info = match.match_info(item['gameId'])
        participant_num = ''
        stat = {'game_id': match_info['gameId'],
                'game_duration': match_info['gameDuration']}

        # # finding player number in json data
        for y in range(10):
            if match_info['participantIdentities'][y]['player']['accountId'] == account_id:
                participant_num = y
                time.sleep(1.5)
                break
        # # getting summoner stats
        requested_summoner = match_info['participants'][participant_num]
        stat.update(match.find_summoner_stats(requested_summoner, *stats_available))

        # # append to match_stats list
        match_stats.append(stat)

    # write data into .csv file
    csv_header = ['game_id', 'game_duration', 'champion', *stats_available]
    # creating a csv -> dataframe for the new stats
    with open('aram-data-transfer.csv', newline="", mode='w', encoding='utf8') as file:
        writer = csv.DictWriter(file, fieldnames=csv_header)
        writer.writeheader()
        for x in range(0, len(match_stats)):
            stat_to_write = {header: match_stats[x][header] for header in csv_header}
            writer.writerow(stat_to_write)

    # appending old stats to new stats so that the recent stat is on top
    data_new = pd.read_csv('aram-data-transfer.csv')
    data_new = data_new.append(data, ignore_index=True)

    # replacing the original file with one up-to-date and deleting the in-between file
    data_new.to_csv('aram-data1.csv')
    os.remove('aram-data-transfer.csv')

    return print('\nTask Completed.')


new_dataset_loop = True
while new_dataset_loop:
    path1 = input('Do you want to create a new Aram stat dataset? (y/n): ')
    if path1 == 'y':
        create_new_dataset()
        new_dataset_loop = False
    elif path1 == 'n':
        new_dataset_loop = False
    else:
        print('Please enter a valid answer.')


update_loop = True
while update_loop:
    path2 = input('\nDo you want to update you Aram stats? (y/n): ').lower()
    if path2 == 'y':
        update_dataset()
        update_loop = False
    elif path2 == 'n':
        update_loop = False
    else:
        print('Please enter a valid answer.')

