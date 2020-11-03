import time
import requests
import faker

BETWEEN_REQUESTS = 1.0
TIMEOUT = 2
TIMEOUT_RETRY = 5
UNKNOWN_ERROR_RETRY = 2
fake = faker.Faker()
url_bank = [
    "https://www.bestbuy.com/site/nvidia-geforce-rtx-3070-8gb-gddr6-pci-express-4-0-graphics-card-dark-platinum-and-black/6429442.p?skuId=6429442",
    "https://www.bestbuy.com/site/nvidia-geforce-rtx-3080-10gb-gddr6x-pci-express-4-0-graphics-card-titanium-and-black/6429440.p?skuId=6429440",
    "https://www.bestbuy.com/site/nvidia-geforce-rtx-3090-24gb-gddr6x-pci-express-4-0-graphics-card-titanium-and-black/6429434.p?skuId=6429434",
    "https://www.bestbuy.com/site/msi-nvidia-geforce-gtx-1650-super-4gb-gddr6-pci-express-3-0-graphics-card-black-gray/6397798.p?skuId=6397798"  # Testing, this should be in stock
]


def detect(link: str):
    headers = {
        "accept": "text/html",
        # "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US",
        "User-Agent": fake.chrome(version_from=75, version_to=86)  # Random User Agent
    }  # A very legit header
    print("Sending Request")
    try:
        response = requests.get(link, headers=headers, timeout=TIMEOUT)
        # print(response.text)  # Debug
        print("Response receive")
        if 'Sold Out</button>' not in response.text:
            print("Yes")
        else:
            print("No")
    except requests.exceptions.ReadTimeout:
        print(f'Timeout! Waiting {TIMEOUT_RETRY} seconds')
        time.sleep(TIMEOUT_RETRY)
        detect(link)
    # finally:
    #     print(f'Unknown error! Waiting {UNKNOWN_ERROR_RETRY} seconds')
    #     time.sleep(UNKNOWN_ERROR_RETRY)


if __name__ == "__main__":
    for url in url_bank:
        detect(url)
