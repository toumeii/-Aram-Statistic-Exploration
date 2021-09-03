import json
import csv

with open('champion_data/champion.json', encoding='utf8') as file:
    data = json.load(file)
    champion_data = data['data']

champion_key_id = [{'champion': champion_data[champion]['key'],
                    'name': champion} for champion in champion_data]


# print(champion_key_id)
csv_header = ['champion', 'name']
with open('champion_data/league_champion_key.csv', newline='', mode='w', encoding='utf8') as file1:
    writer = csv.DictWriter(file1, fieldnames=csv_header)
    writer.writeheader()
    for champion in champion_key_id:
        writer.writerow(champion)
