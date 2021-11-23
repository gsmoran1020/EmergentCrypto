import requests
import os
import tweepy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

API_KEY = os.environ.get('API_KEY')
API_SECRET = os.environ.get('API_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_SECRET = os.environ.get('ACCESS_SECRET')
GOOGLE_CHROME_BIN = os.environ.get('GOOGLE_CHROME_BIN')
CHROMEDRIVER_PATH = os.environ.get('CHROMEDRIVER_PATH')

def __get_most_recent(num: int) -> list[str]:

    options = Options()
    options.add_argument('--log-level=3')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.binary_location = GOOGLE_CHROME_BIN
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=options)
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



def create_content():

    data = get_coin_data(5)

    token_content = [f"${data[i]['symbol'].upper()} {data[i]['name']} {data[i]['website']}" for i in range(len(data))]

    content = f"""Most recent tokens:
1. {token_content[0]}
2. {token_content[1]}
3. {token_content[2]}
4. {token_content[3]}
5. {token_content[4]}
#crypto #altcoin
    """

    if len(content) > 277:
        token_content = [f"${data[i]['symbol'].upper()} {data[i]['website']}" for i in range(len(data))]

        content = f"""Most recent tokens:
1. {token_content[0]}
2. {token_content[1]}
3. {token_content[2]}
4. {token_content[3]}
5. {token_content[4]}
#crypto #altcoin
    """

    with open('lastpost.txt', 'r') as lastpost:
        prev_content = lastpost.read()
    
    if prev_content == content:
        return ''
    else:

        with open('lastpost.txt', 'w') as lastpost:
            lastpost.write(content)
            
        return content


def post_tweet(content: str):
    if content == '':
        pass
    else:
        auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
        api = tweepy.API(auth)

        try:
            api.update_status(content, card_uri='tombstone://card')
        except tweepy.errors.Forbidden as f:
            pass


content = create_content()

post_tweet(content)
