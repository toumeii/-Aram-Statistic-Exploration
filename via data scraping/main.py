from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import csv
import time

chrome_driver_path = "C:/Users/Tommy/Downloads/python/chromedriver.exe"

summoner_name = input('What is your summoner name?\n')
if summoner_name:
    driver = webdriver.Chrome(executable_path=chrome_driver_path)
    driver.get(f"https://na.op.gg/summoner/userName={summoner_name}")

    # selecting aram queue type
    queue_type = driver.find_element_by_class_name('SelectMatchTypes')
    queue_type.click()
    aram = driver.find_element_by_xpath(
        '/html/body/div[2]/div[3]/div/div/div[5]/div[2]/div[2]/div/div[1]/div/ul/li[4]/span/select/option[3]')
    aram.click()
    time.sleep(1)

    # expand match history to max of site
    show_more_button = driver.find_element_by_class_name('GameMoreButton')
    while show_more_button:
        show_more_button.click()
        time.sleep(1.5)
        try:
            show_more_button = driver.find_element_by_class_name('GameMoreButton')
        except NoSuchElementException:
            break

    # finding date/time of games
    dates = driver.find_elements_by_css_selector('.GameItemWrap ._timeago')
    date = [dt.get_attribute('title') for dt in dates]

    # finding game results (victory or defeat)
    win_status = driver.find_elements_by_class_name('GameResult')
    game_results = [game.text for game in win_status]

    # finding game time
    time_elapsed = driver.find_elements_by_css_selector('.GameItemWrap .GameLength')
    game_time = [t.text for t in time_elapsed]

    # finding champion played
    champions = driver.find_elements_by_css_selector('.GameItemWrap .ChampionName')
    champion_name = [name.text for name in champions]

    # finding kill score
    kills = driver.find_elements_by_css_selector('.GameItemWrap .KDA .KDA .Kill')
    kill_score = [kill.text for kill in kills]

    # finding death score
    deaths = driver.find_elements_by_css_selector('.GameItemWrap .KDA .Death')
    death_score = [death.text for death in deaths]

    # finding assist score
    assists = driver.find_elements_by_css_selector('.GameItemWrap .KDA .Assist')
    assist_score = [assist.text for assist in assists]

    # finding damage score
    game_detail_buttons = driver.find_elements_by_id('right_match')
    for button in game_detail_buttons:
        button.click()
        time.sleep(.5)

    damage = driver.find_elements_by_css_selector('.GameItemWrap .GameDetail .isRequester .ChampionDamage')
    damage_score = [dmg.text for dmg in damage]

    time.sleep(1)

    # write data into .csv file
    csv_header = ['date', 'game_result', 'game_time', 'champion', 'kills', 'deaths', 'assists', 'damage']

    try:
        file = open("aram-data.csv", newline="", mode='a', encoding="utf8")
    except FileNotFoundError:
        file = open('aram-data.csv', newline="", mode='w', encoding='utf8')
    else:
        writer = csv.DictWriter(file, fieldnames=csv_header)
        writer.writeheader()
        for x in range(0, len(game_results)):
            writer.writerow({'date': date[x],
                             'game_result': game_results[x],
                             'game_time': game_time[x],
                             'champion': champion_name[x],
                             'kills': kill_score[x],
                             'deaths': death_score[x],
                             'assists': assist_score[x],
                             'damage': damage_score[x]})

    driver.quit()
