from bs4 import BeautifulSoup
import faker
import requests
import json

fake = faker.Faker()
urls = set()
search_urls = ['https://www.bestbuy.com/site/computer-cards-components/video-graphics-cards/abcat0507002.c?id=abcat0507002&qp=gpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~AMD%20Radeon%20RX%206800%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~AMD%20Radeon%20RX%206800%20XT%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203070%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203080%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203090']

if __name__ == '__main__':
    for search_url in search_urls:
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
            "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
        }  # A very legit header
        current_url = search_url
        while True:
            response = requests.get(current_url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            sku_item_list = soup.find_all('ol',class_='sku-item-list')[0]
            links = sku_item_list.find_all('a')
            for link in links:
                url = 'https://www.bestbuy.com' + link.get('href')
                url = url.replace('#tabbed-customerreviews','')
                urls.add(url)
            next_page = soup.find_all('a', class_='sku-list-page-next')
            if len(next_page) > 0:
                current_url = next_page[0].get('href')
                if not current_url:
                    break
            else:
                break

    for url in urls:
        print(url)

    print(len(urls))

    with open('bestbuy_url.json', 'w') as f:
        json.dump(list(urls), f, indent=4)
