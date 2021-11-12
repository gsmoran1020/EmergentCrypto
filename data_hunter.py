import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google_chrome'
CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'

def __get_most_recent(num: int) -> list[str]:

    options = Options()
    options.add_argument('--log-level=3')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.binary_location = GOOGLE_CHROME_PATH
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH  ,options=options)
    driver.get('https://www.coingecko.com/en/coins/recently_added')

    table = driver.find_elements(by=By.CSS_SELECTOR, value='table tbody tr td a')

    api_ids = [item.get_attribute('href').replace("https://www.coingecko.com/en/coins/", '') for item in table]
    api_ids = list(dict.fromkeys(api_ids))

    requested_tokens = [api_ids[i] for i in range(0, num)]

    return requested_tokens




def get_coin_data(num: int) -> list[dict]:

    coins = __get_most_recent(num)

    coin_data = []

    for i in range(len(coins)):
        response = requests.get(url=f'https://api.coingecko.com/api/v3/coins/{coins[i]}')
        coin_data_raw = response.json()
        
        data_dict = {
            'name': coin_data_raw['name'],
            'symbol': coin_data_raw['symbol'],
            'chain_id': coin_data_raw['asset_platform_id'],
            'token_contract': coin_data_raw['platforms'][coin_data_raw['asset_platform_id']],
            'website': coin_data_raw['links']['homepage'][0]
        }
        
        coin_data.append(data_dict)


    return coin_data