import requests
import faker
import time

from settings import *

fake = faker.Faker()


def bestbuy_detect(link: str, v, a, lock):
    fails = 0
    while True:
        if fails > Settings.MAX_RETRIES:
            print("Max retries used. Continuing. Maybe check Internet connection.")
            return False
        headers = {
            "accept": "text/html",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US",
            "User-Agent": fake.chrome(version_from=75, version_to=86)  # Random User Agent
        }  # A very legit header
        # print("Sending Request")
        try:
            result = False
            response = requests.get(link, headers=headers, timeout=Settings.TIMEOUT)
            # print(response.text)  # Debug
            # print("Response receive")
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
            "accept": "text/html",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US",
            "User-Agent": fake.chrome(version_from=75, version_to=86)  # Random User Agent
        }  # A very legit header
        # print("Sending Request")
        try:
            result = False
            response = requests.get(link, headers=headers, timeout=Settings.TIMEOUT)
            # print(response.text)  # Debug
            # print("Response receive")
            if 'Available from' in response.text or 'Currently unavailable' in response.text:
                print(f'No, {link}')
            else:
                print(f'YES, {link}')
                result = True
            with lock:
                v.value += 1
                if result:
                    a.append(link)
            return None
        except requests.exceptions.ReadTimeout:
            # print(f'Timeout! Waiting {Settings.TIMEOUT_RETRY} seconds')
            time.sleep(Settings.TIMEOUT_RETRY)
            fails += 1
        except Exception as e:
            print(f'Error Info: {e}')
            print(f'Unknown error! Waiting {Settings.UNKNOWN_ERROR_RETRY} seconds')
            time.sleep(Settings.UNKNOWN_ERROR_RETRY)
            fails += 1
