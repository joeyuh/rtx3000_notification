import time
import requests
import faker
from multiprocessing import Process, Value, Lock
from settings import *

fake = faker.Faker()


def detect(link: str, v, lock):
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
            response = requests.get(link, headers=headers, timeout=Settings.TIMEOUT)
            # print(response.text)  # Debug
            # print("Response receive")
            if 'Sold Out</button>' not in response.text and 'Coming Soon</button>' not in response.text:
                print(f'YES, {link}')
            else:
                print(f'No, {link}')
            with lock:
                v.value += 1
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


if __name__ == "__main__":
    while True:  # Yes, while true
        start_time = time.time()
        v = Value('i', 0)  # success count
        lock = Lock()
        procs = [Process(target=detect, args=(url, v, lock)) for url in Settings.url_bank]
        for p in procs: p.start()
        for p in procs: p.join()
        if v.value == 0:
            print(f'Detection of all the URL has failed. Sleeping for {Settings.UNKNOWN_ERROR_RETRY} seconds!')
            print('Maybe check your Internet connection!')
            time.sleep(Settings.UNKNOWN_ERROR_RETRY)
        else:
            print(f'Went through all URLS in {time.time() - start_time} seconds, '
                  f'{v.value} Success, {len(Settings.url_bank) - v.value} Failed')
        time.sleep(Settings.BETWEEN_ROUNDS)
