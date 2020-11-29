from bs4 import BeautifulSoup
import requests
import json

urls = set()


def extract_all_links(search_url):
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('div', class_='row-body-inner')[1]
    links = results.find_all('a')
    return soup, links


def extract_url(links):
    for link in links:

        url = link.get('href')
        if url:  # if it exist
            url = url.replace('#scrollFullInfo', '').replace('?IsFeedbackTab=true', '').replace('&', "?")
            if 'Article' in url or 'knowledge' in url or 'BrandStore' in url or 'insider' in url or \
                    'power-requirements' in url or '.jpg' in url or 'EventSaleStore' in url or 'Category' in url or \
                    'INFOCARD' in url:
                continue
            urls.add(url)


search_urls = ["https://www.newegg.com/p/pl?N=100007709%20601359511%20601357282%208000&PageSize=96",
               # RTX 3000 + RX 6000
               'https://www.newegg.com/p/pl?d=rtx+3070&N=31001489&isdeptsrh=1',  # 3070 Combos
               'https://www.newegg.com/p/pl?d=rtx+3080&N=31001489&isdeptsrh=1',  # 3080 Combos
               'https://www.newegg.com/p/pl?d=rtx+3090&N=31001489&isdeptsrh=1',  # 3090 Combos
               'https://www.newegg.com/p/pl?d=rx+6800&N=31001489&isdeptsrh=1',  # 6800 Combos
               'https://www.newegg.com/p/pl?d=rx+6800xt&N=31001489&isdeptsrh=1',  # 6800xt Combos
               'https://www.newegg.com/p/pl?N=100007671%20601359163%208000&PageSize=96',  # Ryzen 5000
               'https://www.newegg.com/p/pl?d=ryzen+5600x&N=31001489&isdeptsrh=1',  # 5600x Combos
               'https://www.newegg.com/p/pl?d=ryzen+5800x&N=31001489&isdeptsrh=1',  # 5800x Combos
               'https://www.newegg.com/p/pl?d=ryzen+5900x&N=31001489&isdeptsrh=1',  # 5900x Combos
               'https://www.newegg.com/p/pl?d=ryzen+5950x&N=31001489&isdeptsrh=1',  # 5950x Combos
               ]

if __name__ == '__main__':
    for search_url in search_urls:
        soup, links = extract_all_links(search_url)

        extract_url(links)

        page_number = soup.find_all('span', class_='list-tool-pagination-text')
        if len(page_number) > 0:
            page_number = page_number[0].strong
            max_page = int(str(page_number).replace('<strong>1<!-- -->/<!-- -->', '').replace('</strong>', ''))
            for page in range(2, max_page + 1):
                soup, links = extract_all_links(search_url + f'&page={page}')
                extract_url(links)

    for url in urls:
        print(url)
    print(len(urls))

    with open('newegg_url.json', 'w') as f:
        json.dump(list(urls), f, indent=4)
