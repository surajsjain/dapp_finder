import sys

import requests
from bs4 import BeautifulSoup
from secrets.cookies import github_cookie

def usage_stats(contract_address):
    cookies = github_cookie

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:100.0) Gecko/20100101 Firefox/100.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'If-None-Match': 'W/"9fef31759f86dcc19c79727867089080"',
    }

    params = {
        'q': contract_address,
        'type': 'code',
    }

    response = requests.get('https://github.com/search', params=params, cookies=cookies, headers=headers)
    response_soup = BeautifulSoup(response.content, 'html.parser')

    languages_and_counts_raw = response_soup.find("div", class_="border rounded-2 p-3 mb-3 d-none d-md-block")\
        .find_all("a", class_="filter-item")

    lang_counts = {}

    for raw_ele in languages_and_counts_raw:
        content_eles = raw_ele.text.split()
        lang_name = ''.join(content_eles[1:])
        lang_files_count = int(content_eles[0])
        lang_counts[lang_name] = lang_files_count

    print(lang_counts)


if __name__ == '__main__':
    contract_address = sys.argv[1]
    usage_stats(contract_address)