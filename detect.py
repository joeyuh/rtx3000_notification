import requests
import faker
import time
import random
import json

from settings import *

fake = faker.Faker()

f = open('user-agents_chrome_browser_win10_64.json')
win10_user_agents = json.load(f)


def bestbuy_detect(link: str, v, a, lock):
    fails = 0
    while True:
        if fails > Settings.MAX_RETRIES:
            print("Max retries used. Continuing. Maybe check Internet connection.")
            return False
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Referer": "https://www.google.com/",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": fake.chrome(version_from=75, version_to=86)  # Random User Agent
        }  # A very legit header
        # print("Sending Request")
        try:
            result = False
            response = requests.get(link, headers=headers, timeout=Settings.TIMEOUT)
            # print(response.text)  # Debug
            # print("Response receive")
            if response.status_code == 200:  # 200 OK
                if 'Sold Out</button>' not in response.text and 'Coming Soon</button>' not in response.text:
                    print(f'YES, {link}')
                    result = True
                else:
                    print(f'No, {link}')
                with lock:
                    v.value += 1
                    if result:
                        a.append(link)
                return None
            else:  # Non-success status code, failed
                 print(f'Code {response.status_code}, sleeping {Settings.TIMEOUT_RETRY} seconds')
                 time.sleep(Settings.TIMEOUT_RETRY)
                 fails += 1
        except requests.exceptions.ReadTimeout:
            # print(f'Timeout! Waiting {Settings.TIMEOUT_RETRY} seconds')
            time.sleep(Settings.TIMEOUT_RETRY)
            fails += 1
        except Exception as e:
            print(f'Error Info: {e}')
            print(f'Unknown error! Waiting {Settings.UNKNOWN_ERROR_RETRY} seconds')
            time.sleep(Settings.UNKNOWN_ERROR_RETRY)
            fails += 1


def amazon_detect(link: str, v, a, lock):
    fails = 0
    while True:
        if fails > Settings.MAX_RETRIES:
            print("Max retries used. Continuing. Maybe check Internet connection.")
            return False
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Referer": "https://www.google.com/",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": random.choice(win10_user_agents)# Random Windows 10 User Agent
        }
        # A list must be used here because amazon is different when a mobile user agent is given
        # print("Sending Request")
        try:
            result = False
            response = requests.get(link, headers=headers, timeout=Settings.TIMEOUT)
            # print(response.text)  # Debug
            # print("Response receive")
            if response.status_code == 200:  # 200 OK
                if 'not a robot' in response.text:
                    print(f'Amazon think we are bot, sleeping {Settings.BOT_RETRY} seconds')
                    time.sleep(Settings.BOT_RETRY)
                    fails+=1
                elif 'Available from' in response.text or 'Currently unavailable' in response.text:
                    print(f'No, {link}')
                else:
                    print(f'YES, {link}')
                    with open('debug.html', 'w') as f:
                        f.write(response.text)
                    result = True
                with lock:
                    v.value += 1
                    if result:
                        a.append(link)
                return None
            else:  # Non-success status code, failed
                 print(f'Code {response.status_code}, sleeping {Settings.TIMEOUT_RETRY} seconds')
                 time.sleep(Settings.TIMEOUT_RETRY)
                 fails += 1
        except requests.exceptions.ReadTimeout:
            # print(f'Timeout! Waiting {Settings.TIMEOUT_RETRY} seconds')
            time.sleep(Settings.TIMEOUT_RETRY)
            fails += 1
        except Exception as e:
            print(f'Error Info: {e}')
            print(f'Unknown error! Waiting {Settings.UNKNOWN_ERROR_RETRY} seconds')
            time.sleep(Settings.UNKNOWN_ERROR_RETRY)
            fails += 1
