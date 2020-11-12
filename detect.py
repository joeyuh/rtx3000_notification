import time

import faker
import requests

from settings import *

fake = faker.Faker()

def bestbuy_detect(link: str, v, a, lock):
    fails = 0
    while True:
        if fails > Settings.MAX_RETRIES_COUNT:
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
            "User-Agent": fake.chrome(version_from=65, version_to=86)  # Random User Agent
        }  # A very legit header
        # print("Sending Request")
        try:
            result = False
            response = requests.get(link, headers=headers, timeout=Settings.TIMEOUT)
            # print(response.text)  # Debug
            # print("Response receive")
            if response.status_code == 200:  # 200 OK
                if 'Sold Out</button>' in response.text or 'Coming Soon</button>' in response.text:
                    print(f'No, {link}')
                elif 'This item is no longer available in new condition.' not in response.text:
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
        if fails > Settings.MAX_RETRIES_COUNT:
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
            # "User-Agent": random.choice(win10_user_agents)# Random Windows 10 User Agent
            "User-Agent": fake.chrome(version_from=65, version_to=86)  # Random User Agent
        }
        # A list must be used here because amazon is different when a mobile user agent is given
        # print("Sending Request")
        try:
            result = False
            response = requests.get(link, headers=headers, timeout=Settings.TIMEOUT)
            # print(response.text)  # Debug
            # print("Response receive")
            if response.status_code == 200:  # 200 OK
                if 'a-touch a-mobile' in response.text:
                    print('Somehow we have a touch screen user_agent, retrying immediately')
                    # fails += 1
                elif 'not a robot' in response.text:
                    # print(f'Amazon think we are bot, sleeping {Settings.BOT_RETRY} seconds')
                    time.sleep(Settings.BOT_RETRY)
                    fails += 1
                else:
                    if 'Available from' in response.text or 'Currently unavailable' in response.text:
                        print(f'No, {link}')
                    else:
                        if '<span class="tabular-buybox-text">Amazon.com</span>' in response.text:  # Amazon sold only
                            print(f'YES, {link}')
                            # with open('debug.html', 'w') as f:
                            #    f.write(response.text)
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


def newegg_detect(link: str, v, a, lock):
    fails = 0
    while True:
        if fails > Settings.MAX_RETRIES_COUNT:
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
            "User-Agent": fake.chrome(version_from=65, version_to=86)  # Random User Agent
        }  # A very legit header
        # print("Sending Request")
        try:
            result = False
            response = requests.get(link, headers=headers, timeout=Settings.TIMEOUT)
            # print(response.text)  # Debug
            # print("Response receive")
            if response.status_code == 200:  # 200 OK
                if 'CURRENTLY SOLD OUT' not in response.text and 'OUT OF STOCK' not in response.text:
                    if 'Sold by: <strong>Newegg' in response.text:
                        print(f'YES, {link}')
                        with open('debug.html', 'w') as f:
                            f.write(response.text)
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
