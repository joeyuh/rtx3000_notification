import time
import requests
import faker
from multiprocessing import Process, Value, Lock, Manager

from settings import *
from notify import *

fake = faker.Faker()


def detect(link: str, v, a, lock):
    fails = 0
    while True:  # Need to while true until reached max retries
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
            if response.status_code == 200:  # 200 OK
                # print(response.text)  # Debug
                # print("Response receive")
                if 'Sold Out</button>' not in response.text and 'Coming Soon</button>' not in response.text:
                    print(f'YES, {link}')
                    result = True
                else:
                    print(f'No, {link}')
                with lock:  # Lock variable for editing
                    v.value += 1  # Success count ++
                    if result:
                        a.append(link)  # If in stock add link to the in stock list for notification
                return None  # exit the function if we succeed
            else:  # Non-success status code, failed
                print(f'Code {response.status_code}, sleeping {Settings.TIMEOUT_RETRY} seconds')
                time.sleep(Settings.TIMEOUT_RETRY)
                fails += 1
        except requests.exceptions.ReadTimeout:  # Timeout is typical
            # print(f'Timeout! Waiting {Settings.TIMEOUT_RETRY} seconds')
            time.sleep(Settings.TIMEOUT_RETRY)
            fails += 1
            # continue to next try
        except Exception as e:  # Unknown error
            print(f'Error Info: {e}')
            print(f'Unknown error! Waiting {Settings.UNKNOWN_ERROR_RETRY} seconds')
            time.sleep(Settings.UNKNOWN_ERROR_RETRY)
            fails += 1
            # continue to next try


if __name__ == "__main__":
    with Manager() as manager:
        while True:  # Yes, while true
            start_time = time.time()
            v = Value('i', 0)  # success count
            l = manager.list()  # in stock list
            lock = Lock()  # variable lock
            procs = [Process(target=detect, args=(url, v, l, lock)) for url in Settings.url_bank]  # Multithreading
            for p in procs: p.start()  # Start all thread
            for p in procs: p.join()  # join all threads
            if v.value == 0:
                print(f'Detection of all the URL has failed. Sleeping for {Settings.UNKNOWN_ERROR_RETRY} seconds!')
                print('Maybe check your Internet connection!')
                time.sleep(Settings.UNKNOWN_ERROR_RETRY)
            else:
                print(f'Went through all URLS in {time.time() - start_time} seconds, '
                      f'{v.value} Success, {len(Settings.url_bank) - v.value} Failed')
                print("Links:")
                print(l)
                notify(l)
            print(f'Sleeping {Settings.BETWEEN_ROUNDS} seconds')
            time.sleep(Settings.BETWEEN_ROUNDS)
