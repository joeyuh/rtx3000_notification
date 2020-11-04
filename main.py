import time
import requests
import faker
from settings import *

fake = faker.Faker()


def detect(link: str, fails=0) -> bool:
    status = False
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
        return True
    except requests.exceptions.ReadTimeout:
        print(f'Timeout! Waiting {Settings.TIMEOUT_RETRY} seconds')
        time.sleep(Settings.TIMEOUT_RETRY)
        status = detect(link, fails + 1)  # Retry might works, need to update status
    except Exception as e:
        print(f'Error Info: {e}')
        print(f'Unknown error! Waiting {Settings.UNKNOWN_ERROR_RETRY} seconds')
        time.sleep(Settings.UNKNOWN_ERROR_RETRY)
        status = detect(link, fails + 1)  # Retry might works, need to update status

    return status


if __name__ == "__main__":
    while True:  # Yes, while true
        success = 0  # success count
        start_time = time.time()
        for url in Settings.url_bank:
            if detect(url):
                success += 1
            time.sleep(Settings.BETWEEN_REQUESTS)
        if success == 0:
            print(f'Detection of all the URL has failed. Sleeping for {Settings.UNKNOWN_ERROR_RETRY} seconds!')
            print('Maybe check your Internet connection!')
            time.sleep(Settings.UNKNOWN_ERROR_RETRY)
        else:
            print(
                f'Went through all URLS in {time.time() - start_time} seconds, {success} Success,'
                f' {len(Settings.url_bank) - success} Failed')
