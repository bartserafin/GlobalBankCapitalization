from bs4 import BeautifulSoup
import requests
import pandas as pd


def scrap_data():
    url = 'https://en.wikipedia.org/wiki/List_of_largest_banks'
    html_data = requests.get(url=url)
    # print(html_data.content)

    soup = BeautifulSoup(html_data.content, 'html.parser')
    # print(soup)

    data = pd.DataFrame(
        {
            'Name': [],
            'Country': [],
            "Market Cap (US$ Billion)": [],
        }
    )

    bank_name_lst = []
    country_name_lst = []
    market_cap_lst = []

    # From scrapped website, find required info
    for row in soup.find_all('tbody')[3].find_all('tr'):
        col = row.find_all('td')
        if not col:
            continue

        # Market Value
        market_cap = col[-1].get_text().strip()
        market_cap_lst.append(market_cap)

        # Name of the Bank
        bank_name = col[1].get_text().strip()
        bank_name_lst.append(bank_name)

        # Country of the bank
        country_name_links = col[1].find_all('a')
        country_name = country_name_links[0].get('title').strip()
        country_name_lst.append(country_name)

    # Append Data
    data['Name'] = bank_name_lst
    data['Market Cap (US$ Billion)'] = market_cap_lst
    data['Country'] = country_name_lst
    # print(data.head(5))

    # Save Data as .json
    f = open('bank_market_cap.json', 'w')
    f.write(data.to_json())
    f.close()
